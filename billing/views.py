from django.shortcuts import render, redirect
from .models import Customer, MeterReading, Invoice
from django.utils import timezone


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'billing/customer_list.html', {'customers': customers})


def meter_input(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        value = request.POST.get('value')
        date = request.POST.get('date') or timezone.now().date()
        if customer_id and value:
            MeterReading.objects.create(customer_id=customer_id, value=value, date=date)
            return redirect('billing:meter_input')
    customers = Customer.objects.all()
    return render(request, 'billing/meter_input.html', {'customers': customers})


def invoice_list(request):
    invoices = Invoice.objects.order_by('-date').all()
    return render(request, 'billing/invoice_list.html', {'invoices': invoices})
