# Discord bot hosting

This project supports the `.deobf` Discord command. Users attach a `.lua`, `.luau`, or text file, and the bot runs the existing detector/dispatcher in `deobf/deob.py`, then sends the result back.

## Environment variable

The bot token variable is:

```text
DISCORD_BOT_TOKEN
```

Never commit the token. Create the bot in the Discord Developer Portal, enable the **Message Content Intent**, invite it with the `bot` and `applications.commands` scopes, and grant it permission to view channels, read message history, send messages, and attach files.

## Local run

```text
python -m pip install -r requirements.txt
set DISCORD_BOT_TOKEN=your-token-here
python bot.py
```

On PowerShell, use `$env:DISCORD_BOT_TOKEN = "your-token-here"` instead.

Use it in Discord as:

```text
.deobf
```

with the script attached to the same message.

## Railway

1. Push this repository to GitHub.
2. In Railway, create a new project and deploy from that repository.
3. Add the variable `DISCORD_BOT_TOKEN` in the Railway service's **Variables** tab. Paste the token as the value; do not include quotes.
4. Railway will use `railway.json`/`Procfile` to run `python bot.py` as a worker.
5. Redeploy and check the deployment logs for `Logged in as ...`.

Railway does not need an HTTP port for this Discord gateway worker. The repository includes the Luau runtime under `deobf/bin`; if it is missing or not executable in the deployed checkout, build it before deploying with `python deobf/build_luau.py --portable` and commit the resulting runtime as appropriate for your deployment workflow.

Optional variables are `DEOB_MAX_FILE_BYTES` and `DEOB_TIMEOUT_SECONDS`.
