from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from rest_framework.schemas import get_schema_view

"""
schema_view = get_schema_view(
    title="NOD API",
    description="API",
    version="1.0.0"
)
"""

urlpatterns = [
    path("admin/", admin.site.urls),
# path('schema/', schema_view),
    path('', include("nod_app.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
