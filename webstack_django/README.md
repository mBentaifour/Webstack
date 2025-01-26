# Webstack Django Project

## Description

A **Django-based web application** for product management, integrated with **Supabase** for backend authentication and session management.

---

## API Documentation

Explore the complete API documentation:

- **Swagger UI**: `/swagger/` - Interactive API testing interface.
- **ReDoc**: `/redoc/` - Comprehensive API documentation.
- **OpenAPI JSON**: `/swagger.json` - OpenAPI specification in JSON format.

### Main Endpoints

#### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/user/` - Current user information

#### Products
- `GET /api/products/` - List products
- `POST /api/products/` - Create a product
- `GET /api/products/{id}/` - Product details
- `PUT /api/products/{id}/` - Update a product
- `DELETE /api/products/{id}/` - Delete a product
- `GET /api/products/search/` - Search products

#### Categories
- `GET /api/categories/` - List categories
- `GET /api/categories/{id}/products/` - Products in a category

#### Brands
- `GET /api/brands/` - List brands
- `GET /api/brands/{id}/products/` - Products in a brand

#### Inventory
- `GET /api/inventory/` - Inventory status
- `GET /api/inventory/{product_id}/` - Product stock

---

## Authentication and Session Management Module

### Key Features

- **User Registration**: Email/password registration with validation and metadata storage.
- **User Login**: Secure authentication with JWT support.
- **OAuth Integration**: Easily extendable with providers like Google, Bing, and others.
- **Session Management**: Retrieve and maintain persistent user sessions.
- **Email Validation**: Check if an email is already registered.

---

## File Structure

```
webstack_django/
├── main/
│   ├── auth/            # Authentication and user management
│   ├── products/        # Product management
│   ├── security/        # Security policies
│   ├── supabase/        # Supabase configurations
│   └── tests/           # Unit and integration tests
├── data/                # Data scripts and migrations
└── static/              # Static files
```

---

## Configuration

### Environment Variables

Create a `.env` file at the project root with the following variables:

```env
# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key

# Supabase Configuration
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-service-role-key

# Admin Configuration
ADMIN_EMAIL=your-admin-email
ADMIN_PASSWORD=your-admin-password
```

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

---

## Testing

Run the tests with:
```bash
python manage.py test
```

---

## API Usage

### Authentication Header

Include the JWT token in the header for authenticated requests:
```http
Authorization: Bearer <your_token>
```

### Pagination

Endpoints returning lists support pagination with the following parameters:
- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10)

### Filters

List endpoints support filtering using parameters like:
- `search`: Text search
- `category`: Filter by category
- `brand`: Filter by brand
- `min_price`: Minimum price
- `max_price`: Maximum price
- `in_stock`: Only products in stock

---

## Development

### Useful Commands

- `python manage.py runserver` - Start the development server
- `python manage.py makemigrations` - Create migrations
- `python manage.py migrate` - Apply migrations
- `python manage.py test` - Run tests
- `python manage.py load_test_data` - Load test data

### Best Practices

1. **Version Control**:
   - Use branches for new features or fixes.
   - Write clear, atomic commit messages.
   - Follow branch naming conventions like `feature/`, `bugfix/`, etc.

2. **Code Quality**:
   - Adhere to PEP 8 coding standards.
   - Add docstrings for all functions and classes.
   - Write tests for all new features.

3. **API Design**:
   - Use appropriate HTTP verbs.
   - Version API endpoints (`/api/v1/`, `/api/v2/`).
   - Handle errors gracefully with meaningful HTTP status codes.

---

## Security Best Practices

- Enable **Row-Level Security (RLS)** in Supabase.
- Use **JWT Authentication** for API security.
- Configure **CSRF protection** for all requests.
- Validate all user inputs to prevent injection attacks.

---

## Contribution Guidelines

1. Fork the repository.
2. Create a branch for your feature or bug fix.
3. Commit your changes.
4. Push the branch and open a pull request.

---

## Example API Requests

### Sign-Up

```bash
curl -X POST http://localhost:8000/api/auth/signup/ \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "password123",
  "confirmPassword": "password123",
  "termsAgreed": true
}'
```

### Email Validation

```bash
curl -X POST http://localhost:8000/api/auth/email_used_check_/ \
-H "Content-Type: application/json" \
-d '{
  "email": "john.doe@example.com"
}'
```
