
@echo off
title Push to GitHub Assistant
cd /d "%~dp0"
echo ========================================================
echo             978 AUTH GITHUB PUSH UTILITY
echo ========================================================
echo.

:: Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed on this system or not in your PATH.
    echo Please download and install Git from: https://git-scm.com/
    echo.
    pause
    exit /b
)

:: Initialize git repository if it hasn't been initialized yet
if not exist ".git" (
    echo Initializing local Git repository...
    git init
    echo.
)

:: Embedded credentials using the new repository and token
set "REPO_URL=https://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@github.com/ddosking5314-png/deobf.git"

echo Staging project files...
git add .

echo.
echo Committing files...
git config user.email "carsonator5314@gmail.com"
git config user.name "HeheheheheheNotahecker"
git commit -m "Deploy 978 Auth"

echo.
echo Setting branch to main...
git branch -M main

:: Safe remote configuration
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%

echo.
echo Pushing codebase to GitHub...
git push -u origin main --force

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo SUCCESS: Project successfully pushed to GitHub!
    echo ========================================================
) else (
    echo.
    echo ERROR: Push failed. If it fails, ensure the 'authtest' 
    echo repository exists on the 'HeheheheheheNotahecker' account.
)

echo.
pause