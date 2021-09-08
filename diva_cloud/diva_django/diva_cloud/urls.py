from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view

router = routers.DefaultRouter()

urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('fileapp.urls')),
    path('', include('jobapp.urls')),
    path('api-auth', include('rest_framework.urls')),
    path('openapi', get_schema_view(
        title="Diva Django",
        description="API for DIVA",
        version="0.3.0"
    ), name='openapi-schema'),
    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
