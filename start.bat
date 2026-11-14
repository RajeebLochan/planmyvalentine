@echo off
echo.
echo ====================================
echo   💘 PlanMyValentine - Starting...
echo ====================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo ✅ .env file created!
    echo ⚠️  Please add your OPENAI_API_KEY to .env file
    echo.
)

REM Run migrations
echo 📊 Checking database...
python manage.py migrate --no-input

echo.
echo ====================================
echo   ✅ Server is starting!
echo   🌐 Open: http://127.0.0.1:8000/
echo ====================================
echo.
echo   Press Ctrl+C to stop the server
echo.

REM Start server
python manage.py runserver

pause
