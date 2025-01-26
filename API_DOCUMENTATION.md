# Webstack API Documentation

## Table of Contents
- [Overview](#overview)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)
- [Code Examples](#code-examples)
- [Frontend Integration Guide](#frontend-integration-guide)
- [Image Handling](#image-handling)

## Overview

The Webstack API provides a RESTful interface for managing products and orders. It uses Supabase for authentication and PostgreSQL for data storage.

### Base URLs
- Production: `https://api.webstack.com`
- Development: `http://localhost:8000`

### Global Headers
All requests must include:
```
Content-Type: application/json
Authorization: Bearer <your_supabase_token>
```

## Authentication

Authentication is handled through Supabase. Here's how to implement it:

```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// Sign In
async function signIn(email, password) {
  const { user, error } = await supabase.auth.signInWithPassword({
    email,
    password
  });
  return { user, error };
}

// Sign Up
async function signUp(email, password) {
  const { user, error } = await supabase.auth.signUp({
    email,
    password
  });
  return { user, error };
}

// Sign Out
async function signOut() {
  const { error } = await supabase.auth.signOut();
  return { error };
}
```

## Frontend Integration Guide

### Initial Setup

1. Install the required dependencies:
```bash
npm install @supabase/supabase-js
# or
yarn add @supabase/supabase-js
```

2. Configure your environment variables:
```javascript
// .env
VITE_BACKEND_URL=http://localhost:8000
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

### Authentication Flow

1. **User Registration**
```javascript
const { user, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password'
});

// Handle verification email if enabled
if (user && !error) {
  // Redirect to verification page or show message
}
```

2. **User Login**
```javascript
const { user, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'secure-password'
});

if (user && !error) {
  // Store session or redirect to dashboard
}
```

3. **Session Management**
```javascript
// Check active session
const session = supabase.auth.session();

// Subscribe to auth changes
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') {
    // Update application state
  }
  if (event === 'SIGNED_OUT') {
    // Clear application state
  }
});
```

### Common Frontend Patterns

#### Loading States
```javascript
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState(null);

async function fetchProducts() {
  setIsLoading(true);
  try {
    const products = await api.get('/api/products/');
    return products;
  } catch (err) {
    setError(err.message);
  } finally {
    setIsLoading(false);
  }
}
```

#### Error Handling
```javascript
function handleApiError(error) {
  switch (error.status) {
    case 401:
      // Redirect to login
      router.push('/login');
      break;
    case 403:
      toast.error('You do not have permission to perform this action');
      break;
    case 404:
      toast.error('Resource not found');
      break;
    default:
      toast.error('An unexpected error occurred');
  }
}
```

#### Data Caching
```javascript
// Using React Query example
const { data: products, isLoading } = useQuery(
  'products',
  () => api.get('/api/products/'),
  {
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 30 * 60 * 1000 // 30 minutes
  }
);
```

## API Endpoints

### Products

#### List Products
```http
GET /api/products/
```

**Response** `200 OK`
```json
{
  "products": [
    {
      "id": "uuid",
      "name": "Product Name",
      "description": "Product Description",
      "price": 99.99,
      "created_at": "2024-03-20T12:00:00Z"
    }
  ]
}
```

#### Get Product Details
```http
GET /api/products/{id}/
```

#### Create Product
```http
POST /api/products/
```

**Request Body**
```json
{
  "name": "New Product",
  "description": "Product Description",
  "price": 99.99
}
```

#### Update Product
```http
PUT /api/products/{id}/
```

#### Delete Product
```http
DELETE /api/products/{id}/
```

### Orders

#### List Orders
```http
GET /api/orders/
```

#### Get Order Details
```http
GET /api/orders/{id}/
```

#### Create Order
```http
POST /api/orders/
```

**Request Body**
```json
{
  "products": ["product_id_1", "product_id_2"],
  "shipping_address": {
    "street": "123 Main St",
    "city": "City",
    "country": "Country",
    "postal_code": "12345"
  }
}
```

## Error Handling

The API uses standard HTTP status codes and returns error messages in JSON format:

```javascript
async function handleApiError(error) {
  if (error.status === 401) {
    // Expired or invalid token
    await signOut();
    window.location.href = '/login';
  } else if (error.status === 403) {
    // Unauthorized access
    console.error('Unauthorized access');
  } else if (error.status === 404) {
    // Resource not found
    console.error('Resource not found');
  } else {
    // Other error
    console.error('An error occurred:', error);
  }
}
```

### Common Error Codes
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Server Error

## Code Examples

### Complete API Client Implementation

```javascript
class Api {
  constructor(config) {
    this.baseUrl = config.backendUrl;
    this.supabase = createClient(config.supabaseUrl, config.supabaseKey);
  }

