from django.urls import path
from . import views

# Define URL patterns for the car inquiry
urlpatterns = [
    path('inquiry', views.inquiry, name='inquiry'),
]
