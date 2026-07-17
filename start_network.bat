@echo off
cd /d "%~dp0"

echo Starting Docker Desktop...
docker desktop start

echo Waiting for Docker Engine...

:wait_docker
docker info >nul 2>&1
if errorlevel 1 (
    timeout /t 2 /nobreak >nul
    goto wait_docker
)

echo Docker is running.

echo Starting MQTT broker...
docker start mqtt-broker

echo Opening broker logs...
start "mqtt-broker" /D "%CD%" powershell.exe -NoExit -Command "$Host.UI.RawUI.WindowTitle = 'mqtt-broker'; docker logs -f mqtt-broker"

echo Opening publisher terminal...
start "publisher_01" /D "%CD%" powershell.exe -NoExit -ExecutionPolicy Bypass -Command "$Host.UI.RawUI.WindowTitle = 'publisher_01'; .\.venv\Scripts\Activate.ps1; python .\01_publisher_01.py"

echo Opening subscriber terminal...
start "subscriber_01" /D "%CD%" powershell.exe -NoExit -ExecutionPolicy Bypass -Command "$Host.UI.RawUI.WindowTitle = 'subscriber_01'; .\.venv\Scripts\Activate.ps1; python .\02_subscriber_01.py"

echo Opening Inverter terminal...
start "inverter_01" /D "%CD%" powershell.exe -NoExit -ExecutionPolicy Bypass -Command "$Host.UI.RawUI.WindowTitle = 'inverter_01'; .\.venv\Scripts\Activate.ps1; python .\03_inverter_01.py"

echo Opening Control Center terminal...
start "control_center" /D "%CD%" powershell.exe -NoExit -ExecutionPolicy Bypass -Command "$Host.UI.RawUI.WindowTitle = 'control_center'; .\.venv\Scripts\Activate.ps1; python .\04_control_center.py"


echo.
echo MQTT environment started.
echo Broker logs, subscriber, and publisher are in separate windows.
echo.
