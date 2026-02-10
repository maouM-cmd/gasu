from django.core.management.base import BaseCommand
from billing.models import Customer, MeterReading
from django.utils import timezone
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create demo customers and a meter reading'

    def handle(self, *args, **options):
        c1, created = Customer.objects.get_or_create(
            name='山田 太郎',
            defaults={'plan_basic_fee': 500, 'plan_unit_price': 50, 'tax_rate': 10}
        )
        c2, _ = Customer.objects.get_or_create(
            name='鈴木 花子',
            defaults={'plan_basic_fee': 700, 'plan_unit_price': 45, 'tax_rate': 10}
        )
        MeterReading.objects.create(customer=c1, date=timezone.now().date(), value=Decimal('123.45'))
        self.stdout.write(self.style.SUCCESS('Demo customers and reading created.'))
