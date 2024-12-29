# Webstack Django Project

## Description
Application web de gestion de produits utilisant Django et Supabase comme backend.

## Structure du Projet
```
webstack_django/
├── main/
│   ├── auth/            # Authentification et gestion des utilisateurs
│   ├── products/        # Gestion des produits
│   ├── security/        # Politiques de sécurité
│   ├── supabase/        # Configuration Supabase
│   └── tests/           # Tests unitaires et d'intégration
├── data/                # Scripts de données et migrations
└── static/              # Fichiers statiques
```

## Configuration

### Variables d'Environnement
Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```env
# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here

# Supabase Configuration
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-service-role-key

# Admin Configuration
ADMIN_EMAIL=your-admin-email
ADMIN_PASSWORD=your-admin-password
```

### Base de Données
1. Exécutez les migrations : `python manage.py migrate`
2. Chargez les données initiales : `python setup_initial_data.py`

## Installation

1. Clonez le repository
2. Créez un environnement virtuel : `python -m venv venv`
3. Activez l'environnement virtuel :
   - Windows : `venv\Scripts\activate`
   - Unix/MacOS : `source venv/bin/activate`
4. Installez les dépendances : `pip install -r requirements.txt`
5. Configurez le fichier `.env`
6. Lancez les migrations
7. Créez un super utilisateur : `python manage.py createsuperuser`

## Tests

Pour exécuter les tests :
```bash
python manage.py test main.tests
```

## Fonctionnalités

- Authentification utilisateur via Supabase
- Gestion des produits (CRUD)
- Gestion des catégories et marques
- Interface d'administration
- API REST pour les produits

## Sécurité

- Politiques RLS (Row Level Security) Supabase
- Authentification JWT
- Protection CSRF
- Validation des données

## Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request
