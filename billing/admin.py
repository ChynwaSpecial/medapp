from django.contrib import admin
from .models import Invoice, Payment

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'total_amount', 'due_date', 'is_paid']
    list_filter = ['is_paid', 'due_date']
    search_fields = ['patient__user__username', 'doctor__user__username']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'amount', 'paid_on', 'method']
    list_filter = ['method', 'paid_on']