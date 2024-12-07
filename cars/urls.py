from django.urls import path
from . import views

# Define URL patterns for the 'cars' app
urlpatterns = [
    path('', views.cars, name='cars'),    # URL pattern for the main cars listing page
    path('<int:id>', views.car_detail, name='car_detail'), # URL pattern for car detail page
    path('search', views.search, name='search'), # URL pattern for the search page

]
