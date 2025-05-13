from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Patient

@login_required
def dashboard_patient(request):
    # Récupère le patient lié à l'utilisateur connecté
    patient = get_object_or_404(Patient, user=request.user)

    # Code d'accès
    access_code = patient.access_password

    # Récupération des dossiers médicaux (exemple : fiches cliniques créées par des docteurs)
    dossiers = []
    if hasattr(patient, 'fiches_cliniques'):
        for fiche in patient.fiches_cliniques.all():
            doctor_name = str(fiche.doctor) if hasattr(fiche, 'doctor') else 'Inconnu'
            detail_url = fiche.get_absolute_url() if hasattr(fiche, 'get_absolute_url') else '#'
            dossiers.append({
                'doctor_name': doctor_name,
                'detail_url': detail_url
            })

    profile_url = reverse('patient:profil_patient', args=[patient.id])
    logout_url = reverse('logout')

    context = {
        'access_code': access_code,
        'medical_records': dossiers,
        'profile_url': profile_url,
        'logout_url': logout_url,
    }
    return render(request, 'patient/dashboard.html', context)
