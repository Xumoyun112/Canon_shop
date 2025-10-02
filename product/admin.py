from django.contrib import admin
from .models import Product, Supplier, Sale, Speska

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "price", "stock", "supplier", "created_at", "total_value")
    list_filter = ("supplier", "created_at")
    search_fields = ("name",)
    ordering = ("-created_at",)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("speska", "quantity", "price", "created_at", "description")
    list_filter = ("created_at",)
    search_fields = ("speska",)
    ordering = ("-created_at",)

@admin.register(Speska)
class SpeskaAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date")
    list_filter = ("id",)
    search_fields = ("date",)

