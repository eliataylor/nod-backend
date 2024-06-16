
###OBJECT-ACTIONS-SERIALIZER-IMPORTS-STARTS###
from rest_framework import serializers
from .models import Customer
from .models import Supplier
from .models import Ingredient
from .models import Meal
from .models import Plan
from .models import OrderItem
from .models import Order
###OBJECT-ACTIONS-SERIALIZER-IMPORTS-ENDS###



###OBJECT-ACTIONS-SERIALIZERS-STARTS###
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        # exclude = ()  # Default: empty tuple, no fields excluded
        # depth = 0  # Default: 0, no nested serialization
        # read_only_fields = ()  # Default: empty tuple, no read-only fields
        # write_only_fields = ()  # Default: empty tuple, no write-only fields
        # extra_kwargs = {}  # Default: empty dictionary, no extra field configurations
        # validators = []  # Default: empty list, no validators defined
        # error_messages = {}  # Default: empty dictionary, no custom error messages

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        # exclude = ()  # Default: empty tuple, no fields excluded
        # depth = 0  # Default: 0, no nested serialization
        # read_only_fields = ()  # Default: empty tuple, no read-only fields
        # write_only_fields = ()  # Default: empty tuple, no write-only fields
        # extra_kwargs = {}  # Default: empty dictionary, no extra field configurations
        # validators = []  # Default: empty list, no validators defined
        # error_messages = {}  # Default: empty dictionary, no custom error messages

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        # exclude = ()  # Default: empty tuple, no fields excluded
        # depth = 0  # Default: 0, no nested serialization
        # read_only_fields = ()  # Default: empty tuple, no read-only fields
        # write_only_fields = ()  # Default: empty tuple, no write-only fields
        # extra_kwargs = {}  # Default: empty dictionary, no extra field configurations
        # validators = []  # Default: empty list, no validators defined
        # error_messages = {}  # Default: empty dictionary, no custom error messages

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'
        # exclude = ()  # Default: empty tuple, no fields excluded
        # depth = 0  # Default: 0, no nested serialization
        # read_only_fields = ()  # Default: empty tuple, no read-only fields
        # write_only_fields = ()  # Default: empty tuple, no write-only fields
        # extra_kwargs = {}  # Default: empty dictionary, no extra field configurations
        # validators = []  # Default: empty list, no validators defined
        # error_messages = {}  # Default: empty dictionary, no custom error messages

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
        # exclude = ()  # Default: empty tuple, no fields excluded
        # depth = 0  # Default: 0, no nested serialization
        # read_only_fields = ()  # Default: empty tuple, no read-only fields
        # write_only_fields = ()  # Default: empty tuple, no write-only fields
        # extra_kwargs = {}  # Default: empty dictionary, no extra field configurations
        # validators = []  # Default: empty list, no validators defined
        # error_messages = {}  # Default: empty dictionary, no custom error messages

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        # exclude = ()  # Default: empty tuple, no fields excluded
        # depth = 0  # Default: 0, no nested serialization
        # read_only_fields = ()  # Default: empty tuple, no read-only fields
        # write_only_fields = ()  # Default: empty tuple, no write-only fields
        # extra_kwargs = {}  # Default: empty dictionary, no extra field configurations
        # validators = []  # Default: empty list, no validators defined
        # error_messages = {}  # Default: empty dictionary, no custom error messages

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        # exclude = ()  # Default: empty tuple, no fields excluded
        # depth = 0  # Default: 0, no nested serialization
        # read_only_fields = ()  # Default: empty tuple, no read-only fields
        # write_only_fields = ()  # Default: empty tuple, no write-only fields
        # extra_kwargs = {}  # Default: empty dictionary, no extra field configurations
        # validators = []  # Default: empty list, no validators defined
        # error_messages = {}  # Default: empty dictionary, no custom error messages

###OBJECT-ACTIONS-SERIALIZERS-ENDS###








































































































































































