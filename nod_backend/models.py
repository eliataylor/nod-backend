from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.TextField()
    billing_name = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=2555)
    delivery_name = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=2555)

    def __str__(self):
        return self.user.username

class Plan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_date = models.DateField()
    start_date = models.DateField()
    customizations = models.CharField(max_length=255)
    glass_containers = models.BooleanField()
    order_items = models.JSONField()


class Order(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    recurring = models.BooleanField()
    delivery_instructions = models.TextField()


class Suppliers(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField()
    address = models.CharField(max_length=2555)
    website = models.URLField()


class Ingredients(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField()
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    seasonal = models.BooleanField()
    in_season_price = models.DecimalField(max_digits=10, decimal_places=2)
    out_of_season_price = models.DecimalField(max_digits=10, decimal_places=2)


class Meal(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    bld = models.TextField()
    photo = models.FileField(upload_to='media/')
    internal_cost = models.DecimalField(max_digits=10, decimal_places=2)
    public_price = models.DecimalField(max_digits=10, decimal_places=2)
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    suppliers = models.ForeignKey(Suppliers, on_delete=models.CASCADE)


class Menu(models.Model):
    date = models.DateField()
    breakfast = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='breakfast_menu')
    lunch = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='lunch_menu')
    dinner = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='dinner_menu')
