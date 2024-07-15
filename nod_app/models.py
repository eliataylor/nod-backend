

####OBJECT-ACTIONS-MODELS_IMPORTS-STARTS####
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from utils.models import BumpParentsModelMixin
from allauth.account.models import EmailAddress
from django.dispatch import receiver
from allauth.account.signals import email_confirmed
from django.utils.timezone import now
from django.core.exceptions import ValidationError
import re
from django.utils.text import slugify
from djmoney.models.fields import MoneyField
####OBJECT-ACTIONS-MODELS_IMPORTS-ENDS####

def generate_slug(title, max_length=50):
    slug = slugify(title)
    if len(slug) <= max_length:
        return slug

    words = slug.split('-')
    truncated_slug = ''
    for word in words:
        if len(truncated_slug) + len(word) + 1 > max_length:  # +1 for the hyphen
            break
        if truncated_slug:
            truncated_slug += '-'
        truncated_slug += word

    return truncated_slug

####OBJECT-ACTIONS-MODELS-STARTS####
def validate_phone_number(value):
	phone_regex = re.compile(r'^\+?1?\d{9,15}$')
	if not phone_regex.match(value):
		raise ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Users(AbstractUser, BumpParentsModelMixin):
	class Meta:
		verbose_name = "Customers"
		verbose_name_plural = "Customers"
		ordering = ['last_login']

	phone = models.CharField(validators=[validate_phone_number], max_length=16, verbose_name='Phone')
	billing_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Billing Name')
	billing_address = models.CharField(max_length=255)
	delivery_address = models.CharField(max_length=255)

	def __str__(self):
		if self.get_full_name().strip():
			return self.get_full_name()
		elif self.get_short_name().strip():
			return self.get_short_name()
		else:
			return str(self.id) # never expose the email

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

	def add_email_address(self, request, new_email):
		# Add a new email address for the user, and send email confirmation.
		# Old email will remain the primary until the new one is confirmed.
		return EmailAddress.objects.add_email(request, request.user, new_email, confirm=True)


	@receiver(email_confirmed)
	def update_user_email(sender, request, email_address, **kwargs):
		# Once the email address is confirmed, make new email_address primary.
		# This also sets user.email to the new email address.
		# email_address is an instance of allauth.account.models.EmailAddress
		email_address.set_as_primary()
		# Get rid of old email addresses
		EmailAddress.objects.filter(user=email_address.user).exclude(primary=True).delete()

class SuperModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
	class Meta:
		abstract = True
		ordering = ['modified_at']

	def save(self, *args, **kwargs):
		self.modified_at = now()
		super().save(*args, **kwargs)

	def __str__(self):
		if hasattr(self, "title"):
			return self.title
		elif hasattr(self, "name"):
			return self.name
		elif hasattr(self, "slug"):
			return self.slug

		return super().__str__()

	@classmethod
	def get_current_user(cls, request):
		if hasattr(request, 'user') and request.user.is_authenticated:
			return request.user
		return None

class Supplier(SuperModel):
	class Meta:
		abstract = False
		verbose_name = "Supplier"
		verbose_name_plural = "Suppliers"
	
	def save(self, *args, **kwargs):
		if 'name' in kwargs:
			self.name = kwargs.pop('name')

		base_slug = slugify(self.name)
		slug = base_slug
		count = 1

		while Supplier.objects.filter(url_alias=slug).exclude(id=self.id).exists():
			slug = f"{base_slug}-{count}"
			count += 1
		self.url_alias = slug

		super().save(*args, **kwargs)

	url_alias = models.SlugField(unique=True, default="name", blank=True, null=True, verbose_name='URL Alias')
	name = models.CharField(max_length=255, verbose_name='Name')
	photo = models.ImageField(upload_to='media/suppliers', blank=True, null=True, verbose_name='Photo')
	address = models.CharField(max_length=255)
	website = models.URLField(blank=True, null=True, verbose_name='Website')

class Ingredient(SuperModel):
	class Meta:
		abstract = False
		verbose_name = "Ingredient"
		verbose_name_plural = "Ingredients"
	
	def save(self, *args, **kwargs):
		if 'name' in kwargs:
			self.name = kwargs.pop('name')

		base_slug = slugify(self.name)
		slug = base_slug
		count = 1

		while Ingredient.objects.filter(id=slug).exclude(id=self.id).exists():
			slug = f"{base_slug}-{count}"
			count += 1
		self.id = slug

		super().save(*args, **kwargs)

	id = models.SlugField(primary_key=True, unique=True, editable=False)
	name = models.CharField(max_length=255, verbose_name='Name')
	image = models.ImageField(upload_to='media/ingredients', blank=True, null=True, verbose_name='Image')
	supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, related_name='+', null=True, blank=True, verbose_name='Supplier')
	seasonal = models.BooleanField(blank=True, null=True, verbose_name='Seasonal')
	in_season_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='In season Price')
	out_of_season_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Out of season price')

