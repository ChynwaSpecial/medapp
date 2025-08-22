from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import MedicalReport
from .forms import MedicalReportForm
from django.core.exceptions import PermissionDenied
from django.http import Http404, FileResponse
import os

# Utility for admin-only access
def is_admin(user):
    return user.is_superuser or user.role == 'admin'

# PATIENT: Their own reports
@login_required
def patient_reports(request):
    reports = MedicalReport.objects.filter(patient=request.user)
    return render(request, 'reports/patient_reports.html', {
        'title': 'My Medical Reports',
        'reports': reports,
    })

# DOCTOR: Reports created by them
@login_required
def doctor_reports(request):
    reports = MedicalReport.objects.filter(doctor=request.user)
    return render(request, 'reports/doctor_reports.html', {
        'title': 'Reports I Wrote',
        'reports': reports,
    })

# ADMIN: All reports
@login_required
@user_passes_test(is_admin)
def all_reports(request):
    reports = MedicalReport.objects.all()
    return render(request, 'reports/all_reports.html', {
        'title': 'All Reports',
        'reports': reports,
    })

@login_required
def report_upload(request):
    if not hasattr(request.user, 'doctor_profile') and not request.user.is_superuser:
        raise PermissionDenied("Only doctors or admins can upload reports.")
    
    if request.method == 'POST':
        form = MedicalReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.doctor = request.user
            report.save()
            return redirect('doctor-reports')
    else:
        form = MedicalReportForm()
    return render(request, 'reports/report_upload.html', {'form': form})


@login_required
def download_report(request, report_id):
    try:
        report = MedicalReport.objects.get(pk=report_id)
        
        # Check if the user has permission to access the report
        if request.user != report.patient and request.user != report.doctor and not request.user.is_superuser:
            raise Http404("You don't have permission to access this report.")

        if not report.file:
            raise Http404("This report has no file attached.")

        response = FileResponse(report.file.open('rb'), as_attachment=True, filename=os.path.basename(report.file.name))
        return response

    except MedicalReport.DoesNotExist:
        raise Http404("Report not found.")
    


    

    