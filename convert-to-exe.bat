@echo off
@setlocal enableextensions
@cd /d "%~dp0"
call conda activate pdf-reader
pyinstaller run.py --noconfirm --exclude-module matplotlib --icon %cd%/assets/app_logo_icon.ico
xcopy /E %cd%\assets %cd%\dist\run\assets