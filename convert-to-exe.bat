call conda activate pdf-reader
pyinstaller run.py --exclude-module matplotlib
xcopy /E %cd%\assets %cd%\dist\run\assets