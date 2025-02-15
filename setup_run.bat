@echo off
echo Checking Python version...

:: Get Python version
for /f "delims=" %%v in ('python -V 2^>^&1') do set "PYTHON_VERSION=%%v"
set "PYTHON_VERSION=%PYTHON_VERSION:Python =%"

:: Check if Python version is 3.10 or higher
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    if %%a LSS 3 (
        echo Python 3.10 or higher is required.
        exit /b 1
    ) 
    if %%a EQU 3 if %%b LSS 10 (
        echo Python 3.10 or higher is required.
        exit /b 1
    )
)

echo Python version is sufficient: %PYTHON_VERSION%

echo Setting up the Flask environment...

:: Check if virtual environment exists, if not, create one
if not exist venv (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate the virtual environment
call .venv\Scripts\activate

:: Install required dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

:: Run the Flask app on port 5008
echo Starting Flask app on port 5008...
python app.py --port 5008
