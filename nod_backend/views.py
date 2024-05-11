import logging
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import *

logger = logging.getLogger('django')


class MealsViewSet(viewsets.ModelViewSet):
    serializer_class = MealsSerializer

    # permission_classes = [IsAuthenticated, HasGroupPermission]
    @method_decorator(cache_page(60 * 3))
    def list(self, request):
        return Response({
            "rows": ["test"]
        })
