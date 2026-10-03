@echo off
title Fowascend Deobfuscator - GitHub Push Utility
cd /d "%~dp0"
echo ========================================================
echo       FOWASCEND DEOBFUSCATOR GITHUB PUSH UTILITY
echo ========================================================
echo.

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in your PATH.
    pause
    exit /b
)

echo Pushing from: %cd%
echo.

set "GH_TOKEN=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"
set "REPO_URL=https://%GH_TOKEN%@github.com/fowascenddd/dbf.git"

echo __pycache__/ > .gitignore
echo *.pyc >> .gitignore
echo *.pyo >> .gitignore
echo .env >> .gitignore

git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%

echo Staging all files...
git add .
echo.

echo Files staged:
git status --short
echo.

echo Committing...
git config user.email "fowascend@deobfuscator.local"
git config user.name "fowascenddd"
git commit -m "Deploy Fowascend Deobfuscator"
if %errorlevel% neq 0 (
    echo Nothing new to commit, pushing existing commits...
)

echo.
echo Setting branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main --force

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo  SUCCESS: Pushed to github.com/fowascenddd/dbf
    echo ========================================================
) else (
    echo.
    echo ERROR: Push failed.
)

echo.
pause
