"""Discord frontend for the Roblox Luau deobfuscator."""
from __future__ import annotations

import asyncio
import os
import sys
import tempfile
from pathlib import Path

import discord
from discord.ext import commands

ROOT = Path(__file__).resolve().parent
DEOB = ROOT / "deobf" / "deob.py"
TOKEN_ENV = "DISCORD_BOT_TOKEN"
MAX_FILE_BYTES = int(os.getenv("DEOB_MAX_FILE_BYTES", str(10 * 1024 * 1024)))
TIMEOUT_SECONDS = int(os.getenv("DEOB_TIMEOUT_SECONDS", "300"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)


async def run_deobfuscator(input_path: Path, output_path: Path) -> tuple[str, str]:
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        str(DEOB),
        str(input_path),
        "-o",
        str(output_path),
        "--no-pypy",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=str(ROOT),
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=TIMEOUT_SECONDS
        )
    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        raise TimeoutError
    if process.returncode != 0 or not output_path.is_file():
        details = (stderr or stdout).decode("utf-8", errors="replace")
        raise RuntimeError(details[-1500:] or "deobfuscator exited without an output file")
    return stdout.decode("utf-8", errors="replace"), stderr.decode("utf-8", errors="replace")


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user} ({bot.user.id})")


@bot.command(name="deobf")
async def deobf_command(ctx: commands.Context) -> None:
    if not ctx.message.attachments:
        await ctx.reply("Add a `.lua`, `.luau`, or `.txt` file to the `.deobf` command.")
        return

    attachment = ctx.message.attachments[0]
    if attachment.size > MAX_FILE_BYTES:
        await ctx.reply(f"That file is too large. The limit is {MAX_FILE_BYTES // (1024 * 1024)} MB.")
        return

    suffix = Path(attachment.filename).suffix.lower()
    if suffix not in {".lua", ".luau", ".txt"}:
        await ctx.reply("Attach a `.lua`, `.luau`, or `.txt` file.")
        return

    async with ctx.typing():
        with tempfile.TemporaryDirectory(prefix="deobf_discord_") as temp_dir:
            workdir = Path(temp_dir)
            input_path = workdir / (Path(attachment.filename).name or "script.lua")
            output_path = workdir / input_path.name
            await attachment.save(input_path)
            try:
                _, diagnostics = await run_deobfuscator(input_path, output_path)
            except TimeoutError:
                await ctx.reply("Deobfuscation timed out. Try a smaller script or contact the bot owner.")
                return
            except (OSError, RuntimeError) as exc:
                message = str(exc)
                await ctx.reply(f"Deobfuscation failed:\n```text\n{message[-1500:]}\n```")
                return

            detected = next(
                (line.split(": ", 1)[1] for line in diagnostics.splitlines() if line.startswith("[*] obfuscator: ")),
                "unknown",
            )
            await ctx.reply(
                f"Detected: **{detected}**",
                file=discord.File(output_path, filename=f"deobfuscated_{input_path.name}"),
            )


if __name__ == "__main__":
    token = os.getenv(TOKEN_ENV)
    if not token:
        raise SystemExit(f"Set the {TOKEN_ENV} environment variable before starting the bot.")
    bot.run(token)
