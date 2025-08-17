from django.urls import path
from .views import assign_topics

urlpatterns = [
    path('assign/', assign_topics, name='assign-topics'),
]
