"""
URL configuration for PSiM_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
   openapi.Info(
      title="API projektu PSiM",  # Tytuł dokumentacji API.
      default_version='v1',  # Domyślna wersja API.
      description="Dokumentacja API dla projektu PSiM",  # Opis API.
   ),
   public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),  # Ścieżka do panelu administracyjnego Django.
    path('', include('backend.urls')),  # Dodanie do głównego pliku konfiguracyjnego ścieżki do pliku konfiguracyjnego aplikacji backend.
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Ścieżka do interfejsu użytkownika Swagger dla dokumentacji API.
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # Ścieżka do interfejsu użytkownika ReDoc dla dokumentacji API.
]
