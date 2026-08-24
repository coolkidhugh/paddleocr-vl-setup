@echo off
chcp 65001 >nul
echo ========================================
echo PaddleOCR-VL-1.5 web UI
echo ========================================
echo.

echo Checking for Gradio...
python -c "import gradio" 2>nul
if errorlevel 1 (
    echo Gradio not found. Installing...
    pip install gradio
    echo.
)

echo Starting server. A browser will open at http://localhost:7860
echo Press Ctrl+C to stop.
echo.

python demo_web_ui.py
pause
