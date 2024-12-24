@echo off
echo Activation de l'environnement virtuel Django...
call django_env\Scripts\activate

echo Installation/mise a jour des dependances...
pip install -r requirements.txt

echo Application des migrations...
cd webstack_django
python manage.py migrate

echo Demarrage du serveur Django...
python manage.py runserver
pause
