####OBJECT-ACTIONS-URL-IMPORTS-STARTS####
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet
from .views import IngredientViewSet
from .views import MealViewSet
from .views import OrderItemViewSet
from .views import OrderViewSet
from .views import PlanViewSet
from .views import SupplierViewSet
from .views import migrate, collectstatic

####OBJECT-ACTIONS-URL-IMPORTS-ENDS####



####OBJECT-ACTIONS-URLS-STARTS####

router = DefaultRouter()
router.register(r'api/customer', CustomerViewSet, basename='customer')
router.register(r'api/supplier', SupplierViewSet, basename='supplier')
router.register(r'api/ingredient', IngredientViewSet, basename='ingredient')
router.register(r'api/meal', MealViewSet, basename='meal')
router.register(r'api/plan', PlanViewSet, basename='plan')
router.register(r'api/order_item', OrderItemViewSet, basename='order_item')
router.register(r'api/order', OrderViewSet, basename='order')
urlpatterns = [
    path('migrate/', migrate, name='migrate'),
    path('collectstatic/', collectstatic, name='collectstatic'),
    path('', include(router.urls)),
]
####OBJECT-ACTIONS-URLS-ENDS####























































