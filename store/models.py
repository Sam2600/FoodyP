# Create your models here.
from decimal import Decimal
from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

class Category(models.Model):
   name = models.CharField(max_length=100, unique=True)

   def __str__(self):
      return self.name

class Item(models.Model):
   name = models.CharField(max_length=100)
   description = models.TextField()
   price = models.DecimalField(max_digits=8, decimal_places=2)
   category = models.ForeignKey(Category, on_delete=models.CASCADE)
   image = models.ImageField(upload_to='items/', null=True, blank=True)
   created_by = models.ForeignKey(User, on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.name

class Order(models.Model):
   summary = models.TextField(default="")  # e.g., "2 Banana ($36), 1 Apple ($30)"
   total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f"Order #{self.id} - {self.created_at.strftime('%Y-%m-%d')} - ${self.total_amount}"


class OrderItem(models.Model):
   order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
   name = models.CharField(max_length=255)
   description = models.TextField(blank=True)
   price = models.DecimalField(max_digits=10, decimal_places=2)
   quantity = models.PositiveIntegerField()
   category = models.CharField(max_length=100)
   image_url = models.URLField(blank=True)
   sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

   def save(self, *args, **kwargs):
       self.sub_total = Decimal(self.price) * self.quantity
       super().save(*args, **kwargs)

   def __str__(self):
      return f"{self.name} (x{self.quantity})"