"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from user_center import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('register/', views.register),
    path('register_handle/', views.register_handle),
    path('register_username_check/', views.register_username_check),
    path('register_email_check/', views.register_email_check),
    path('verify_mail/', views.verify_mail)
]
