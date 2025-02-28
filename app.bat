@echo off

REM Change to the location of Python executable
call venv\Scripts\activate

REM Run the Python script
python app.py

REM Return to the original directory
cd /d %current_dir%

REM Pause to keep the command prompt window open (optional)
pause