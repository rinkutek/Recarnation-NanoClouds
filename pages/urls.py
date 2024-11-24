from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('sell', views.sell, name='sell'),
    path('contact', views.contact, name='contact'),
    path('edit_car/<int:car_id>/', views.edit_car, name='edit_car'),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),  # Delete car page
    path('add_car', views.add_car, name='add_car')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Edit car page