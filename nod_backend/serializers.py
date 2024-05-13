from rest_framework import serializers
from .models import *

class MealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'