  async getHeaders() {
    const session = this.supabase.auth.session();
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${session?.access_token}`
    };
  }

  async get(endpoint) {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        headers: await this.getHeaders()
      });
      if (!response.ok) throw response;
      return response.json();
    } catch (error) {
      handleApiError(error);
      throw error;
    }
  }

  async post(endpoint, data) {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers: await this.getHeaders(),
        body: JSON.stringify(data)
      });
      if (!response.ok) throw response;
      return response.json();
    } catch (error) {
      handleApiError(error);
      throw error;
    }
  }
}

// Usage Examples
const api = new Api({
  backendUrl: 'http://localhost:8000',
  supabaseUrl: 'https://your-project.supabase.co',
  supabaseKey: 'your-supabase-key'
});

// List products
async function displayProducts() {
  try {
    const products = await api.get('/api/products/');
    console.log('Products:', products);
  } catch (error) {
    console.error('Error fetching products:', error);
  }
}

// Create order
async function createNewOrder(orderData) {
  try {
    const order = await api.post('/api/orders/', orderData);
    console.log('Order created:', order);
  } catch (error) {
    console.error('Error creating order:', error);
  }
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

## Support

For support or feature requests, please:
1. Check the existing documentation
2. Search for existing issues on GitHub
3. Open a new issue if needed

## Changelog

### v1.0.0 (2024-03-20)
- Initial release
- Basic CRUD operations for products and orders
- Supabase authentication integration

## Image Handling

### Option 1: Using Supabase Storage (Recommended)
```javascript
// Upload product image
async function uploadProductImage(file) {
  const { data, error } = await supabase
    .storage
    .from('products')
    .upload(`product-${Date.now()}`, file);

  if (error) throw error;
  return data.publicUrl;
}

// Example usage with product creation
async function createProductWithImage(productData, imageFile) {
  // 1. Upload image first
  const imageUrl = await uploadProductImage(imageFile);
  
  // 2. Create product with image URL
  const product = await api.post('/api/products/', {
    ...productData,
    image_url: imageUrl
  });
  
  return product;
}
```

### Option 2: Direct API Upload
```javascript
async function uploadProductImage(productId, imageFile) {
  const formData = new FormData();
  formData.append('image', imageFile);

  const response = await fetch(`${BACKEND_URL}/api/products/${productId}/image/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${supabase.auth.session()?.access_token}`
    },
    body: formData
  });

  return response.json();
}
```

### Image Display
```javascript
// Component example
function ProductImage({ imageUrl }) {
  // Add error handling for broken images
  const [imgError, setImgError] = useState(false);

  return (
    <img
      src={imageUrl}
      onError={() => setImgError(true)}
      alt="Product"
      className="product-image"
      style={{ 
        width: '200px',
        height: '200px',
        objectFit: 'cover'
      }}
      // Fallback to placeholder if image fails to load
      {...(imgError && {
        src: '/placeholder-image.jpg'
      })}
    />
  );
}
```

### Best Practices for Product Images

1. **Image Optimization**
```javascript
// Using a library like sharp or browser-image-compression
async function optimizeImage(file) {
  const options = {
    maxSizeMB: 1,
    maxWidthOrHeight: 1024,
    useWebWorker: true
  };
  
  try {
    const compressedFile = await imageCompression(file, options);
    return compressedFile;
  } catch (error) {
    console.error('Error compressing image:', error);
    return file;
  }
}
```

2. **Image Validation**
```javascript
function validateImage(file) {
  // Check file type
  const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (!validTypes.includes(file.type)) {
    throw new Error('Invalid file type. Please use JPEG, PNG or WebP');
  }

  // Check file size (max 5MB)
  const maxSize = 5 * 1024 * 1024; // 5MB
  if (file.size > maxSize) {
    throw new Error('File too large. Maximum size is 5MB');
  }

  return true;
}
```

3. **Responsive Images**
```javascript
function ProductImage({ imageUrl }) {
  return (
    <picture>
      <source
        media="(min-width: 800px)"
        srcSet={`${imageUrl}?width=800`}
      />
      <source
        media="(min-width: 400px)"
        srcSet={`${imageUrl}?width=400`}
      />
      <img
        src={`${imageUrl}?width=200`}
        alt="Product"
        loading="lazy"
      />
    </picture>
  );
}
```

### Image Handling Implementation Details

#### Backend Endpoints for Images
```http
# Upload product image
POST /api/products/{id}/image/
Content-Type: multipart/form-data

