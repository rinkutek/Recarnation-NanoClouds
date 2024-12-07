from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),  # URL for the login page, linked to the `login` view.
    path('register', views.register, name='register'),  # URL for the registration page, linked to the `register` view.
    path('logout', views.logout, name='logout'),  # URL for logging out, linked to the `logout` view.
    path('dashboard', views.dashboard, name='dashboard'),  # URL for the user dashboard, linked to the `dashboard` view.
]
