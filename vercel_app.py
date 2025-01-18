import os
import sys
from pathlib import Path

# Add the project root to the Python path
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(path, 'webstack_django'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstack_django.settings')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
