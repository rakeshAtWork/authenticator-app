from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(openapi.Info(title="Auth API", default_version='v1'))

urlpatterns = [
    path('api/', include('authentication.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]
