from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from .models import Invoice

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED:
        try:
            invoice_id = int(ipn.invoice)
            invoice = Invoice.objects.get(id=invoice_id)
            invoice.is_paid = True
            invoice.paid_on = ipn.payment_date
            invoice.payment_method = "PayPal"
            invoice.transaction_id = ipn.txn_id
            invoice.save()
        except Invoice.DoesNotExist:
            pass
