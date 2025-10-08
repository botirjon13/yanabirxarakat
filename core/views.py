from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def create_sale(request):
    return render(request, 'create_sale.html')

from django.http import HttpResponse
import csv

def sales_report_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Mahsulot', 'Soni', 'Narxi'])
    writer.writerow(['Olma', 10, 5000])
    writer.writerow(['Nok', 5, 8000])
    return response
