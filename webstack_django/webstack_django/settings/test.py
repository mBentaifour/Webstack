from ..settings import *
import os
from dotenv import load_dotenv

# Charger les variables d'environnement de test
load_dotenv(os.path.join(BASE_DIR, '.env.test'))

# Configuration de la base de données de test
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}

# Configuration de l'API Gateway et Supabase pour les tests
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL', 'http://localhost:8000/api')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Configuration du runner de test
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Désactiver le cache pendant les tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Configurer le mode DEBUG pour les tests
DEBUG = True

# Configurer les clés secrètes pour les tests
SECRET_KEY = 'test-secret-key'
STRIPE_SECRET_KEY = os.getenv('STRIPE_TEST_SECRET_KEY', 'sk_test_your_stripe_key')

# Configuration des médias pour les tests
MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')
MEDIA_URL = '/test-media/'

# Configuration des fichiers statiques pour les tests
STATIC_ROOT = os.path.join(BASE_DIR, 'test_static')
STATIC_URL = '/test-static/'

# Désactiver les middlewares non nécessaires pour les tests
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Configuration de l'email pour les tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Configuration de la journalisation pour les tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
