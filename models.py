# models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    bank_routing = models.CharField(max_length=500, blank=True, null=True)
    bank_account = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term_days = models.IntegerField()
    status = models.CharField(max_length=20, default="active")# active, completed, defaulted
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan {self.id} - {self.company.name}"

class PaymentSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    scheduled_date = models.DateField()
    status = models.CharField(max_length=20, default="scheduled")# scheduled, processing, completed, failed

    def __str__(self):
        return f"Payment Schedule {self.id} - {self.scheduled_date}"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_schedule = models.ForeignKey(PaymentSchedule, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")# pending, processing, completed, failed, returned
    ach_provider_reference_id = models.CharField(max_length=255, null=True, blank=True)
    ach_trace_number = models.CharField(max_length=255, null=True, blank=True)
    ach_status_code = models.CharField(max_length=10, null=True, blank=True)# R01, R02, etc.
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"