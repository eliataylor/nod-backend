from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

####OBJECT-ACTIONS-URL-IMPORTS-ENDS####



####OBJECT-ACTIONS-URLS-STARTS####

schema_view = get_schema_view(
    openapi.Info(
        title="Nod Backend APIs",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("nod_app.urls")),
    path('auth/', include("users.urls", namespace="users")),
    path('accounts/', include('allauth.urls')),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

####OBJECT-ACTIONS-URLS-ENDS####