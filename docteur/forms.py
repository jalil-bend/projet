from django import forms
from .models import Doctor

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor  
        fields = [
            'photo', 'workplace_type', 'workplace_name', 
            'specialization',  'phone_number', 'city', 
            'consultation_fee', 'availability_dim', 'availability_lun', 'availability_mar', 
            'availability_mer', 'availability_jeu', 'availability_ven', 'availability_sam',
        ]  

        widgets = {
            'availability': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Numéro de téléphone'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Prix de la consultation'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Ville'}),
            'workplace_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nom du lieu de travail'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Votre spécialité'}),
            'availability_dim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 08:00 - 12:00'}),
            'availability_lun': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 08:00 - 12:00'}),
            'availability_mar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 08:00 - 12:00'}),
            'availability_mer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 08:00 - 12:00'}),
            'availability_jeu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 08:00 - 12:00'}),
            'availability_ven': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 08:00 - 12:00'}),
            'availability_sam': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 08:00 - 12:00'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Appliquer une classe CSS Bootstrap à tous les champs
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.FileInput):  # Exclure le champ "photo"
                field.widget.attrs['class'] = 'form-control'






