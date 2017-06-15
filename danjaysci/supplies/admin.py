from django.contrib import admin
from .models import Vendor, WebAccount, Quote, SupplyCategory, Item, Order, ItemPrice, LineItem, ItemRequest

# Define Inlines
class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 3

# Customize admin pages
class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['placed_by', 'date_ordered', 'vendor', 'charge_to', 'order_method', 'invoice_number', 'shipping_cost']}),
        ('Receipt', {'fields': ['received_by', 'date_received']}),
        
    ]
    inlines = [LineItemInline]

# Register your models here.
admin.register(
    Vendor,
    WebAccount,
    Quote,
    SupplyCategory,
    Item,
    ItemPrice,
    LineItem,
    ItemRequest)(admin.ModelAdmin)

admin.site.register(Order, OrderAdmin)
