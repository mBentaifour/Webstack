# Webstack API

API Django avec authentification Supabase pour la gestion des produits et des commandes.

## Configuration requise

- Python 3.12+
- PostgreSQL (via Supabase)

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-nom/webstack.git
cd webstack
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Créer un fichier .env avec les variables suivantes :
```
SECRET_KEY=votre-cle-secrete
SUPABASE_URL=votre-url-supabase
SUPABASE_KEY=votre-cle-supabase
DB_HOST=votre-host-supabase
DB_NAME=votre-nom-db
DB_USER=votre-user-db
DB_PASSWORD=votre-password-db
```

5. Lancer le serveur :
```bash
python webstack_django/manage.py runserver
```

## Endpoints API

### Produits
- `GET /api/v1/products/` - Liste des produits
- `GET /api/v1/products/{id}/` - Détails d'un produit

### Commandes
- `GET /api/v1/orders/` - Liste des commandes de l'utilisateur
- `POST /api/v1/orders/` - Créer une nouvelle commande
- `GET /api/v1/orders/{id}/` - Détails d'une commande

### Santé
- `GET /api/health/` - Vérifier l'état de l'API

## Authentification

L'API utilise l'authentification Supabase. Pour accéder aux endpoints, vous devez :
1. Obtenir un token JWT via Supabase
2. Inclure le token dans le header : `Authorization: Bearer <votre-token>`

## Structure du projet

```
webstack_django/
├── api/                # Application API principale
├── core/              # Configuration centrale
├── supabase/          # Client et auth Supabase
└── webstack_django/   # Configuration du projet

STRUCTURE EXPLICATION 

webstack_django/
├── api/                    # Application API principale
│   ├── authentication.py   # Authentification Supabase
│   ├── models.py          # Modèles de données
│   ├── serializers.py     # Sérialiseurs
│   ├── supabase.py        # Client Supabase
│   ├── urls.py            # Routes API
│   └── views.py           # Vues API
│
├── core/                   # Configuration du projet
│   ├── settings.py        # Paramètres Django
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuration WSGI
│
├── .env.example           # Exemple de variables d'environnement
├── .gitignore             # Fichiers à ignorer
├── README.md              # Documentation
└── requirements.txt       # Dépendances