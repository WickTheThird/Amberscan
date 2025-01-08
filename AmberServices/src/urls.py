from django.urls import path, re_path
from django.urls import path
from django.utils.text import slugify

from .views import LogIn, RegisterClient, Images, PDFs, Logout, Permissions
from .models import Providers

# Base urlpatterns
urlpatterns = [
    path('login/', LogIn.as_view(), name='login'),
    path('register/', RegisterClient.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('images/', Images.as_view(), name='images'),
    path('pdfs/', PDFs.as_view(), name='pdfs'),
    path("permissions/", Permissions.as_view(), name="permissions"),
]

def get_dynamic_routes():
    dynamic_routes = []
    try:
        PROV = Providers.objects.filter(is_active=True)
        for provider in PROV:
            signature = provider.signature
            dynamic_routes.extend([
                path(f'{signature}/logout/', Logout.as_view(), name=f'{signature}_logout'),
                path(f'{signature}/upload_image/', Images.as_view(), name=f'{signature}_upload_image'),
                path(f'{signature}/upload_pdf/', PDFs.as_view(), name=f'{signature}_upload_pdf'),
            ])
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error generating dynamic routes: {e}")
    return dynamic_routes


urlpatterns += get_dynamic_routes()
