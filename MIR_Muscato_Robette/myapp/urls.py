from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view
from .views import signup_view

urlpatterns = [
    path('', views.home, name="home"),  # Home page
    path('accounts/login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('get_races/', views.get_races, name='get_races'),
    path('get_images/', views.get_images, name='get_images'),
    path('indexation/', views.indexation, name="indexation"),  # Indexation page
    path('recherche/', views.recherche, name="recherche"),  # Recherche page
    path('api/on_top_changed/', views.on_top_changed, name='on_top_changed'),
    path('api/affiche_top/', views.affiche_top, name='affiche_top'),
    path('charger_descripteurs/', views.charger_descripteurs, name='charger_descripteurs'),
    path('api/affiche_distance/', views.affiche_distance, name='affiche_distance'),
    path('recherche_images/', views.recherche_images, name='recherche_images'),
    path('get_images_in_dataset/', views.get_images_in_dataset, name='get_images_in_dataset'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
