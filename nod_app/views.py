####OBJECT-ACTIONS-VIEWSET-IMPORTS-STARTS####
from rest_framework import viewsets, permissions, status, pagination
from django.http import JsonResponse
from django.core.management import call_command
from .models import Users
from .serializers import UsersSerializer
from .models import Supplier
from .serializers import SupplierSerializer
from .models import Ingredient
from .serializers import IngredientSerializer
from .models import Meal
from .serializers import MealSerializer
from .models import Plan
from .serializers import PlanSerializer
from .models import OrderItem
from .serializers import OrderItemSerializer
from .models import Order
from .serializers import OrderSerializer
####OBJECT-ACTIONS-VIEWSET-IMPORTS-ENDS####


####OBJECT-ACTIONS-VIEWSETS-STARTS####
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
####OBJECT-ACTIONS-VIEWSETS-ENDS####


####OBJECT-ACTIONS-CORE-STARTS####
def migrate(request):
    call_command('migrate')
    return JsonResponse({'status': 'migrations complete'})

def collectstatic(request):
    call_command('collectstatic', '--noinput')
    return JsonResponse({'status': 'static files collected'})
####OBJECT-ACTIONS-CORE-ENDS####



