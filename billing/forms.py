from django import forms
from .models import Invoice
from patients.models import PatientProfile
from doctors.models import DoctorProfile

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['patient', 'doctor', 'due_date', 'total_amount', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter any additional notes...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter patient and doctor dropdowns for clarity
        self.fields['patient'].queryset = PatientProfile.objects.select_related('user').all()
        self.fields['doctor'].queryset = DoctorProfile.objects.select_related('user').all()

        if user:
            # If the user is a doctor, hide doctor field and set initial value
            if hasattr(user, 'doctor_profile'):
                self.fields['doctor'].widget = forms.HiddenInput()
                self.fields['doctor'].initial = user.doctor_profile
