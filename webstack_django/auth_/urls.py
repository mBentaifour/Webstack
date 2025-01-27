"""
URL configuration for my_p project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urlsignins import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from . import views
from django.urls import path
from .views import signin_view, signup_view, check_email, google_oauth, x_oauth, bing_oauth, retrieve_session


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),
    path('email_used_check/', check_email, name='checkEmail'),
    path('google_signin/', google_oauth, name='signin'),
    path('google_signup/', google_oauth, name='signin'),
    path('check_session/', signin_view, name='signin'),
    path('retreivesession/', retrieve_session, name='signin'),
]
