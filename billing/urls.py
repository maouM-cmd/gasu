from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('meter/', views.meter_input, name='meter_input'),
    path('invoices/', views.invoice_list, name='invoice_list'),
]
