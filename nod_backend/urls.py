from .views import *
from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.urls import include, path
from django.contrib import admin

router = DefaultRouter()
router.register(r'menu', MealsViewSet, basename='meals')
router.register(r'plans', PlanViewSet)
# router.register(r'orders', PlanViewSet)
# router.register(r'supplier', PlanViewSet)
# router.register(r'ingredient', PlanViewSet)
# router.register(r'meal', PlanViewSet)
# router.register(r'menu', PlanViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.extend(router.urls)