# Get product image
GET /api/products/{id}/image/
```

#### Supabase Storage Configuration
```javascript
// Storage bucket configuration
const STORAGE_CONFIG = {
  BUCKET_NAME: 'products',
  MAX_FILE_SIZE: 5 * 1024 * 1024, // 5MB
  ALLOWED_MIME_TYPES: ['image/jpeg', 'image/png', 'image/webp'],
  IMAGE_SIZES: {
    thumbnail: 200,
    medium: 400,
    large: 800
  }
};

// Initialize storage
const productStorage = supabase.storage.from(STORAGE_CONFIG.BUCKET_NAME);
```

#### Complete Image Upload Implementation
```javascript
class ProductImageHandler {
  constructor(supabase) {
    this.storage = supabase.storage.from(STORAGE_CONFIG.BUCKET_NAME);
  }

  async uploadImage(file, productId) {
    try {
      // 1. Validate image
      this.validateImage(file);

      // 2. Optimize image before upload
      const optimizedFile = await this.optimizeImage(file);

      // 3. Generate unique filename
      const filename = this.generateFilename(productId, file.name);

      // 4. Upload to Supabase
      const { data, error } = await this.storage.upload(filename, optimizedFile, {
        cacheControl: '3600',
        upsert: true
      });

      if (error) throw error;

      // 5. Get public URL
      const { publicURL } = this.storage.getPublicUrl(filename);

      return {
        url: publicURL,
        filename: filename,
        size: optimizedFile.size,
        type: optimizedFile.type
      };

    } catch (error) {
      console.error('Image upload failed:', error);
      throw new Error('Failed to upload image');
    }
  }

  generateFilename(productId, originalName) {
    const extension = originalName.split('.').pop();
    return `${productId}-${Date.now()}.${extension}`;
  }

  // ... other methods from previous examples
}

// Usage in a React component
function ProductImageUploader({ productId }) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    try {
      const imageHandler = new ProductImageHandler(supabase);
      const result = await imageHandler.uploadImage(file, productId);
      
      // Update product with new image URL
      await api.patch(`/api/products/${productId}/`, {
        image_url: result.url
      });

      toast.success('Image uploaded successfully');
    } catch (error) {
      toast.error(error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept="image/jpeg,image/png,image/webp"
        onChange={handleImageUpload}
        disabled={uploading}
      />
      {uploading && <ProgressBar progress={progress} />}
    </div>
  );
}
```

#### Image Error Handling
```javascript
// Custom hook for image loading
function useImageLoader(imageUrl) {
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState(null);

  useEffect(() => {
    const img = new Image();
    
    img.onload = () => setStatus('loaded');
    img.onerror = () => {
      setStatus('error');
      setError('Failed to load image');
    };

    img.src = imageUrl;

    return () => {
      img.onload = null;
      img.onerror = null;
    };
  }, [imageUrl]);

  return { status, error };
}

// Usage in component
function ProductImage({ imageUrl }) {
  const { status, error } = useImageLoader(imageUrl);

  if (status === 'loading') {
    return <Skeleton width={200} height={200} />;
  }

  if (status === 'error') {
    return <FallbackImage />;
  }

  return (
    <picture>
      <source
        media="(min-width: 800px)"
        srcSet={`${imageUrl}?width=800`}
      />
      <source
        media="(min-width: 400px)"
        srcSet={`${imageUrl}?width=400`}
      />
      <img
        src={`${imageUrl}?width=200`}
        alt="Product"
        loading="lazy"
        className="product-image"
      />
    </picture>
  );
}
```

This implementation provides:
- Complete error handling
- Automatic image optimization
- Progressive loading
- Loading state management
- Responsive support
- Client-side validation

The frontend team can easily integrate this code and adapt it to their specific needs.
