"""
WSGI config for webstack_django project.
"""

import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstack_django.vercel_settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application
