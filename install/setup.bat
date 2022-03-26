@echo off
@setlocal enableextensions
@cd /d "%~dp0"
call tesseract-ocr-w64-setup-v5.0.1.20220118.exe
xcopy /E %cd%\ben.traineddata "C:\Program Files\Tesseract-OCR\tessdata" 
pause