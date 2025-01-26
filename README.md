# Webstack API

A robust Django REST API with Supabase authentication for efficient product and order management.

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

## Features

- Secure authentication using Supabase
- RESTful API endpoints for products and orders
- PostgreSQL database integration
- Comprehensive error handling
- API health monitoring
- Detailed API documentation

## Requirements

- Python 3.12+
- PostgreSQL (via Supabase)
- Node.js 18+ (for frontend integration)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-name/webstack.git
cd webstack
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
source venv\Scripts\activate  # Windows
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
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
```

5. Run database migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## API Documentation

For detailed API documentation, please refer to [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

### Quick Endpoint Reference

#### Products
- `GET /api/v1/products/` - List all products
- `GET /api/v1/products/{id}/` - Get product details
- `POST /api/v1/products/` - Create a new product
- `PUT /api/v1/products/{id}/` - Update a product
- `DELETE /api/v1/products/{id}/` - Delete a product

#### Orders
- `GET /api/v1/orders/` - List user orders
- `POST /api/v1/orders/` - Create a new order
- `GET /api/v1/orders/{id}/` - Get order details

#### Health Check
- `GET /api/health/` - Check API status

## Authentication

The API uses Supabase authentication. To access the endpoints:
1. Obtain a JWT token from Supabase
2. Include the token in the header: `Authorization: Bearer <your-token>`

## Project Structure

```
webstack_django/
├── api/                    # Main API application
│   ├── authentication.py   # Supabase authentication
│   ├── models.py          # Data models
│   ├── serializers.py     # Serializers
│   ├── supabase.py        # Supabase client
│   ├── urls.py            # API routes
│   └── views.py           # API views
│
├── core/                   # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URLs
│   └── wsgi.py            # WSGI configuration
│
├── .env.example           # Environment variables example
├── .gitignore             # Ignored files
├── README.md              # Documentation
└── requirements.txt       # Dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Realization and contribution guidelines:
1. BACKEND:

```python
**CONTRIBUTING:  # BENTAIFOUR MOHAMMED   # KASSIM

- Create a Django project and a Supabase database
- Configure the project to use Supabase
- Create an API application with authentication and serializers
- Implement the necessary views and endpoints
- Test the API using Swagger or ReDoc
- Document the API using Swagger or ReDoc

FRONTEND:
```React
- Create a React or Vue.js frontend application
- Connect it to the API
- Implement the necessary components and pages
- Test the frontend application
- Document the frontend application using Storybook
- Deploy the frontend application using Docker or similar




Here’s an optimized, professional, and structured version of your **README** that clearly documents the **auth_ module** and makes it easy for developers to integrate and understand:

---

# Authentication and Session Management Module  
**Developed by Kassem Saber**  
_Email: kamsdonga@gmail.com_  

This module provides robust **authentication** and **session management** functionalities for Django projects. It supports traditional email/password-based authentication, OAuth integrations, and session persistence, ensuring seamless integration with modern frontend frameworks.  

## Key Features  

- **User Registration (Sign-Up)**: Handles email/password registration with input validation and metadata storage.  
- **User Login (Sign-In)**: Secure authentication using email and password.  
- **OAuth Integration**: Easy-to-extend third-party login via Google, Bing, and others.  
- **Session Management**: Retrieve user sessions for persistent authentication.  
- **Email Validation**: Check if an email is already registered in the system.  
- **Secure APIs**: Ensures CSRF protection and follows best security practices.  

---

## File Structure  

### **1. `settings.py`**  
- Contains configurations for:  
  - Installed Django apps and middleware.  
  - Supabase integration credentials (`SUPABASE_KEY`, `SUPABASE_URL`).  
  - CSRF and CORS settings for secure communication with the frontend.  

### **2. `urls.py`**  
- Defines routes for authentication APIs, including:  
  - `/signup/`: User registration.  
  - `/signin/`: User login.  
  - `/email_used_check_/`: Check if an email exists.  
  - `/google_signin/`, `/bing_signin/`, etc.: OAuth login endpoints.  
  - `/retreivesession/`: Retrieve session details.  

### **3. `views.py`**  
- Core logic for authentication and session management, including:  
  - **`signup_view`**: Handles user registration with Supabase.  
  - **`signin_view`**: Verifies user credentials and provides session tokens.  
  - **`check_email`**: Validates and checks email existence in the database.  
  - **OAuth Handlers**: Redirect users to third-party login providers like Google.  

### **4. `utils/db_get_data.py`**  
- Helper functions for database operations, including:  
  - **`email_exists`**: Checks if an email is already registered.  
  - **`check_jwt`**: Validates JWT tokens for session security.  

---

## Setup and Integration  

### **1. Installation**  
1. Clone the repository:  
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```  

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

3. Configure environment variables in `.env`:  
   ```env
   SUPABASE_URL=<your-supabase-url>
   SUPABASE_KEY=<your-supabase-key>
   SUPABASE_SEC_JWT=<your-supabase-secret-jwt>
   USER=<database-user>
   PASSWORD=<database-password>
   HOST=<database-host>
   PORT=<database-port>
   DBNAME=<database-name>
   ```

### **2. Run the Server**  
Start the Django development server:  
```bash
python manage.py runserver
```  

### **3. API Endpoints**  

#### **Sign-Up**  
- **URL**: `/signup/`  
- **Method**: `POST`  
- **Request Body**:  
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "password123",
    "confirmPassword": "password123",
    "termsAgreed": true
  }
  ```  
- **Response**:  
  ```json
  { "message": "User created successfully", "access_token": "<token>" }
  ```

#### **Sign-In**  
- **URL**: `/signin/`  
- **Method**: `POST`  
- **Request Body**:  
  ```json
  { "email": "john.doe@example.com", "password": "password123" }
  ```  
- **Response**:  
  ```json
  { "message": "Login successful", "access_token": "<token>" }
  ```

#### **OAuth Login**  
- **URL**: `/google_signin/` (for Google)  
- **Method**: `GET`  
- **Response**: Redirects to Google OAuth URL.  

#### **Session Retrieval**  
- **URL**: `/retreivesession/`  
- **Method**: `GET`  
- **Response**:  
  ```json
  { "session": { ... } }
  ```

---

## Security Best Practices  

1. **Environment Variables**:  
   Ensure sensitive keys (e.g., `SUPABASE_KEY`, `SUPABASE_SEC_JWT`) are never hardcoded.  

2. **Production Readiness**:  
   - Set `DEBUG = False`.  
   - Use a strong secret key for `SECRET_KEY`.  

3. **Secure Communication**:  
   Properly configure `CSRF_TRUSTED_ORIGINS` and `CORS_ALLOWED_ORIGINS` for your frontend domain.  

4. **OAuth Links**:  
   Ensure OAuth providers are trusted and configured securely in Supabase.  

---

## Contributing  

Contributions to improve this module are welcome! Contact **kamsdonga@gmail.com** for queries or suggestions.  

---

## Example Testing (Using cURL)  

Test the sign-up endpoint:  
```bash
curl -X POST http://localhost:8000/signup/ \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "password123",
  "confirmPassword": "password123",
  "termsAgreed": true
}'
```

Test the email existence check:  
```bash
curl -X POST http://localhost:8000/email_used_check_/ \
-H "Content-Type: application/json" \
-d '{
  "email": "john.doe@example.com"
}'
```

---

This README is optimized for developers to understand and integrate the `auth_` module effortlessly into their projects.
