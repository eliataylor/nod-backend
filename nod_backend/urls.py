from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

####OBJECT-ACTIONS-URL-IMPORTS-ENDS####



####OBJECT-ACTIONS-URLS-STARTS####

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("nod_app.urls")),
    path('auth/', include("users.urls", namespace="users")),
    path('accounts/', include('allauth.urls'))
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

####OBJECT-ACTIONS-URLS-ENDS####


urlpatterns += [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
