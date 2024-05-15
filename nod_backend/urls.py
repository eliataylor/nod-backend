from .views import *
from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.urls import include, path
from django.contrib import admin

###OBJECT-ACTIONS-URLS-STARTS###
router = DefaultRouter()
router.register(r'api/customer', CustomerViewSet, basename='customer')
router.register(r'api/supplier', SupplierViewSet, basename='supplier')
router.register(r'api/ingredient', IngredientViewSet, basename='ingredient')
router.register(r'api/meal', MealViewSet, basename='meal')
router.register(r'api/order_items', OrderItemsViewSet, basename='order_items')
router.register(r'api/plan', PlanViewSet, basename='plan')
router.register(r'api/order', OrderViewSet, basename='order')

###OBJECT-ACTIONS-URLS-ENDS###

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
