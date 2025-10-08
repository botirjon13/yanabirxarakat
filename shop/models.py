from django.db import models
from django.utils import timezone
from decimal import Decimal

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=64, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Sale(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Sale #{self.id} - {self.created_at.date()}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        # decrease stock before saving the sale item
        if self.pk is None:
            self.product.stock -= self.quantity
            if self.product.stock < 0:
                # allow negative stock but warn (business rule can be changed later)
                pass
            self.product.save()
        super().save(*args, **kwargs)
