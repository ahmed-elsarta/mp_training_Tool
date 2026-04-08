from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('language/<int:language_id>/pairs/', views.minimal_pairs_by_language, name='minimal_pairs_by_language'),
]