# Webstack E-commerce Backend API

Backend API pour l'application e-commerce Webstack, construit avec Django REST Framework et Supabase.

## Structure du Projet

```
backend/
├── core/                  # Application principale
│   ├── auth/             # Authentification et autorisation
│   ├── products/         # Gestion des produits
│   ├── orders/           # Gestion des commandes
│   └── users/            # Gestion des utilisateurs
├── config/               # Configuration du projet
└── utils/               # Utilitaires partagés
```

## Configuration

1. Variables d'environnement requises :
```env
SUPABASE_URL=votre_url_supabase
SUPABASE_KEY=votre_clé_supabase
DJANGO_SECRET_KEY=votre_clé_secrète
```

2. Installation des dépendances :
```bash
pip install -r requirements/dev.txt
```

3. Migrations :
```bash
python manage.py migrate
```

## API Endpoints

### Authentification
- POST /api/auth/register/ - Inscription
- POST /api/auth/login/ - Connexion
- POST /api/auth/refresh/ - Rafraîchir le token
- POST /api/auth/logout/ - Déconnexion

### Produits
- GET /api/products/ - Liste des produits
- GET /api/products/{id}/ - Détails d'un produit
- POST /api/products/ - Créer un produit (Admin)
- PUT /api/products/{id}/ - Modifier un produit (Admin)
- DELETE /api/products/{id}/ - Supprimer un produit (Admin)

### Commandes
- GET /api/orders/ - Liste des commandes de l'utilisateur
- POST /api/orders/ - Créer une commande
- GET /api/orders/{id}/ - Détails d'une commande

### Utilisateurs
- GET /api/users/me/ - Profil de l'utilisateur
- PUT /api/users/me/ - Modifier le profil
- GET /api/users/ - Liste des utilisateurs (Admin)

## Sécurité

- Authentification JWT
- Row Level Security (RLS) avec Supabase
- Permissions basées sur les rôles
- Rate limiting
- CORS configuré

## Tests

```bash
python manage.py test
```

## Déploiement

Le backend est configuré pour être déployé sur Vercel.
