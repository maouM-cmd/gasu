from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from django.core.management import call_command
from billing.models import Customer, MeterReading, Invoice


class GenerateInvoicesIntegrationTest(TestCase):
    def test_generate_invoices_creates_invoice_from_readings(self):
        c = Customer.objects.create(name='テスト顧客', plan_basic_fee=500, plan_unit_price=50, tax_rate=10)
        # previous
        MeterReading.objects.create(customer=c, date=timezone.datetime(2024, 1, 1).date(), value=Decimal('100'))
        # current
        MeterReading.objects.create(customer=c, date=timezone.datetime(2024, 2, 1).date(), value=Decimal('120'))
        # Run management command
        call_command('generate_invoices')
        invs = Invoice.objects.filter(customer=c)
        self.assertEqual(invs.count(), 1)
        inv = invs.first()
        # usage = 20, subtotal = 500 + 50*20 = 1500, tax 10% = 150, total 1650
        self.assertEqual(inv.amount, Decimal('1650'))
