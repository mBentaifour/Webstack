from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Django sur Vercel</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: #f0f2f5;
            }
            .container {
                background: white;
                padding: 2rem;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                text-align: center;
                max-width: 600px;
                width: 90%;
            }
            h1 {
                color: #1a73e8;
                margin-bottom: 1rem;
            }
            p {
                color: #5f6368;
                line-height: 1.5;
            }
            .success-icon {
                font-size: 48px;
                margin-bottom: 1rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success-icon">✅</div>
            <h1>Application Django en ligne!</h1>
            <p>Votre application Django fonctionne correctement sur Vercel.</p>
            <p>Vous pouvez maintenant commencer à ajouter vos propres fonctionnalités.</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
