from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),  # Home page
    path('indexation/', views.indexation, name="indexation"),  # Indexation page
    path('recherche/', views.recherche, name="recherche"),  # Recherche page
]
