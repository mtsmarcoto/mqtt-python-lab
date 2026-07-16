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
start "Mosquitto Logs" /D "%CD%" powershell.exe -NoExit -Command "docker logs -f mqtt-broker"

echo Opening publisher terminal...
start "Publisher" /D "%CD%" powershell.exe -NoExit -ExecutionPolicy Bypass -Command ".\.venv\Scripts\Activate.ps1; python .\01_publisher_01.py"

echo Opening subscriber terminal...
start "Subscriber" /D "%CD%" powershell.exe -NoExit -ExecutionPolicy Bypass -Command ".\.venv\Scripts\Activate.ps1; python .\02_subscriber_01.py"

echo.
echo MQTT environment started.
echo Broker logs, subscriber, and publisher are in separate windows.
echo.