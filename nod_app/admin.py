####OBJECT-ACTIONS-ADMIN_IMPORTS-STARTS####
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Users
from .models import Suppliers
from .models import Ingredients
from .models import Tags
from .models import Meals
from .models import Plans
from .models import OrderItems
from .models import Orders
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

class SuppliersAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Suppliers, SuppliersAdmin)

class IngredientsAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Ingredients, IngredientsAdmin)

class TagsAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Tags, TagsAdmin)

class MealsAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Meals, MealsAdmin)

class PlansAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Plans, PlansAdmin)

class OrderItemsAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(OrderItems, OrderItemsAdmin)

class OrdersAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Orders, OrdersAdmin)
####OBJECT-ACTIONS-ADMIN_MODELS-ENDS####































