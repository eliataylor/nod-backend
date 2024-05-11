from django.urls import include, path
from .views import *
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from django.contrib import admin

router = DefaultRouter()
router.register(r'meals', MealsViewSet, basename='meals')

#health check function
def respond(request):
    return HttpResponse("Status OK")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', respond),
    path('health/', respond),
    # path('login/', login, name='login')

]

urlpatterns.extend(router.urls)
