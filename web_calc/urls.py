from django.urls import path
from .views import AgeCalculatorView

urlpatterns = [
    path("age/", AgeCalculatorView.as_view(), name="age_calculator"),
]


