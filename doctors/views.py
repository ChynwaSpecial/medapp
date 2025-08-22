from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import DoctorProfile
from .forms import DoctorProfileForm

@login_required
def profile_view(request):
    profile = request.user.doctor_profile
    return render(request, 'doctors/profile_view.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile = request.user.doctor_profile
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('doctor-profile')
    else:
        form = DoctorProfileForm(instance=profile)
    return render(request, 'doctors/profile_edit.html', {'form': form})

