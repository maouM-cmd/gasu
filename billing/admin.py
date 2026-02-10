from django.contrib import admin
from .models import Customer, MeterReading, Invoice, Payment

admin.site.register(Customer)
admin.site.register(MeterReading)
admin.site.register(Invoice)
admin.site.register(Payment)
