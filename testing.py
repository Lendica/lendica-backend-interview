from django.utils import timezone
import datetime
from models import *
from implementation import *

# Create test data
company = Company.objects.create(
    name="Test Company",
    bank_routing='123456789',
    bank_account='987654321'
)
loan = Loan.objects.create(
    company=company,
    amount=10000.00,
    term_days=90,
    status="active"
)
payment_schedule = PaymentSchedule.objects.create(
    loan=loan,
    amount=1000.00,
    scheduled_date=timezone.now().date() + datetime.timedelta(days=30),
    status="scheduled"
)

# Test payment submission
result = submit_payment_to_ach_provider(payment_schedule.id)
print(result)

# Test reconciliation
result = reconcile_ach_payment_statuses()
print(result)
