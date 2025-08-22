from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import User




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("✅ User created:", user.email, user.role)
            login(request, user)
            return redirect_user_by_role(user)
        else:
            print("❌ Form errors:", form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})





def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_user_by_role(user)
        else:
            messages.error(request, "Invalid email or password")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def redirect_user_by_role(user):
    if user.is_superuser or user.role == 'admin':
        return redirect('admin-dashboard')
    elif user.role == 'doctor':
        return redirect('doctor-dashboard')
    elif user.role == 'patient':
        return redirect('patient-dashboard')
    elif user.role == 'staff':
        return redirect('staff-dashboard')
    return redirect('default-dashboard')


@login_required
def doctor_list(request):
    doctors = User.objects.filter(role='doctor')
    return render(request, 'accounts/doctor_list.html', {'doctors': doctors})

@login_required
def patient_list(request):
    patients = User.objects.filter(role='patient')
    return render(request, 'accounts/patient_list.html', {'patients': patients})
