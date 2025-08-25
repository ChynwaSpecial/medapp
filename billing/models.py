from django.db import models
from django.conf import settings
from django.utils import timezone
from patients.models import PatientProfile
from doctors.models import DoctorProfile

class Invoice(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    paid_on = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)


    class Meta:
        ordering = ['-issued_date']

    def __str__(self):
        return f"Invoice #{self.id} for {self.patient.user.get_full_name()}"

    @property
    def amount_paid(self):
        return sum(payment.amount for payment in self.payments.all())

    @property
    def balance_due(self):
        return self.total_amount - self.amount_paid

    @property
    def status(self):
        if self.is_paid:
            return "Paid"
        elif timezone.now().date() > self.due_date:
            return "Overdue"
        elif self.amount_paid > 0:
            return "Partially Paid"
        else:
            return "Unpaid"

    def update_payment_status(self):
        self.is_paid = self.amount_paid >= self.total_amount
        self.save()


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField(auto_now_add=True)
    method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
    ])

    class Meta:
        ordering = ['-paid_on']

    def __str__(self):
        return f"Payment #{self.id} - {self.amount} for Invoice #{self.invoice.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invoice.update_payment_status()
     
        
