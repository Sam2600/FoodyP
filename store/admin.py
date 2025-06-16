from django.contrib import admin
# Register your models here.
from django.contrib import admin
from .models import Item, Order, Category, OrderItem

# CATEGORY ADMIN
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# ITEM ADMIN
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'created_by', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

# INLINE ORDER ITEMS FOR ORDER ADMIN
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('name', 'description', 'price', 'quantity', 'category', 'image_url', 'sub_total')
    extra = 0

# ORDER ADMIN
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'total_amount', 'summary')
    search_fields = ('summary',)
    ordering = ('-created_at',)
    list_per_page = 20
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'name', 'quantity', 'price', 'sub_total')
    search_fields = ('name', 'order__id')
    list_filter = ('category',)
    ordering = ('-id',)
