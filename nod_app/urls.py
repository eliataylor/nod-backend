####OBJECT-ACTIONS-URL-IMPORTS-STARTS####
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import migrate, collectstatic
from .views import UsersViewSet
from .views import SuppliersViewSet
from .views import IngredientsViewSet
from .views import TagsViewSet
from .views import MealsViewSet
from .views import PlansViewSet
from .views import OrderItemsViewSet
from .views import OrdersViewSet
####OBJECT-ACTIONS-URL-IMPORTS-ENDS####



####OBJECT-ACTIONS-URLS-STARTS####
router = DefaultRouter()
router.register(r'api/users', UsersViewSet, basename='users')
router.register(r'api/suppliers', SuppliersViewSet, basename='suppliers')
router.register(r'api/ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'api/tags', TagsViewSet, basename='tags')
router.register(r'api/meals', MealsViewSet, basename='meals')
router.register(r'api/plans', PlansViewSet, basename='plans')
router.register(r'api/order_items', OrderItemsViewSet, basename='order_items')
router.register(r'api/orders', OrdersViewSet, basename='orders')
urlpatterns = [
    path('migrate/', migrate, name='migrate'),
    path('collectstatic/', collectstatic, name='collectstatic'),
    path('', include(router.urls)),
]
####OBJECT-ACTIONS-URLS-ENDS####























































