class Meal(SuperModel):
	class Meta:
		abstract = False
		verbose_name = "Meal"
		verbose_name_plural = "Meals"
	
	def save(self, *args, **kwargs):
		if 'title' in kwargs:
			self.title = kwargs.pop('title')

		base_slug = generate_slug(self.title)
		slug = base_slug
		count = 1

		while Meal.objects.filter(id=slug).exclude(id=self.id).exists():
			slug = f"{base_slug}-{count}"
			count += 1
		self.id = slug

		super().save(*args, **kwargs)

	
	class BldChoices(models.TextChoices):
		breakfast = ("breakfast", "Breakfast")
		lunch = ("lunch", "Lunch")
		dinner = ("dinner", "Dinner")
		desert = ("desert", "Desert")
		snack = ("snack", "Snack")
	id = models.SlugField(primary_key=True, unique=True, editable=False)
	title = models.CharField(max_length=255, verbose_name='Title')
	description = models.CharField(max_length=255, verbose_name='Description')
	bld = models.CharField(max_length=20, choices=BldChoices.choices, verbose_name='BLD')
	photo = models.FileField(upload_to='media/calendar', blank=True, null=True, verbose_name='Photo')
	internal_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Internal Cost')
	public_price = models.DecimalField(max_digits=10, decimal_places=2, default=16, blank=True, null=True, verbose_name='Public Price')
	ingredients = models.ForeignKey('Ingredient', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ingredients')
	suppliers = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Suppliers')

class Plan(SuperModel):
	class Meta:
		abstract = False
		verbose_name = "Plan"
		verbose_name_plural = "Plans"
	
	def save(self, *args, **kwargs):
		if 'name' in kwargs:
			self.name = kwargs.pop('name')

		base_slug = slugify(self.name)
		slug = base_slug
		count = 1

		while Plan.objects.filter(id=slug).exclude(id=self.id).exists():
			slug = f"{base_slug}-{count}"
			count += 1
		self.id = slug

		super().save(*args, **kwargs)

	id = models.SlugField(primary_key=True, unique=True, editable=False)
	name = models.CharField(max_length=255, verbose_name='Name')
	description = models.TextField(blank=True, null=True, verbose_name='Description')
	meals = models.ForeignKey('Meal', on_delete=models.SET_NULL, null=True, verbose_name='Meals')
	MoneyField(decimal_places=2, default_currency='USD', max_digits=11, verbose_name='Price')
	date = models.DateField(blank=True, null=True, verbose_name='Date')

class OrderItem(SuperModel):
	class Meta:
		abstract = False
		verbose_name = "Order Item"
		verbose_name_plural = "Order Items"

	id = models.AutoField(primary_key=True)
	date = models.DateField(verbose_name='Date')
	delivery_date = models.DateField(verbose_name='Delivery Date')
	meal = models.ForeignKey('Meal', on_delete=models.SET_NULL, related_name='+', null=True, blank=True, verbose_name='Meal')
	meal_menu = models.ForeignKey('Plan', on_delete=models.SET_NULL, related_name='+', null=True, blank=True, verbose_name='Meal Menu')
	servings = models.IntegerField(default=1, verbose_name='Servings')

class Order(SuperModel):
	class Meta:
		abstract = False
		verbose_name = "Order"
		verbose_name_plural = "Orders"
	
	class StatusChoices(models.TextChoices):
		paid = ("paid", "Paid")
		cancelled = ("cancelled", "Cancelled")
		unpaid = ("unpaid", "Unpaid")
	id = models.AutoField(primary_key=True)
	customer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='+', null=True, verbose_name='Customer')
	created_date = models.DateField(verbose_name='Created Date')
	start_date = models.DateField(verbose_name='Start Date')
	final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Final Price')
	delivery_instructions = models.TextField(blank=True, null=True, verbose_name='Delivery Instructions')
	customizations = models.TextField(verbose_name='Customizations')
	glass_containers = models.BooleanField(default="0", blank=True, null=True, verbose_name='Glass Containers')
	recurring = models.BooleanField(default="0", blank=True, null=True, verbose_name='Recurring')
	order_items = models.ForeignKey('OrderItem', on_delete=models.SET_NULL, null=True, verbose_name='Order Items')
	status = models.CharField(max_length=20, choices=StatusChoices.choices, verbose_name='Status', default="unpaid")
####OBJECT-ACTIONS-MODELS-ENDS####

