from django import forms
from .models import Patient
from .models import FicheClinique
from .models import RendezVous



class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'birth_date', 'profession', 'email',
            'phone', 'birth_place', 'sphere_right_vl', 'cylinder_right_vl', 'axis_right_vl', 'sphere_left_vl',
             'cylinder_left_vl', 'axis_left_vl', 'sphere_right_vp', 'cylinder_right_vp', 'axis_right_vp',
              'sphere_left_vp', 'cylinder_left_vp', 'axis_left_vp', 'diagnosis', 'remarks', 
             'prescription', 
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_place': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'sphere_right_vl': forms.TextInput(attrs={'class': 'form-control'}),
            'cylinder_right_vl': forms.TextInput(attrs={'class': 'form-control'}),
            'axis_right_vl': forms.TextInput(attrs={'class': 'form-control'}),
            'sphere_left_vl': forms.TextInput(attrs={'class': 'form-control'}),
            'cylinder_left_vl': forms.TextInput(attrs={'class': 'form-control'}),
            'axis_left_vl': forms.TextInput(attrs={'class': 'form-control'}),
            'sphere_right_vp': forms.TextInput(attrs={'class': 'form-control'}),
            'cylinder_right_vp': forms.TextInput(attrs={'class': 'form-control'}),
            'axis_right_vp': forms.TextInput(attrs={'class': 'form-control'}),
            'sphere_left_vp': forms.TextInput(attrs={'class': 'form-control'}),
            'cylinder_left_vp': forms.TextInput(attrs={'class': 'form-control'}),
            'axis_left_vp': forms.TextInput(attrs={'class': 'form-control'}),
            'diagnosis': forms.TextInput(attrs={'class' : 'form-control'}),
            'prescription': forms.TextInput(attrs={'class' : 'form-control'}),
            'consultation_date': forms.DateInput(attrs={'type': 'date'}),
            'next_appointment': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import FicheClinique

class FicheCliniqueForm(forms.ModelForm):
    class Meta:
        model = FicheClinique
        fields = ['antecedents', 'diagnostic', 'traitement']
        widgets = {
            'antecedents': forms.Textarea(attrs={'rows': 3}),
            'diagnostic': forms.Textarea(attrs={'rows': 3}),
            'traitement': forms.Textarea(attrs={'rows': 3}),
        }

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['patient', 'date', 'status', 'description']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


    