from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Customer, MeterReading, Invoice
from django.utils import timezone
from .forms import CustomerForm
from django.contrib import messages
from .utils import generate_invoices_for_all
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse


@login_required
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


@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'billing/customer_list.html', {'customers': customers})


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('billing:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'billing/customer_form.html', {'form': form, 'title': '新規顧客登録'})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('billing:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'billing/customer_form.html', {'form': form, 'title': '顧客編集'})


@login_required
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


@login_required
def invoice_list(request):
    invoices = Invoice.objects.order_by('-date').all()
    return render(request, 'billing/invoice_list.html', {'invoices': invoices})


@login_required
def generate_invoices_view(request):
    if request.method != 'POST':
        return redirect('billing:invoice_list')
    created = generate_invoices_for_all()
    ids = [str(i.id) for i in created]
    if ids:
        # store IDs in session so UI can show a modal with details
        request.session['created_invoice_ids'] = ids
        messages.success(request, f'作成された請求: {len(created)} 件')
        messages.info(request, '作成された請求IDが表示されます')
    else:
        messages.info(request, '新しい請求は作成されませんでした')
    return redirect('billing:invoice_list')


@login_required
def clear_created_invoices(request):
    if request.method == 'POST':
        request.session.pop('created_invoice_ids', None)
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)
