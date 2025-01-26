# Webstack API
Django API with Supabase authentication for managing products and orders.


📦 WEBSTACK PROJECT
├── 🔧 Architecture
│   ├── Backend: Django REST Framework
│   ├── Database: Supabase (PostgreSQL)
│   └── Auth: Supabase JWT
│
├── 🗂️ Structure
│   ├── /webstack_django/
│   │   ├── settings.py (Configuration Django + Supabase)
│   │   └── urls.py (Routes principales)
│   │
│   ├── /api/
│   │   ├── models.py (Product, Order)
│   │   ├── views.py (ProductViewSet, OrderViewSet)
│   │   ├── serializers.py (ProductSerializer, OrderSerializer)
│   │   └── authentication.py (SupabaseAuthentication)
│   │
│   └── /tests/
│       ├── test_auth.html (Test d'authentification)
│       └── test_api.html (Test des endpoints)
│
├── 🛣️ API Endpoints
│   ├── /api/products/ (GET, POST)
│   ├── /api/products/{id}/ (GET)
│   └── /api/orders/ (GET, POST)
│
├── 🔐 Sécurité
│   ├── JWT Authentication
│   ├── Row Level Security (RLS)
│   └── Variables d'environnement
│
└── 📝 Configuration
    ├── requirements.txt
    ├── .env
    └── README.md


    
Realization and contribution guidelines:
BACKEND:
CONTRIBUTING:  # BENTAIFOUR MOHAMMED   # KASSIM
- Create a Django project and a Supabase database
- Configure the project to use Supabase
- Create an API application with authentication and serializers
- Implement the necessary views and endpoints
- Test the API using Swagger or ReDoc
- Document the API using Swagger or ReDoc

FRONTEND:
- Create a React or Vue.js frontend application
- Connect it to the API
- Implement the necessary components and pages
- Test the frontend application
- Document the frontend application using Storybook
- Deploy the frontend application using Docker or similar

## Requirements

- Python 3.12+
- PostgreSQL (via Supabase)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-name/webstack.git
cd webstack

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file with the following variables:
```
SECRET_KEY=your-secret-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
DB_HOST=your-supabase-host
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password

5. Run the server:
```bash
python webstack_django/manage.py runserver
```
6. API Endpoints
Products
GET /api/v1/products/ - List of products
GET /api/v1/products/{id}/ - Product details
Orders
GET /api/v1/orders/ - List of the user's orders
POST /api/v1/orders/ - Create a new order
GET /api/v1/orders/{id}/ - Order details
Health
GET /api/health/ - Check the API's status
Authentication
The API uses Supabase authentication. To access the endpoints, you need to:

Obtain a JWT token via Supabase.
Include the token in the header: Authorization: Bearer <your-token>
Project Structure
bash
Copier le code
webstack_django/
├── api/                # Main API application
├── core/               # Central configuration
├── supabase/           # Supabase client and auth
└── webstack_django/    # Project configuration
Structure Explanation
bash
Copier le code
webstack_django/
├── api/                    # Main API application
│   ├── authentication.py   # Supabase authentication
│   ├── models.py           # Data models
│   ├── serializers.py      # Serializers
│   ├── supabase.py         # Supabase client
│   ├── urls.py             # API routes
│   └── views.py            # API views
│
├── core/                   # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URLs
│   └── wsgi.py             # WSGI configuration
│
├── .env.example            # Environment variables example
├── .gitignore              # Ignored files
├── README.md               # Documentation
└── requirements.txt        # Dependencies



