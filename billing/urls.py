from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('customer/new/', views.customer_create, name='customer_create'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('meter/', views.meter_input, name='meter_input'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
]
