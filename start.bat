@echo off
chcp 65001 >nul
echo ========================================
echo PaddleOCR-VL-1.5
echo ========================================
echo.

:menu
echo   1. Install PaddleOCR-VL-1.5
echo   2. Verify the installation
echo   3. Basic example
echo   4. Transformers example
echo   5. Batch process a folder
echo   6. Web UI
echo   7. Quit
echo.

set /p choice="Select (1-7): "

if "%choice%"=="1" (
    call install.bat
    goto menu
) else if "%choice%"=="2" (
    echo.
    python test_installation.py
    echo.
    pause
    goto menu
) else if "%choice%"=="3" (
    echo.
    python demo_basic.py
    echo.
    pause
    goto menu
) else if "%choice%"=="4" (
    echo.
    python demo_transformers.py
    echo.
    pause
    goto menu
) else if "%choice%"=="5" (
    echo.
    python demo_batch.py
    echo.
    pause
    goto menu
) else if "%choice%"=="6" (
    call run_web_ui.bat
    goto menu
) else if "%choice%"=="7" (
    exit
) else (
    echo Not a valid option.
    echo.
    goto menu
)
