
from django.test import TestCase
from .models import Product, Sale, SaleItem
from decimal import Decimal

class InventoryMovementTests(TestCase):
    def test_saleitem_reduces_inventory(self):
        p = Product.objects.create(name='Orange', price=Decimal('70.00'), stock=30)
        sale = Sale.objects.create(total=Decimal('0.00'))
        SaleItem.objects.create(sale=sale, product=p, quantity=2, price=p.price)
        p.refresh_from_db()
        self.assertEqual(p.stock, 28)

    def test_multiple_saleitems_reduce_inventory(self):
        p = Product.objects.create(name='Grapes', price=Decimal('20.00'), stock=10)
        sale = Sale.objects.create(total=Decimal('0.00'))
        SaleItem.objects.create(sale=sale, product=p, quantity=2, price=p.price)
        SaleItem.objects.create(sale=sale, product=p, quantity=1, price=p.price)
        p.refresh_from_db()
        self.assertEqual(p.stock, 7)
