@echo off
echo Starting ARCFORM Frontend Server on port 5500...
start cmd /c "cd frontend && python -m http.server 5500"

echo Starting ARCFORM Backend Server on port 8000...
start cmd /c "cd backend && venv\Scripts\activate && python manage.py runserver"

echo Opening ARCFORM Website...
timeout /t 3 >nul
start http://localhost:5500/index.html
