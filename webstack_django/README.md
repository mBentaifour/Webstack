# Webstack Django Project

## Description
Application web de gestion de produits utilisant Django et Supabase comme backend.

## Documentation API

La documentation complète de l'API est disponible aux endpoints suivants :

- Swagger UI : `/swagger/` - Interface interactive pour tester l'API
- ReDoc : `/redoc/` - Documentation détaillée de l'API
- OpenAPI JSON : `/swagger.json` - Spécification OpenAPI au format JSON

### Endpoints Principaux

#### Authentification
- `POST /api/auth/login/` - Connexion utilisateur
- `POST /api/auth/register/` - Inscription utilisateur
- `POST /api/auth/logout/` - Déconnexion
- `GET /api/auth/user/` - Informations utilisateur courant

#### Produits
- `GET /api/products/` - Liste des produits
- `POST /api/products/` - Créer un produit
- `GET /api/products/{id}/` - Détails d'un produit
- `PUT /api/products/{id}/` - Modifier un produit
- `DELETE /api/products/{id}/` - Supprimer un produit
- `GET /api/products/search/` - Rechercher des produits

#### Catégories
- `GET /api/categories/` - Liste des catégories
- `GET /api/categories/{id}/products/` - Produits d'une catégorie

#### Marques
- `GET /api/brands/` - Liste des marques
- `GET /api/brands/{id}/products/` - Produits d'une marque

#### Inventaire
- `GET /api/inventory/` - État du stock
- `GET /api/inventory/{product_id}/` - Stock d'un produit

### Authentification

L'API utilise l'authentification JWT. Pour les requêtes authentifiées, incluez le token dans le header :
```http
Authorization: Bearer <votre_token>
```

### Pagination

Les endpoints qui retournent des listes supportent la pagination avec les paramètres :
- `page` : Numéro de page (défaut: 1)
- `page_size` : Nombre d'éléments par page (défaut: 10)

### Filtres

Les endpoints de liste supportent le filtrage avec les paramètres :
- `search` : Recherche textuelle
- `category` : Filtrer par catégorie
- `brand` : Filtrer par marque
- `min_price` : Prix minimum
- `max_price` : Prix maximum
- `in_stock` : Produits en stock uniquement

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
2. Chargez les données initiales : `python manage.py load_test_data`

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

## Développement

### Commandes Utiles

- `python manage.py runserver` - Démarrer le serveur de développement
- `python manage.py load_test_data` - Charger les données de test
- `python manage.py test` - Exécuter les tests
- `python manage.py makemigrations` - Créer de nouvelles migrations
- `python manage.py migrate` - Appliquer les migrations

### Bonnes Pratiques

1. **Versionnement**
   - Utilisez des branches pour les nouvelles fonctionnalités
   - Faites des commits atomiques avec des messages clairs
   - Suivez la convention de nommage des branches : `feature/`, `bugfix/`, `hotfix/`

2. **Code**
   - Suivez PEP 8 pour le style de code Python
   - Documentez vos fonctions et classes avec des docstrings
   - Écrivez des tests pour les nouvelles fonctionnalités

3. **API**
   - Utilisez des verbes HTTP appropriés
   - Versionnez vos endpoints (/api/v1/, /api/v2/)
   - Gérez correctement les erreurs et les codes HTTP

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




# Session Management and Authentication Module by kassem saber Email kamsdonga@gmail.com

This module is responsible for handling **user session management**, **authentication**, and **sign-in/sign-up processes** for the project. The backend is developed using Django and integrates with **Supabase** for user authentication and session management.

## Features

- **Sign-Up**: Users can register with email, password, and additional metadata.
- **Sign-In**: Authentication using email and password.
- **Session Management**: Retrieve user sessions for persistent logins.
- **Email Check**: Validate if an email address is already registered.
- **CSRF Protection**: Ensures secure requests via Django's built-in CSRF middleware.
- **Validation**: Comprehensive validation for email format, password match, and required terms agreement.

