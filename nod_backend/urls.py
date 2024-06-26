from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView

####OBJECT-ACTIONS-URL-IMPORTS-ENDS####



####OBJECT-ACTIONS-URLS-STARTS####

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("nod_app.urls"))
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

####OBJECT-ACTIONS-URLS-ENDS####