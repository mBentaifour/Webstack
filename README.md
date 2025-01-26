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