---

## File Structure

### 1. `settings.py`
Contains the configurations for the Django project, including:
- Installed apps.
- Middleware setup.
- CORS and CSRF configurations for secure frontend-backend communication.
- Supabase credentials for authentication.

### 2. `urls.py`
Defines the URL routes for authentication-related APIs:
- `api/auth/signup/`: Handles user sign-up.
- `api/auth/signin/`: Handles user sign-in.
- `api/email_used_check_/`: Checks if an email is already registered.
- Additional routes for third-party login and session retrieval.

### 3. `views.py`
Implements the core logic for the following:
- **`signup_view`**: Handles user registration with input validation and Supabase integration.
- **`signin_view`**: Handles user authentication with email and password.
- **`retrieve_session`**: Retrieves the user session to maintain a persistent state.
- **`check_email`**: Validates email format and checks its existence in the database.

---

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install Dependencies**:
   Ensure `Django`, `supabase`, and other required packages are installed:
   ```bash
   pip install django supabase
   ```

3. **Configure Environment Variables**:
   Add the following to your `.env` file:
   ```
   SUPABASE_KEY=<your_supabase_key>
   SUPABASE_URL=<your_supabase_url>
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### 1. **Sign-Up**
**URL**: `/api/auth/signup/`  
**Method**: `POST`  
**Body Parameters**:
```json
{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "password": "password123",
  "confirmPassword": "password123",
  "language": "en",
  "country": "USA",
  "mobilePhone": "1234567890",
  "address1": "123 Main St",
  "address2": "Apt 4",
  "termsAgreed": true
}
```
**Response**:
- Success:  
  ```json
  { "message": "User created successfully", "access_token": "token_here" }
  ```
- Failure:  
  ```json
  { "error": "Passwords do not match" }
  ```

### 2. **Sign-In**
**URL**: `/api/auth/signin/`  
**Method**: `POST`  
**Body Parameters**:
```json
{
  "email": "johndoe@example.com",
  "password": "password123"
}
```
**Response**:
- Success:  
  ```json
  { "message": "Login successful", "access_token": "token_here" }
  ```
- Failure:  
  ```json
  { "error": "Invalid username or password" }
  ```

### 3. **Check Email**
**URL**: `/api/email_used_check_/`  
**Method**: `POST`  
**Body Parameters**:
```json
{ "email": "johndoe@example.com" }
```
**Response**:
- Email Exists:  
  ```json
  { "exists": true }
  ```
- Email Does Not Exist:  
  ```json
  { "exists": false }
  ```

### 4. **Retrieve Session**
**URL**: `/api/auth/retreivesession/`  
**Method**: `GET`  
**Response**:
- Success:  
  ```json
  { "session": { ... } }
  ```
- Failure:  
  ```json
  { "error": "something went wrong" }
  ```

---

## Security Considerations

1. **Environment Variables**:
   Ensure `SUPABASE_KEY` and `SUPABASE_URL` are securely stored in `.env` and never exposed.

2. **Production Settings**:
   - Set `DEBUG = False` in production.
   - Use strong, secret keys for `SECRET_KEY`.

3. **CSRF and CORS**:
   Properly configure `CSRF_TRUSTED_ORIGINS` and `CORS_ALLOWED_ORIGINS` to match your frontend domain.

---

## Testing

Use tools like **Postman** or **cURL** to test the endpoints. For example:
```bash
curl -X POST http://localhost:8000/api/auth/signup/ \
-H "Content-Type: application/json" \
-d '{
  "email": "test@example.com",
  "password": "password123",
  "confirmPassword": "password123",
  "termsAgreed": true
}'
```

---

## Contributions

Team contributions:
- **Backend**: Session management, authentication, sign-up/sign-in (your role).
- **Frontend**: Integration with backend APIs.
- **Database**: Configured using **Supabase**.

