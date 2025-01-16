# Frontend Implementation Guide

## Pages Structure

```
/                       # Home page
├── auth/
│   ├── login          # Login page
│   ├── register       # Registration page
│   ├── profile        # User profile
│   └── reset-password # Password reset
├── shop/
│   ├── products       # Products list
│   ├── product/:id    # Product details
│   ├── category/:id   # Category products
│   ├── brand/:id      # Brand products
│   └── search         # Search results
├── cart/
│   ├── view           # Shopping cart
│   └── checkout       # Checkout process
└── account/
    ├── orders         # Order history
    ├── order/:id      # Order details
    ├── settings       # Account settings
    └── addresses      # Shipping addresses
```

## Required Features

### 1. Authentication Pages

#### Login Page (`/auth/login`)
- Email/Password login form
- "Remember me" option
- Forgot password link
- Register link
- Social login buttons (if implemented)

```javascript
// Example login form
const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/auth/login/', { email, password });
      const { token, user } = response.data;
      // Store token and redirect
    } catch (error) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Login</button>
    </form>
  );
};
```

#### Register Page (`/auth/register`)
- Registration form with:
  - Email
  - Password
  - Confirm password
  - First name
  - Last name
  - Phone (optional)
- Terms and conditions checkbox
- Privacy policy checkbox

### 2. Shop Pages

#### Products List Page (`/shop/products`)
Features:
- Product grid/list view toggle
- Filtering sidebar:
  - Categories
  - Brands
  - Price range
  - Availability
- Sorting options:
  - Price (low to high)
  - Price (high to low)
  - Newest first
  - Most popular
- Pagination
- Quick view modal

```javascript
// Example products fetch
const ProductsList = () => {
  const [products, setProducts] = useState([]);
  const [filters, setFilters] = useState({
    category: null,
    brand: null,
    minPrice: 0,
    maxPrice: 1000,
    inStock: true
  });

  useEffect(() => {
    const fetchProducts = async () => {
      const queryString = new URLSearchParams(filters).toString();
      const response = await api.get(`/products/?${queryString}`);
      setProducts(response.data.results);
    };
    fetchProducts();
  }, [filters]);

  return (
    <div className="products-grid">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
};
```

#### Product Details Page (`/shop/product/:id`)
Features:
- Image gallery
- Product information:
  - Name
  - Price
  - Description
  - Specifications
- Stock status
- Add to cart button
- Quantity selector
- Related products
- Reviews section

### 3. Cart & Checkout

#### Cart Page (`/cart/view`)
Features:
- Product list with:
  - Image
  - Name
  - Price
  - Quantity selector
  - Remove button
- Cart summary:
  - Subtotal
  - Tax
  - Shipping cost
  - Total
- Proceed to checkout button
- Continue shopping link

#### Checkout Page (`/cart/checkout`)
Steps:
1. Shipping address
2. Billing address
3. Shipping method
4. Payment method
5. Order review

```javascript
// Example checkout process
const Checkout = () => {
  const [step, setStep] = useState(1);
  const [orderData, setOrderData] = useState({
    shipping_address: {},
    billing_address: {},
    payment_method: null
  });

  const handlePayment = async () => {
    try {
      // 1. Create order
      const order = await api.post('/orders/', orderData);
      
      // 2. Initialize payment
      const { client_secret } = await api.post(
        `/orders/${order.id}/process_payment/`
      );
      
      // 3. Confirm payment with Stripe
      const { paymentIntent } = await stripe.confirmCardPayment(
        client_secret,
        { payment_method: { card: elements.getElement('card') } }
      );
      
      // 4. Confirm on backend
      await api.post(`/orders/${order.id}/confirm_payment/`, {
        payment_intent_id: paymentIntent.id
      });
      
      // 5. Redirect to success page
      router.push(`/account/order/${order.id}`);
    } catch (error) {
      // Handle error
    }
  };

  return (
    <div className="checkout">
      <CheckoutSteps currentStep={step} />
      {step === 1 && <ShippingForm onSubmit={handleShippingSubmit} />}
      {step === 2 && <BillingForm onSubmit={handleBillingSubmit} />}
      {step === 3 && <PaymentForm onSubmit={handlePayment} />}
    </div>
  );
};
```

