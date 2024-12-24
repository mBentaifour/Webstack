import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstack_django.settings')
django.setup()

User = get_user_model()

# Créer un superutilisateur si aucun n'existe
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("Superutilisateur créé avec succès!")
else:
    print("Un superutilisateur existe déjà.")
