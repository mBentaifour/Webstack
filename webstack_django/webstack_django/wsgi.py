"""
WSGI config for webstack_django project.
"""

import os
from django.core.wsgi import get_wsgi_application
from django.urls import path
from django.http import HttpResponse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstack_django.settings')

def hello(request):
    return HttpResponse("""
        <html>
            <head>
                <title>Django sur Vercel</title>
                <style>
                    body { 
                        font-family: Arial, sans-serif;
                        margin: 40px;
                        line-height: 1.6;
                    }
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                    }
                    h1 { color: #333; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Bienvenue sur Django Vercel!</h1>
                    <p>Cette page confirme que votre application Django fonctionne correctement sur Vercel.</p>
                    <p>Heure du serveur: """ + str(os.environ.get('TZ', 'non définie')) + """</p>
                </div>
            </body>
        </html>
    """)

# Get the WSGI application
application = get_wsgi_application()

# Add URL pattern for the root path
from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Override the URL patterns
from django.conf.urls import url
settings.ROOT_URLCONF = __name__
urlpatterns = [
    path('', hello),
]
