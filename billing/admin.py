from django.contrib import admin
from .models import Customer, MeterReading, Invoice, Payment

admin.site.register(Customer)
admin.site.register(MeterReading)
admin.site.register(Invoice)
admin.site.register(Payment)

from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
	list_display = ('created_at', 'action_type', 'actor', 'target_table', 'target_id')
	readonly_fields = ('created_at',)
