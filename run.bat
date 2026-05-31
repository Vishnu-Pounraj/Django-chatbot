@echo off
echo Starting Django server...

REM Activate virtual environment
call .venv\Scripts\activate

REM Start server in background
start cmd /k python manage.py runserver

REM Wait a bit for server to start
timeout /t 2 >nul

REM Open browser
start http://127.0.0.1:8000/

pause