@echo off
cd /d "%~dp0"
"C:\Users\38089\AppData\Local\Programs\Python\Python314\python.exe" "%~dp0main.py"
if errorlevel 1 pause
