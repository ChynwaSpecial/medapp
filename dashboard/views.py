from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from reports.models import MedicalReport
from accounts.models import User
from datetime import date



@login_required
def dashboard_home(request):
    user = request.user
    context = {}

    if user.role == 'doctor':
        context['today_appointments'] = Appointment.objects.filter(doctor=user, date=date.today()).count()
        context['total_patients'] = Appointment.objects.filter(doctor=user).values('patient').distinct().count()
        context['report_count'] = MedicalReport.objects.filter(doctor=user).count()

    elif user.role == 'patient':
        context['upcoming_appointments'] = Appointment.objects.filter(patient=user, date__gte=date.today()).count()
        context['report_count'] = MedicalReport.objects.filter(patient=user).count()

    elif user.is_superuser:
        context['doctor_count'] = User.objects.filter(role='doctor').count()
        context['patient_count'] = User.objects.filter(role='patient').count()
        context['appointment_count'] = Appointment.objects.all().count()

    return render(request, 'dashboard/dashboard_home.html', context)

@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin.html')

@login_required
def doctor_dashboard(request):
    return render(request, 'dashboard/doctor.html')

@login_required
def patient_dashboard(request):
    return render(request, 'dashboard/patient.html')

@login_required
def staff_dashboard(request):
    return render(request, 'dashboard/staff.html')
