@echo off
echo === Vérification de l'environnement ===
python -c "import django" 2>nul
if errorlevel 1 (
    echo Django n'est pas installé. Installation...
    pip install -r requirements.txt
)

echo === Vérification de la base de données ===
python manage.py migrate

echo === Vérification des tables Supabase ===
python init_tables.py

echo === Démarrage du serveur de développement ===
echo Le serveur sera accessible à l'adresse: http://localhost:8000
python manage.py runserver
