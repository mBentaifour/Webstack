# Documentation API Webstack

## Configuration du Frontend

### Configuration de Base
```javascript
const BACKEND_URL = 'http://localhost:8000';
const SUPABASE_URL = 'https://hbqpplveyaofcqtuippl.supabase.co';
const SUPABASE_KEY = 'votre_clé_supabase';
```

### Authentification
L'authentification est gérée via Supabase. Voici comment l'implémenter dans votre frontend :

```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// Connexion
async function signIn(email, password) {
  const { user, error } = await supabase.auth.signInWithPassword({
    email,
    password
  });
  return { user, error };
}

// Inscription
async function signUp(email, password) {
  const { user, error } = await supabase.auth.signUp({
    email,
    password
  });
  return { user, error };
}

// Déconnexion
async function signOut() {
  const { error } = await supabase.auth.signOut();
  return { error };
}
```

### Endpoints API

#### Produits

1. **Liste des produits**
```javascript
async function getProducts() {
  const response = await fetch(`${BACKEND_URL}/api/products/`, {
    headers: {
      'Authorization': `Bearer ${supabase.auth.session()?.access_token}`
    }
  });
  return response.json();
}
```

2. **Détail d'un produit**
```javascript
async function getProduct(productId) {
  const response = await fetch(`${BACKEND_URL}/api/products/${productId}/`, {
    headers: {
      'Authorization': `Bearer ${supabase.auth.session()?.access_token}`
    }
  });
  return response.json();
}
```

3. **Créer un produit**
```javascript
async function createProduct(productData) {
  const response = await fetch(`${BACKEND_URL}/api/products/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${supabase.auth.session()?.access_token}`
    },
    body: JSON.stringify(productData)
  });
  return response.json();
}
```

4. **Mettre à jour un produit**
```javascript
async function updateProduct(productId, productData) {
  const response = await fetch(`${BACKEND_URL}/api/products/${productId}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${supabase.auth.session()?.access_token}`
    },
    body: JSON.stringify(productData)
  });
  return response.json();
}
```

5. **Supprimer un produit**
```javascript
async function deleteProduct(productId) {
  const response = await fetch(`${BACKEND_URL}/api/products/${productId}/`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${supabase.auth.session()?.access_token}`
    }
  });
  return response.status === 204;
}
```

#### Commandes

1. **Liste des commandes**
```javascript
async function getOrders() {
  const response = await fetch(`${BACKEND_URL}/api/orders/`, {
    headers: {
      'Authorization': `Bearer ${supabase.auth.session()?.access_token}`
    }
  });
  return response.json();
}
```

2. **Détail d'une commande**
```javascript
async function getOrder(orderId) {
  const response = await fetch(`${BACKEND_URL}/api/orders/${orderId}/`, {
    headers: {
      'Authorization': `Bearer ${supabase.auth.session()?.access_token}`
    }
  });
  return response.json();
}
```

3. **Créer une commande**
```javascript
async function createOrder(orderData) {
  const response = await fetch(`${BACKEND_URL}/api/orders/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${supabase.auth.session()?.access_token}`
    },
    body: JSON.stringify(orderData)
  });
  return response.json();
}
```

### Gestion des Erreurs

```javascript
async function handleApiError(error) {
  if (error.status === 401) {
    // Token expiré ou invalide
    await signOut();
    window.location.href = '/login';
  } else if (error.status === 403) {
    // Accès non autorisé
    console.error('Accès non autorisé');
  } else if (error.status === 404) {
    // Ressource non trouvée
    console.error('Ressource non trouvée');
  } else {
    // Autre erreur
    console.error('Une erreur est survenue:', error);
  }
}
```

### Exemple d'Utilisation Complète

```javascript
// Configuration
const config = {
  backendUrl: 'http://localhost:8000',
  supabaseUrl: 'https://hbqpplveyaofcqtuippl.supabase.co',
  supabaseKey: 'votre_clé_supabase'
};

// Initialisation de Supabase
const supabase = createClient(config.supabaseUrl, config.supabaseKey);

// Classe API
class Api {
  constructor() {
    this.baseUrl = config.backendUrl;
  }

  async getHeaders() {
    const session = supabase.auth.session();
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

// Exemple d'utilisation
const api = new Api();

// Récupérer la liste des produits
async function displayProducts() {
  try {
    const products = await api.get('/api/products/');
    console.log('Produits:', products);
  } catch (error) {
    console.error('Erreur lors de la récupération des produits:', error);
  }
}

// Créer une commande
async function createNewOrder(orderData) {
  try {
    const order = await api.post('/api/orders/', orderData);
    console.log('Commande créée:', order);
  } catch (error) {
    console.error('Erreur lors de la création de la commande:', error);
  }
}
```
