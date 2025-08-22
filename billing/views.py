from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse
import uuid
import requests
from .models import Payment


from .models import Invoice
from .forms import InvoiceForm

# Optional helper function (add this to a utils file or your User model as a property)
def is_doctor(user):
    return hasattr(user, 'doctor_profile')

def is_patient(user):
    return hasattr(user, 'patient_profile')

# ----------------------
# Billing Views
# ----------------------

@login_required
def patient_billing(request):
    if not is_patient(request.user):
        raise PermissionDenied
    invoices = Invoice.objects.filter(patient__user=request.user)
    return render(request, 'billing/patient_billing.html', {'invoices': invoices})


@login_required
def doctor_billing(request):
    if not is_doctor(request.user):
        raise PermissionDenied
    invoices = Invoice.objects.filter(doctor__user=request.user)
    return render(request, 'billing/doctor_billing.html', {'invoices': invoices})


@login_required
def admin_billing(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    invoices = Invoice.objects.all()
    return render(request, 'billing/admin_billing.html', {'invoices': invoices})


@login_required
def create_invoice(request):
    # Allow only superusers or doctors
    if not (request.user.is_superuser or is_doctor(request.user)):
        raise PermissionDenied

    if request.method == 'POST':
        form = InvoiceForm(request.POST, user=request.user)
        if form.is_valid():
            invoice = form.save(commit=False)
            if is_doctor(request.user):
                invoice.doctor = request.user.doctor_profile
            invoice.save()
            messages.success(request, f"Invoice #{invoice.id} created successfully.")
            return redirect('doctor-billing' if is_doctor(request.user) else 'admin-billing')
    else:
        form = InvoiceForm(user=request.user)

    return render(request, 'billing/create_invoice.html', {'form': form})


@staff_member_required
@require_POST
def mark_invoice_paid(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.is_paid = True
    invoice.save()
    messages.success(request, f"Invoice #{invoice.id} marked as paid.")
    return redirect('admin-billing')