### 4. Account Pages

#### Order History (`/account/orders`)
Features:
- List of all orders with:
  - Order number
  - Date
  - Status
  - Total
  - View details button
- Filtering by status
- Search by order number

#### Order Details (`/account/order/:id`)
Features:
- Order summary
- Payment information
- Shipping details
- Order status timeline
- Reorder button
- Download invoice

## Components Library

Suggested reusable components:
- `<ProductCard />`
- `<AddToCartButton />`
- `<QuantitySelector />`
- `<PriceDisplay />`
- `<RatingStars />`
- `<Pagination />`
- `<FiltersSidebar />`
- `<SortDropdown />`
- `<AddressForm />`
- `<PaymentForm />`

## State Management

Recommended structure:
```javascript
const initialState = {
  auth: {
    user: null,
    token: null,
    isAuthenticated: false
  },
  cart: {
    items: [],
    total: 0,
    quantity: 0
  },
  ui: {
    theme: 'light',
    currency: 'EUR',
    loading: false
  }
};
```

## API Integration

Create an API client:
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add auth token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 responses
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response.status === 401) {
      // Redirect to login
      router.push('/auth/login');
    }
    return Promise.reject(error);
  }
);
```

## Error Handling

Create a global error handler:
```javascript
const ErrorBoundary = ({ children }) => {
  const [error, setError] = useState(null);

  useEffect(() => {
    const handleError = (error) => {
      setError(error);
      // Log error to service
      logger.error(error);
    };

    window.addEventListener('error', handleError);
    return () => window.removeEventListener('error', handleError);
  }, []);

  if (error) {
    return <ErrorPage error={error} />;
  }

  return children;
};
```

## Loading States

Use a global loading indicator:
```javascript
const LoadingProvider = ({ children }) => {
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.interceptors.request.use(config => {
      setLoading(true);
      return config;
    });

    api.interceptors.response.use(
      response => {
        setLoading(false);
        return response;
      },
      error => {
        setLoading(false);
        return Promise.reject(error);
      }
    );
  }, []);

  return (
    <>
      {loading && <LoadingSpinner />}
      {children}
    </>
  );
};
```

## Recommended Libraries

1. State Management:
   - Redux Toolkit
   - React Query

2. Forms:
   - Formik
   - React Hook Form

3. Validation:
   - Yup
   - Zod

4. UI Components:
   - Material-UI
   - Tailwind CSS
   - Chakra UI

5. Payment:
   - Stripe Elements

6. Routing:
   - React Router
   - Next.js Router

## Security Considerations

1. XSS Prevention:
   - Sanitize user input
   - Use React's built-in XSS protection
   - Implement CSP headers

2. CSRF Protection:
   - Include CSRF token in requests
   - Validate token on backend

3. Secure Storage:
   - Use HttpOnly cookies for tokens
   - Don't store sensitive data in localStorage

4. Input Validation:
   - Validate on both client and server
   - Use strong validation schemas

## Performance Optimization

1. Code Splitting:
```javascript
const ProductDetails = React.lazy(() => import('./ProductDetails'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <ProductDetails />
    </Suspense>
  );
}
```

2. Image Optimization:
```javascript
const ProductImage = ({ src, alt }) => (
  <img
    src={src}
    alt={alt}
    loading="lazy"
    srcSet={`${src} 1x, ${src.replace('.jpg', '@2x.jpg')} 2x`}
  />
);
```

3. Caching:
```javascript
const { data: products } = useQuery(['products'], fetchProducts, {
  staleTime: 5 * 60 * 1000, // 5 minutes
  cacheTime: 30 * 60 * 1000 // 30 minutes
});
```
