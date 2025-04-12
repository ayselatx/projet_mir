from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),  # Home page
    path('indexation/', views.indexation, name="indexation"),  # Indexation page
    path('recherche/', views.recherche, name="recherche"),  # Recherche page
    path('api/on_top_changed/', views.on_top_changed, name='on_top_changed'),
    path('api/affiche_top/', views.affiche_top, name='affiche_top'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
