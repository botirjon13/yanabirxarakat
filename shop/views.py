from django.shortcuts import render, redirect
from .models import Product, Sale, SaleItem
from decimal import Decimal
from django.http import HttpResponse

def dashboard(request):
    products = Product.objects.all()
    sales = Sale.objects.prefetch_related('items__product').order_by('-created_at')[:20]
    return render(request, 'shop/dashboard.html', {'products': products, 'sales': sales})

def create_sale(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_id')
        qtys = request.POST.getlist('qty')
        sale = Sale.objects.create(total=Decimal('0.00'))
        total = Decimal('0.00')
        for pid, q in zip(product_ids, qtys):
            if not pid or not q:
                continue
            p = Product.objects.get(pk=int(pid))
            qn = int(q)
            SaleItem.objects.create(sale=sale, product=p, quantity=qn, price=p.price)
            total += p.price * qn
        sale.total = total
        sale.save()
    return redirect('dashboard')

def sales_report_csv(request):
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Sale ID','Date','Total','Items'])
    for s in Sale.objects.all().order_by('-created_at'):
        items = '; '.join([f"{it.product.name} x{it.quantity}" for it in s.items.all()])
        writer.writerow([s.id, s.created_at.isoformat(), s.total, items])
    return response
