from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.password_generator, name='password-generator'),
    path('strength/', views.password_strength, name='password-strength'),
]
