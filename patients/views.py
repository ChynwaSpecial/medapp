from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PatientProfileForm

@login_required
def profile_view(request):
    profile = request.user.patient_profile
    return render(request, 'patients/profile_view.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile = request.user.patient_profile
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('patient-profile')
    else:
        form = PatientProfileForm(instance=profile)
    return render(request, 'patients/profile_edit.html', {'form': form})
