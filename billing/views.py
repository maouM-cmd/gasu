from django.shortcuts import render, redirect
from .models import Customer, MeterReading, Invoice
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import HttpResponse


def invoice_pdf(request, pk):
    invoice = Invoice.objects.filter(pk=pk).select_related('customer').first()
    if not invoice:
        return HttpResponse('Invoice not found', status=404)
    html = render_to_string('billing/invoice_pdf.html', {'invoice': invoice})
    try:
        from weasyprint import HTML
        pdf = HTML(string=html).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"invoice_{invoice.id}.pdf"
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response
    except Exception:
        # If WeasyPrint is not available or fails, return HTML for debugging
        return HttpResponse(html)


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
