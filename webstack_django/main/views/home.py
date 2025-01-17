from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

def home(request):
    """Vue de la page d'accueil"""
    return render(request, 'home.html', {
        'debug': settings.DEBUG
    })
