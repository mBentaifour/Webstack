Project Name

# Bricolage Express - Guide d'utilisation rapide

## Application Web

Configuration
Environment Variables
You need to configure the following environment variables in the .env file:



## Fonctionnalités principales

- 🔍 Recherche de produits
- 📁 Filtrage par catégorie
- 🛒 Gestion du panier
- ⚙️ Administration des produits


License
This project is licensed under the MIT License. See LICENSE for more details.

Features
User authentication and management.
Database integration with SQLite.
Email notifications using Gmail SMTP.
Secure environment variable management with .env.

webstack_django/
├── api/
│   ├── __init__.py
│   ├── models.py      # Modèles de données
│   ├── serializers.py # Sérialiseurs pour l'API
│   ├── urls.py        # Routes de l'API
│   └── views.py       # Vues de l'API
├── core/
│   ├── __init__.py
│   ├── settings.py    # Configuration Django
│   ├── urls.py        # URLs principales
│   └── wsgi.py        # Configuration WSGI
├── supabase/
│   ├── __init__.py
│   ├── client.py      # Client Supabase
│   └── auth.py        # Authentification Supabase
├── .env.example
├── manage.py
└── requirements.txt

structure 

propre et focalisée sur l'essentiel :

Django pour l'API REST
Supabase pour la gestion des données
Authentification via Supabase

API (/api/) :

models.py : Modèles pour les produits et commandes
serializers.py : Sérialiseurs pour l'API
views.py : Vues pour gérer les requêtes API
urls.py : Configuration des routes

Core (/core/) :

settings.py : Configuration Django
urls.py : URLs principales
wsgi.py : Configuration WSGI

Supabase (/supabase/) :

client.py : Client Supabase
auth.py : Authentification