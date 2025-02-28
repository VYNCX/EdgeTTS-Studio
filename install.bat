@echo off
REM Prompt user for GPU or CPU usage
set /p use_gpu="Do you want to use GPU? (y/n): "

REM Prompt user for GPU or CPU usage
set /p use_clone="Do you want to use Voice Clone? (y/n): "

REM Create a virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install required dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

if /I "%use_gpu%"=="y" (
    echo Installing GPU-specific dependencies...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
)

if /I "%use_clone%"=="y" (
    REM Download OpenVoice models
    echo Downloading OpenVoice models...
    powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/VYNCX/OpenVoice-WebUI/releases/download/Download/OPENVOICE_MODELS.zip', 'OPENVOICE_MODELS.zip')"

    REM Extract the models
    echo Extracting OpenVoice models...
    powershell -Command "Expand-Archive -Path 'OPENVOICE_MODELS.zip' -DestinationPath './OPENVOICE_MODELS' -Force"

    REM Clean up zip file
    del OPENVOICE_MODELS.zip
)

REM Run the application
echo Running app.py...
python app.py

REM Deactivate the virtual environment
echo Deactivating virtual environment...
deactivate

echo Setup complete. The virtual environment is ready.
pause