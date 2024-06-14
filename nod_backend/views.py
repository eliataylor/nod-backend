

















import logging
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from .models import Customer, Plan, Order, Supplier, Ingredient, Meal, OrderItem

logger = logging.getLogger('django')

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default number of results per page
    page_size_query_param = 'page_size'  #
    max_page_size = 100  # Maximum number of results per page


###OBJECT-ACTIONS-VIEWSETS-STARTS###


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Add pagination
    pagination_class = CustomPagination

    def get_queryset(self):
        return Customer.objects.all()

    @action(detail=True, methods=['get'])
    @method_decorator(cache_page(60 * 3))
    def custom_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Add error handling for specific methods
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Add pagination
    pagination_class = CustomPagination

    def get_queryset(self):
        return Supplier.objects.all()

    @action(detail=True, methods=['get'])
    @method_decorator(cache_page(60 * 3))
    def custom_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Add error handling for specific methods
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Add pagination
    pagination_class = CustomPagination

    def get_queryset(self):
        return Ingredient.objects.all()

    @action(detail=True, methods=['get'])
    @method_decorator(cache_page(60 * 3))
    def custom_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Add error handling for specific methods
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Add pagination
    pagination_class = CustomPagination

    def get_queryset(self):
        return Meal.objects.all()

    @action(detail=True, methods=['get'])
    @method_decorator(cache_page(60 * 3))
    def custom_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Add error handling for specific methods
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Add pagination
    pagination_class = CustomPagination

    def get_queryset(self):
        return Plan.objects.all()

    @action(detail=True, methods=['get'])
    @method_decorator(cache_page(60 * 3))
    def custom_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Add error handling for specific methods
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Add pagination
    pagination_class = CustomPagination

    def get_queryset(self):
        return OrderItem.objects.all()

    @action(detail=True, methods=['get'])
    @method_decorator(cache_page(60 * 3))
    def custom_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Add error handling for specific methods
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Add pagination
    pagination_class = CustomPagination

    def get_queryset(self):
        return Order.objects.all()

    @action(detail=True, methods=['get'])
    @method_decorator(cache_page(60 * 3))
    def custom_list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Add error handling for specific methods
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

###OBJECT-ACTIONS-VIEWSETS-ENDS###

















