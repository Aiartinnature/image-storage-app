@echo off
echo Starting server shutdown process...

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrator privileges.
    echo Please run as administrator.
    pause
    exit /b 1
)

echo.
echo Stopping Python and Flask processes...

:: Kill Python processes
echo Terminating Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
if %errorLevel% equ 0 (
    echo Python processes terminated successfully.
) else (
    echo No Python processes found.
)

:: Kill Python3 processes if they exist
echo Terminating Python3 processes...
taskkill /F /IM python3.exe /T >nul 2>&1
if %errorLevel% equ 0 (
    echo Python3 processes terminated successfully.
) else (
    echo No Python3 processes found.
)

:: Kill Pythonw processes if they exist
echo Terminating Pythonw processes...
taskkill /F /IM pythonw.exe /T >nul 2>&1
if %errorLevel% equ 0 (
    echo Pythonw processes terminated successfully.
) else (
    echo No Pythonw processes found.
)

echo.
echo Checking for processes on port 5000...

:: Find and kill processes using port 5000
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000" 2^>nul') do (
    echo Found process using port 5000 with PID: %%a
    taskkill /F /PID %%a >nul 2>&1
    if !errorLevel! equ 0 (
        echo Successfully terminated process with PID: %%a
    ) else (
        echo Failed to terminate process with PID: %%a
    )
)

:: Double-check port 5000
netstat -ano | find ":5000" >nul 2>&1
if %errorLevel% equ 0 (
    echo Warning: Some processes on port 5000 could not be terminated.
) else (
    echo Port 5000 is clear.
)

echo.
echo Server shutdown process completed.
echo All Flask servers and Python processes have been stopped.
echo.
pause
