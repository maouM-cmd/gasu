from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from billing.models import Customer, MeterReading, Invoice
from django.core.management import call_command


class GenerateEdgecasesTest(TestCase):
    def test_same_date_multiple_readings_uses_latest(self):
        c = Customer.objects.create(name='同日検針', plan_basic_fee=100, plan_unit_price=10, tax_rate=10)
        # two readings on same date, second should be used as 'current'
        MeterReading.objects.create(customer=c, date=timezone.datetime(2024,1,1).date(), value=Decimal('50'))
        MeterReading.objects.create(customer=c, date=timezone.datetime(2024,1,1).date(), value=Decimal('70'))
        MeterReading.objects.create(customer=c, date=timezone.datetime(2024,2,1).date(), value=Decimal('90'))
        call_command('generate_invoices')
        inv = Invoice.objects.filter(customer=c).first()
        # usage = 90 - 70 = 20 => subtotal = 100 + 10*20 = 300, tax 10% =30 total=330
        self.assertEqual(inv.amount, Decimal('330'))

    def test_negative_usage_is_skipped(self):
        c = Customer.objects.create(name='逆転', plan_basic_fee=100, plan_unit_price=10, tax_rate=10)
        MeterReading.objects.create(customer=c, date=timezone.datetime(2024,1,1).date(), value=Decimal('200'))
        MeterReading.objects.create(customer=c, date=timezone.datetime(2024,2,1).date(), value=Decimal('150'))
        call_command('generate_invoices')
        invs = Invoice.objects.filter(customer=c)
        self.assertEqual(invs.count(), 0)
