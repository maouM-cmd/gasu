from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    # Auth
    path('login/', LoginView.as_view(template_name='billing/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='billing:login'), name='logout'),
    # Billing views
    path('', views.customer_list, name='customer_list'),
    path('customer/new/', views.customer_create, name='customer_create'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('meter/', views.meter_input, name='meter_input'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('invoices/generate/', views.generate_invoices_view, name='generate_invoices'),
    path('invoices/clear_created/', views.clear_created_invoices, name='clear_created_invoices'),
]
