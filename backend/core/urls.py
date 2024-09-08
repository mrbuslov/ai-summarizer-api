from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="PDF Summarization API",
        default_version='v1',
        description="API to upload a 1-page PDF and get a summarized version using OpenAI.",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="example@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('api/', include('text_processor.urls')),
]
