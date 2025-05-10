from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from mozilla_django_oidc import views as oidc_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site for managing the application.
    path('', include('pages.urls')),  # Root URL is routed to the 'pages' app.
    path('cars/', include('cars.urls')),  # Handles URLs related to the 'cars' app.
    path('accounts/', include('accounts.urls')),  # User account management, e.g., login, signup.
    path("authorization-code/authenticate/", oidc_views.OIDCAuthenticationRequestView.as_view(), name="oidc_authentication_init"),
    path("authorization-code/callback/", oidc_views.OIDCAuthenticationCallbackView.as_view(), name="oidc_authentication_callback"),
    path('oidc/callback/', oidc_views.OIDCAuthenticationCallbackView.as_view(), name='oidc_callback'),
    path('accounts/social/login/google/', include('allauth.urls'), name='google_login'),  
    # Integrates Google login via Django Allauth.
    path('contacts/', include('contacts.urls')),  # Routes URLs for contact-related functionality.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
# Serves uploaded media files in development mode.
