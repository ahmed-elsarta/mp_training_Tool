from django.urls import path
from . import views

app_name = 'practice'

urlpatterns = [
    path('<int:mp_id>/', views.session, name='session'),
    path('save-score/', views.save_score, name='save_score'),
    path('results/', views.results, name='results'),
]