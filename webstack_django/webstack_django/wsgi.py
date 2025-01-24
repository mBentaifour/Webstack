"""
WSGI config for webstack_django project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'webstack_django.settings'
os.environ['DEBUG'] = 'True'

application = get_wsgi_application()
