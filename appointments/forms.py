from django import forms
from django.utils import timezone
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'doctor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'step': '900'  # 15-minute steps
            }),
            'reason': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Describe your symptoms or concerns...'
            }),
        }
        labels = {
            'doctor': 'Select Doctor',
            'date': 'Appointment Date',
            'time': 'Appointment Time',
            'reason': 'Reason for Appointment',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Accept user context from the view
        super().__init__(*args, **kwargs)

        # Filter only users with role='doctor' in the dropdown
        self.fields['doctor'].queryset = self.fields['doctor'].queryset.filter(role='doctor')

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.localdate():
            raise forms.ValidationError("You can't book an appointment in the past.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        # Check if an appointment already exists at the same date/time with the same doctor
        if doctor and date and time:
            conflict = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                time=time
            ).exists()
            if conflict:
                raise forms.ValidationError(
                    "This doctor already has an appointment at this date and time. Please choose a different slot."
                )
        return cleaned_data
