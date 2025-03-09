"""
URL configuration for quantumfold project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from quantumfold.apps.web import views

urlpatterns = [
    path('', views.home, name='home'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("visualizer", views.visualizer, name="visualizer"),
    path("protein_search", views.protein_search, name="protein_search"),
    path("protein_folding/<str:uniprot_accession>", views.protein_folding, name="protein_folding"),
    path("personalized_compare", views.personalized_compare, name="personalized_compare"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
