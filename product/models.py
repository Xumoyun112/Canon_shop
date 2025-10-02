from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone

User = get_user_model()

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50, default="dona")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_value(self):
        return self.price * self.stock

    def __str__(self):
        return self.name

class Speska(models.Model):
    id = models.AutoField(primary_key=True)  # avtomatik ortib boradi
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)  # faqat sana
    created_at = models.DateTimeField(auto_now_add=True)
    is_finalized = models.BooleanField(default=False)  # 🔑 saqlangandan keyin bloklanadi


    def total_sum(self):
        return self.sales.aggregate(
            total=Sum(models.F("quantity") * models.F("price"))
        )["total"] or Decimal("0.00")

    def __str__(self):
        return f"Speska #{self.id} - {self.created_at.strftime('%Y-%m-%d')}"

class Sale(models.Model):
    speska = models.ForeignKey("Speska", on_delete=models.CASCADE, related_name="sales")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.product.stock < self.quantity:
                raise ValueError("Skladda yetarli mahsulot yo‘q!")
            self.product.stock -= self.quantity
            self.product.save()
            self.price = self.product.price
            # self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity} dona"
