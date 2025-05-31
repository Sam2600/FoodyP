from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Item, Order, Category

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Category)