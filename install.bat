@echo off
chcp 65001 >nul
echo ========================================
echo PaddleOCR-VL-1.5 installer
echo ========================================
echo.

echo [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.8 or newer first.
    pause
    exit /b 1
)
echo.

echo [2/3] Installing PaddlePaddle
echo   1. GPU (CUDA 12.6)
echo   2. GPU (CUDA 11.8)
echo   3. CPU
set /p choice="Select (1-3): "

if "%choice%"=="1" (
    echo Installing GPU build for CUDA 12.6...
    python -m pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
) else if "%choice%"=="2" (
    echo Installing GPU build for CUDA 11.8...
    python -m pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
) else if "%choice%"=="3" (
    echo Installing CPU build...
    python -m pip install paddlepaddle==3.2.1
) else (
    echo Not a valid option. Defaulting to the CPU build.
    python -m pip install paddlepaddle==3.2.1
)
echo.

echo [3/3] Installing PaddleOCR...
python -m pip install -U "paddleocr[doc-parser]"
echo.

echo ========================================
echo Done.
echo ========================================
echo.
echo Verify with:  python test_installation.py
echo Or try:       paddleocr doc_parser -i test.png
echo.
pause
