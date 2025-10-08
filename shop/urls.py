
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sale/create/', views.create_sale, name='create_sale'),
    path('report/sales/', views.sales_report_csv, name='sales_report_csv'),
]
