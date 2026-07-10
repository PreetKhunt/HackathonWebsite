@echo off
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask application...
echo Visit: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
pause