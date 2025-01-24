# API Documentation

## Overview

This documentation describes the REST API endpoints for our e-commerce backend. The API is built with Django REST Framework and uses Supabase for authentication and data storage.

## Base URLs

- API Base URL: `http://localhost:8000/api/v1/`
- Supabase URL: `https://hbqpplveyaofcqtuippl.supabase.co`

## Authentication

Authentication is handled by Supabase. You need to include the Supabase token in your API requests:

```http
Authorization: Bearer <supabase_token>
```

To get the authentication token, use Supabase's authentication methods in your frontend:

```javascript
const { user, session } = await supabase.auth.signIn({
  email: 'user@example.com',
  password: 'your_password'
})

// The access token will be in:
const token = session.access_token
```

## Products API

### List Products
```http
GET /products/
```

Query parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10)
- `search`: Search term
- `category_id`: Filter by category ID
- `price_min`: Minimum price
- `price_max`: Maximum price
- `stock`: Filter by stock availability (true/false)

Response:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/v1/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Product Name",
            "description": "Product description",
            "price": "29.99",
            "stock": 50,
            "category_id": "550e8400-e29b-41d4-a716-446655440001",
            "image_url": "https://example.com/image.jpg",
            "created_at": "2024-01-24T15:44:28+01:00",
            "updated_at": "2024-01-24T15:44:28+01:00"
        }
    ]
}
```

### Get Product Details
```http
GET /products/{id}/
```

Response: Same as single product in list response

## Orders API

### Create Order
```http
POST /orders/
```

Request body:
```json
{
    "items": [
        {
            "product_id": "550e8400-e29b-41d4-a716-446655440000",
            "quantity": 2
        }
    ],
    "shipping_address": {
        "street": "123 Main St",
        "city": "City Name",
        "country": "Country Name",
        "postal_code": "12345"
    }
}
```

Response:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "order_number": "ORD-2024-0001",
    "status": "pending",
    "total_amount": "59.98",
    "items": [
        {
            "product_id": "550e8400-e29b-41d4-a716-446655440000",
            "product_name": "Product Name",
            "quantity": 2,
            "unit_price": "29.99",
            "total_price": "59.98"
        }
    ],
    "shipping_address": {
        "street": "123 Main St",
        "city": "City Name",
        "country": "Country Name",
        "postal_code": "12345"
    },
    "created_at": "2024-01-24T15:44:28+01:00"
}
```

### Get Order Status
```http
GET /orders/{id}/
```

Response: Same as order creation response

## Error Handling

The API uses standard HTTP status codes:

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

Error response format:
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message"
    }
}
```

## Rate Limiting

The API has rate limiting enabled:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

## Frontend Integration Example

```javascript
// Initialize Supabase client
const supabase = createClient(
  'https://hbqpplveyaofcqtuippl.supabase.co',
  'your-anon-key'
)

// Example function to fetch products
async function getProducts(page = 1) {
  const token = (await supabase.auth.getSession()).data.session?.access_token
  
  const response = await fetch(
    `http://localhost:8000/api/v1/products/?page=${page}`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    }
  )
  
  return await response.json()
}
```

## Need Help?

For technical support or questions about the API:
- Email: support@example.com
- Documentation Repository: https://github.com/your-org/api-docs
