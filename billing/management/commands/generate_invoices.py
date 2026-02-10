from django.core.management.base import BaseCommand
from billing.utils import generate_invoices_for_all


class Command(BaseCommand):
    help = 'Generate invoices from meter readings (uses latest and previous readings per customer)'

    def handle(self, *args, **options):
        created = generate_invoices_for_all()
        self.stdout.write(self.style.SUCCESS(f'Created {len(created)} invoice(s).'))
