from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    plan_basic_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    plan_unit_price = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    tax_rate = models.DecimalField(max_digits=4, decimal_places=2, default=10.0)
    contract_start = models.DateField(null=True, blank=True)
    contract_end = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class MeterReading(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.customer} @ {self.date}: {self.value}"


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.id} - {self.customer} - {self.amount}"


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.id} - {self.amount}"
