"""
WSGI config for webstack_django project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstack_django.settings')

application = get_wsgi_application()
