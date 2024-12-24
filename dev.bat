@echo off
echo Starting development servers...

:: Start Django server
start cmd /k "cd backend && django_env\Scripts\activate && python manage.py runserver"

:: Start React development server
start cmd /k "cd frontend && npm run dev"

echo Development servers started!
echo Django server: http://localhost:8000
echo React server: http://localhost:5173
