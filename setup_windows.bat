@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  py -m venv .venv
) else (
  python -m venv .venv
)
if errorlevel 1 goto fail
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto fail
.venv\Scripts\python.exe manage.py makemigrations
if errorlevel 1 goto fail
.venv\Scripts\python.exe manage.py migrate
if errorlevel 1 goto fail
.venv\Scripts\python.exe manage.py seed_demo
if errorlevel 1 goto fail
.venv\Scripts\python.exe manage.py check
if errorlevel 1 goto fail
echo.
echo READY! Next: run "python manage.py createsuperuser" with the venv Python.
echo Then run "run_windows.bat" and open http://127.0.0.1:8000/admin/
pause
exit /b 0
:fail
echo Installation failed. Check Python 3.10+ and your internet connection.
pause
exit /b 1
