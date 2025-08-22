from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment, APPOINTMENT_STATUS
from .forms import AppointmentForm
from django.contrib import messages

@login_required
def appointment_list(request):
    if request.user.role == 'doctor':
        appointments = Appointment.objects.select_related('patient').filter(doctor=request.user)
    elif request.user.role == 'patient':
        appointments = Appointment.objects.select_related('doctor').filter(patient=request.user)
    else:
        appointments = Appointment.objects.select_related('doctor', 'patient').all()
    
    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments
    })

@login_required
def book_appointment(request):
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('appointment-list')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user

            # Prevent double-booking the same doctor at the same time
            exists = Appointment.objects.filter(
                doctor=appointment.doctor,
                date=appointment.date,
                time=appointment.time
            ).exists()

            if exists:
                messages.error(request, 'This time slot is already booked.')
            else:
                appointment.save()
                messages.success(request, 'Appointment booked successfully!')
                return redirect('appointment-list')
        else:
            messages.error(request, 'Please correct the form errors.')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/add_appointment.html', {
        'form': form
    })

@login_required
def appointment_status_update(request, appointment_id, status):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Validate that the new status is in the defined choices
    valid_statuses = [choice[0] for choice in APPOINTMENT_STATUS]
    if status not in valid_statuses:
        messages.error(request, 'Invalid status.')
        return redirect('appointment-list')

    if request.user == appointment.doctor:
        appointment.status = status
        appointment.save()
        messages.success(request, f'Appointment status updated to "{status}".')
    else:
        messages.error(request, 'You are not authorized to update this appointment.')

    return redirect('appointment-list')
