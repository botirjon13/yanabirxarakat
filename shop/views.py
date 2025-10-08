
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Sale, SaleItem, Product
import csv
from decimal import Decimal

def dashboard(request):
    products = Product.objects.all()
    sales = Sale.objects.prefetch_related('items__product').order_by('-created_at')[:20]
    return render(request, 'shop/dashboard.html', {'sales': sales, 'products': products})

def create_sale(request):
    if request.method == 'POST':
        # Expect form fields: product_id[], qty[]
        product_ids = request.POST.getlist('product_id')
        qtys = request.POST.getlist('qty')
        total = Decimal('0.00')
        sale = Sale.objects.create(total=Decimal('0.00'))
        for pid, q in zip(product_ids, qtys):
            if not pid or not q:
                continue
            p = Product.objects.get(pk=int(pid))
            qn = int(q)
            price = p.price
            SaleItem.objects.create(sale=sale, product=p, quantity=qn, price=price)
            total += price * qn
        sale.total = total
        sale.save()
        return redirect(reverse('dashboard'))
    return redirect('dashboard')

def sales_report_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Sale ID', 'Date', 'Total', 'Items'])
    for s in Sale.objects.all().order_by('-created_at'):
        items = '; '.join([f"{it.product.name} x{it.quantity}" for it in s.items.all()])
        writer.writerow([s.id, s.created_at.isoformat(), s.total, items])
    return response
