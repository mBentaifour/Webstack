"""
WSGI config for webstack_django project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstack_django.settings')

def application(environ, start_response):
    if environ['PATH_INFO'] == '/':
        status = '200 OK'
        response_headers = [('Content-type', 'text/html')]
        start_response(status, response_headers)
        return [b"""
            <html>
                <head>
                    <title>Test Django on Vercel</title>
                    <style>
                        body { 
                            font-family: Arial, sans-serif;
                            margin: 40px;
                            line-height: 1.6;
                            background: #f0f2f5;
                        }
                        .container {
                            max-width: 800px;
                            margin: 0 auto;
                            padding: 20px;
                            background: white;
                            border-radius: 8px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }
                        h1 { 
                            color: #1a73e8;
                            margin-bottom: 20px;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Django est en ligne sur Vercel !</h1>
                        <p>Cette page confirme que l'application fonctionne correctement.</p>
                        <p>Path: /</p>
                        <p>Time: """ + str(environ.get('REQUEST_TIME', 'unknown')).encode() + b"""</p>
                    </div>
                </body>
            </html>
        """]
    
    django_app = get_wsgi_application()
    return django_app(environ, start_response)
