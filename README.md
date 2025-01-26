# Webstack API

A robust Django REST API with Supabase authentication for efficient product and order management.

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