

import re

from address.models import AddressField
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
####OBJECT-ACTIONS-MODEL_IMPORTS-STARTS####
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from djmoney.models.fields import MoneyField

from users.models import User


####OBJECT-ACTIONS-MODEL_IMPORTS-ENDS####

####OBJECT-ACTIONS-PRE-HELPERS-STARTS####

def validate_phone_number(value):
                        phone_regex = re.compile(r'^\+?1?\d{9,15}$')
                        if not phone_regex.match(value):
                            raise ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
####OBJECT-ACTIONS-PRE-HELPERS-ENDS####



####OBJECT-ACTIONS-MODELS-STARTS####

def validate_phone_number(value):
	phone_regex = re.compile(r'^\+?1?\d{9,15}$')
	if not phone_regex.match(value):
		raise ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class SuperModel(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
	class Meta:
		abstract = True
	def __str__(self):
		if hasattr(self, "title"):
			return self.title
		elif hasattr(self, "name"):
			return self.name
		return self.__class__
	@classmethod
	def get_current_user(cls, request):
		if hasattr(request, 'user') and request.user.is_authenticated:
			return request.user
		return None

class Customer(User):
	class Meta:
		abstract = False

	id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(get_user_model(),  on_delete=models.CASCADE,  related_name='+', blank=True, null=True)
	phone = models.CharField(validators=[validate_phone_number], max_length=16)
	email = models.EmailField()
	billing_name = models.CharField(max_length=255, blank=True, null=True)
	billing_address = AddressField(related_name='+', blank=True, null=True)
	delivery_address = AddressField(related_name='+', blank=True, null=True)

class CustomerAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Customer, CustomerAdmin)


class Supplier(SuperModel):
	class Meta:
		abstract = False
	def save(self, *args, **kwargs):
		if not self.id:
			self.id = slugify(self.name)
		super().save(*args, **kwargs)
	id = models.SlugField(primary_key=True, unique=True, editable=False)
	name = models.CharField(max_length=255)
	photo = models.ImageField(upload_to='media/suppliers', blank=True, null=True)
	address = AddressField(related_name='+', blank=True, null=True)
	website = models.URLField(blank=True, null=True)

class SupplierAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Supplier, SupplierAdmin)


class Ingredient(SuperModel):
	class Meta:
		abstract = False
	def save(self, *args, **kwargs):
		if not self.id:
			self.id = slugify(self.title)
		super().save(*args, **kwargs)
	id = models.SlugField(primary_key=True, unique=True, editable=False)
	title = models.CharField(max_length=255)
	image = models.ImageField(upload_to='media/ingredients', blank=True, null=True)
	supplier = models.OneToOneField('Supplier',  on_delete=models.CASCADE, blank=True, null=True)
	seasonal = models.BooleanField(blank=True, null=True)
	in_season_price = models.DecimalField(max_digits=10,  decimal_places=2, blank=True, null=True)
	out_of_season_price = models.DecimalField(max_digits=10,  decimal_places=2, blank=True, null=True)

class IngredientAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Ingredient, IngredientAdmin)


class Meal(SuperModel):
	class Meta:
		abstract = False
	def save(self, *args, **kwargs):
		if not self.id:
			self.id = slugify(self.title)
		super().save(*args, **kwargs)
	
	class BldChoices(models.TextChoices):
		breakfast = ("Breakfast", "breakfast")
		lunch = ("Lunch", "lunch")
		dinner = ("Dinner", "dinner")
		desert = ("Desert", "desert")
		snack = ("Snack", "snack")
	id = models.SlugField(primary_key=True, unique=True, editable=False)
	title = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	bld = models.CharField(max_length=20, choices=BldChoices.choices)
	photo = models.FileField(upload_to='media/calendar', blank=True, null=True)
	internal_cost = models.DecimalField(max_digits=10,  decimal_places=2, blank=True, null=True)
	public_price = models.DecimalField(max_digits=10,   decimal_places=2,  default=16, blank=True, null=True)
	ingredients = models.ManyToManyField('Ingredient', blank=True)
	suppliers = models.ManyToManyField('Supplier', blank=True)

class MealAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Meal, MealAdmin)


class Plan(SuperModel):
	class Meta:
		abstract = False
	def save(self, *args, **kwargs):
		if not self.id:
			self.id = slugify(self.name)
		super().save(*args, **kwargs)
	id = models.SlugField(primary_key=True, unique=True, editable=False)
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	meals = models.ManyToManyField('Meal')
	MoneyField(decimal_places=2, default_currency='USD', max_digits=11)
	date = models.DateField(blank=True, null=True)

class PlanAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Plan, PlanAdmin)


class OrderItem(SuperModel):
	class Meta:
		abstract = False

	id = models.AutoField(primary_key=True)
	date = models.DateField()
	delivery_date = models.DateField()
	meal = models.OneToOneField('Meal',  on_delete=models.CASCADE, blank=True, null=True)
	meal_menu = models.OneToOneField('Plan',  on_delete=models.CASCADE, blank=True, null=True)
	servings = models.IntegerField(default=1)

class OrderItemAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(OrderItem, OrderItemAdmin)


class Order(SuperModel):
	class Meta:
		abstract = False
	
	class StatusChoices(models.TextChoices):
		paid = ("Paid", "paid")
		cancelled = ("Cancelled", "cancelled")
		unpaid = ("Unpaid", "unpaid")
	id = models.AutoField(primary_key=True)
	customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='+')
	created_date = models.DateField()
	start_date = models.DateField()
	final_price = models.DecimalField(max_digits=10, decimal_places=2)
	delivery_instructions = models.TextField(blank=True, null=True)
	customizations = models.TextField()
	glass_containers = models.BooleanField(default="0", blank=True, null=True)
	recurring = models.BooleanField(default="0", blank=True, null=True)
	order_items = models.ManyToManyField('OrderItem')
	status = models.CharField(max_length=20,  choices=StatusChoices.choices, default="unpaid")

class OrderAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(Order, OrderAdmin)

####OBJECT-ACTIONS-MODELS-ENDS####



####OBJECT-ACTIONS-POST-HELPERS-STARTS####

@receiver(pre_save, sender=Supplier)
def generate_slug_supplier_id(sender, instance, **kwargs):
    if not instance.id:
        instance.id = slugify(instance.name)


@receiver(pre_save, sender=Ingredient)
def generate_slug_ingredient_id(sender, instance, **kwargs):
    if not instance.id:
        instance.id = slugify(instance.title)


@receiver(pre_save, sender=Meal)
def generate_slug_meal_id(sender, instance, **kwargs):
    if not instance.id:
        instance.id = slugify(instance.title)


@receiver(pre_save, sender=Plan)
def generate_slug_plan_id(sender, instance, **kwargs):
    if not instance.id:
        instance.id = slugify(instance.name)

####OBJECT-ACTIONS-POST-HELPERS-ENDS####



















































































































