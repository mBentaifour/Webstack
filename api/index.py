from webstack_django.webstack_django.wsgi import application

# Vercel serverless function handler
def handler(request, response):
    return application(request, response)
