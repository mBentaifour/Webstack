# API Documentation

## Overview

This documentation describes the API endpoints for the e-commerce backend. The API follows REST principles and uses JSON for request and response bodies.

## Base URL

```
http://localhost:8000/api/v1/
```

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your_token>
```

### Authentication Endpoints

#### Login
```http
POST /auth/login/
```

Request body:
```json
{
    "email": "user@example.com",
    "password": "your_password"
}
```

Response:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "name": "John Doe"
    }
}
```

## Products

### List Products
```http
GET /products/
```

Query parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10)
- `search`: Search term
- `category`: Filter by category ID
- `brand`: Filter by brand ID
- `min_price`: Minimum price
- `max_price`: Maximum price
- `in_stock`: Filter in-stock items only (true/false)

Response:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/v1/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Product Name",
            "slug": "product-name",
            "description": "Product description",
            "price": "99.99",
            "stock": 50,
            "category": {
                "id": 1,
                "name": "Category Name"
            },
            "brand": {
                "id": 1,
                "name": "Brand Name"
            },
            "image_url": "https://example.com/image.jpg",
            "is_active": true
        }
    ]
}
```

### Get Product Details
```http
GET /products/{id}/
```

Response: Same as single product in list response

## Orders

### Create Order
```http
POST /orders/
```

Request body:
```json
{
    "payment_method": "card",
    "shipping_address": "123 Main St, City, Country",
    "billing_address": "123 Main St, City, Country",
    "items": [
        {
            "product": 1,
            "quantity": 2
        }
    ]
}
```

Response:
```json
{
    "id": 1,
    "order_number": "CMD000001",
    "status": "pending",
    "status_display": "En attente",
    "payment_method": "card",
    "payment_method_display": "Carte bancaire",
    "subtotal": "199.98",
    "tax": "40.00",
    "shipping_cost": "0.00",
    "total": "239.98",
    "items": [
        {
            "id": 1,
            "product": 1,
            "product_name": "Product Name",
            "product_price": "99.99",
            "quantity": 2,
            "unit_price": "99.99",
            "total_price": "199.98"
        }
    ]
}
```

### Process Payment
```http
POST /orders/{id}/process_payment/
```

Response:
```json
{
    "client_secret": "pi_3NqKsP2eZvKYlo2C1gH1YzJO_secret_abcdef",
    "payment_id": 1
}
```

### Confirm Payment
```http
POST /orders/{id}/confirm_payment/
```

Request body:
```json
{
    "payment_intent_id": "pi_3NqKsP2eZvKYlo2C1gH1YzJO"
}
```

Response:
```json
{
    "status": "payment_confirmed"
}
```

## Payments

### List Payments
```http
GET /payments/
```

Response:
```json
{
    "count": 10,
    "results": [
        {
            "id": 1,
            "order_number": "CMD000001",
            "amount": "239.98",
            "payment_method": "card",
            "payment_method_display": "Carte bancaire",
            "status": "completed",
            "status_display": "Complété",
            "transaction_id": "pi_3NqKsP2eZvKYlo2C1gH1YzJO",
            "created_at": "2025-01-13T19:00:00Z"
        }
    ]
}
```

### Request Refund
```http
POST /payments/{id}/refund/
```

Request body:
```json
{
    "reason": "customer_requested"
}
```

Response:
```json
{
    "status": "refunded",
    "refund_id": "re_3NqKsP2eZvKYlo2C1gH1YzJO"
}
```

## Error Handling

The API uses standard HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

Error response format:
```json
{
    "error": "Error message",
    "detail": "Detailed error description"
}
```

## Pagination

List endpoints support pagination with the following format:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/v1/endpoint/?page=2",
    "previous": null,
    "results": []
}
```

## Testing the API

You can test the API using the interactive Swagger documentation at:
```
http://localhost:8000/swagger/
```

Or using the ReDoc documentation at:
```
http://localhost:8000/redoc/
```

## Implementation Example (JavaScript)

```javascript
// Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';
const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
};

// Create an order
async function createOrder(orderData) {
    const response = await fetch(`${API_BASE_URL}/orders/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(orderData)
    });
    return await response.json();
}

// Process payment
async function processPayment(orderId) {
    const response = await fetch(`${API_BASE_URL}/orders/${orderId}/process_payment/`, {
        method: 'POST',
        headers
    });
    return await response.json();
}

// Example usage
async function checkout(items) {
    try {
        // 1. Create order
        const order = await createOrder({
            payment_method: 'card',
            shipping_address: '123 Main St',
            billing_address: '123 Main St',
            items: items
        });

        // 2. Process payment
        const { client_secret } = await processPayment(order.id);

        // 3. Confirm payment with Stripe
        const { paymentIntent } = await stripe.confirmCardPayment(client_secret, {
            payment_method: {
                card: elements.getElement('card')
            }
        });

        // 4. Confirm payment on backend
        const confirmation = await fetch(`${API_BASE_URL}/orders/${order.id}/confirm_payment/`, {
            method: 'POST',
            headers,
            body: JSON.stringify({
                payment_intent_id: paymentIntent.id
            })
        });

        return confirmation.json();
    } catch (error) {
        console.error('Checkout error:', error);
        throw error;
    }
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:
- Anonymous users: 100 requests per hour
- Authenticated users: 1000 requests per hour

Rate limit headers are included in responses:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 3600
```

## Webhooks

The API provides webhooks for asynchronous events:
- Payment successful
- Payment failed
- Refund processed
- Order status updated

To receive webhooks, register your endpoint in the admin interface.
