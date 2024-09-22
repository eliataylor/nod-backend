####OBJECT-ACTIONS-VIEWSET-IMPORTS-STARTS####
from rest_framework import viewsets, permissions, status, pagination
from django.http import JsonResponse
from django.core.management import call_command
from .models import Users
from .serializers import UsersSerializer
from .models import Suppliers
from .serializers import SuppliersSerializer
from .models import Ingredients
from .serializers import IngredientsSerializer
from .models import Tags
from .serializers import TagsSerializer
from .models import Meals
from .serializers import MealsSerializer
from .models import Plans
from .serializers import PlansSerializer
from .models import OrderItems
from .serializers import OrderItemsSerializer
from .models import Orders
from .serializers import OrdersSerializer
####OBJECT-ACTIONS-VIEWSET-IMPORTS-ENDS####

####OBJECT-ACTIONS-VIEWSETS-STARTS####
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Users.objects.all()
        title = self.request.query_params.get('id', None)
        if title is not None:
            queryset = queryset.filter(id__icontains=title)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = UsersSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)
class SuppliersViewSet(viewsets.ModelViewSet):
    queryset = Suppliers.objects.all()
    serializer_class = SuppliersSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Suppliers.objects.all()
        title = self.request.query_params.get('name', None)
        if title is not None:
            queryset = queryset.filter(name__icontains=title)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = SuppliersSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)
class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Ingredients.objects.all()
        title = self.request.query_params.get('name', None)
        if title is not None:
            queryset = queryset.filter(name__icontains=title)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = IngredientsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)
class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Tags.objects.all()
        title = self.request.query_params.get('name', None)
        if title is not None:
            queryset = queryset.filter(name__icontains=title)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = TagsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)
class MealsViewSet(viewsets.ModelViewSet):
    queryset = Meals.objects.all()
    serializer_class = MealsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Meals.objects.all()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = MealsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)
class PlansViewSet(viewsets.ModelViewSet):
    queryset = Plans.objects.all()
    serializer_class = PlansSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Plans.objects.all()
        title = self.request.query_params.get('name', None)
        if title is not None:
            queryset = queryset.filter(name__icontains=title)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = PlansSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)
class OrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = OrderItems.objects.all()
        title = self.request.query_params.get('id', None)
        if title is not None:
            queryset = queryset.filter(id__icontains=title)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = OrderItemsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Orders.objects.all()
        title = self.request.query_params.get('id', None)
        if title is not None:
            queryset = queryset.filter(id__icontains=title)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = OrdersSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)
####OBJECT-ACTIONS-VIEWSETS-ENDS####


####OBJECT-ACTIONS-CORE-STARTS####
def migrate(request):
    call_command('migrate')
    return JsonResponse({'status': 'migrations complete'})

def collectstatic(request):
    call_command('collectstatic', '--noinput')
    return JsonResponse({'status': 'static files collected'})
####OBJECT-ACTIONS-CORE-ENDS####




































