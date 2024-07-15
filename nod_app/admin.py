####OBJECT-ACTIONS-ADMIN_IMPORTS-STARTS####
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Users
from .models import Supplier
from .models import Ingredient
from .models import Meal
from .models import Plan
from .models import OrderItem
from .models import Order
####OBJECT-ACTIONS-ADMIN_IMPORTS-ENDS####



####OBJECT-ACTIONS-ADMIN_MODELS-STARTS####
class UsersAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Additional Info'), {'fields': ('phone', 'billing_name', 'billing_address', 'delivery_address')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'billing_name', 'billing_address', 'delivery_address'),
        }),
    )                


admin.site.register(Users, UsersAdmin)

class SupplierAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Supplier, SupplierAdmin)

class IngredientAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Ingredient, IngredientAdmin)

class MealAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Meal, MealAdmin)

class PlanAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Plan, PlanAdmin)

class OrderItemAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(OrderItem, OrderItemAdmin)

class OrderAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Order, OrderAdmin)
####OBJECT-ACTIONS-ADMIN_MODELS-ENDS####



