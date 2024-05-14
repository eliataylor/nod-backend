from django.contrib import admin

from .models import Customer, Plan, Order, Supplier, Ingredient, Meal, DayMenu

admin.site.register(Customer)
admin.site.register(Plan)
admin.site.register(Order)
admin.site.register(Supplier)
admin.site.register(Ingredient)
admin.site.register(Meal)
admin.site.register(DayMenu)