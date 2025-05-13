from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count
from django.contrib import messages
from datetime import timedelta, datetime
from patient.models import Patient, RendezVous
from docteur.models import Doctor
from django.db.models.functions import TruncDate
from .forms import DoctorProfileForm 
from django.utils.dateformat import format
import json


JOURS_FR = {
    'Sunday': 'Dimanche',
    'Monday': 'Lundi',
    'Tuesday': 'Mardi',
    'Wednesday': 'Mercredi',
    'Thursday': 'Jeudi',
    'Friday': 'Vendredi',
    'Saturday': 'Samedi',
    
}

@login_required
def ophtalmologue_dashboard(request):
    
    if request.user.profile.speciality != "ophtalmologue":
        messages.error(request, "Accès non autorisé")
        return redirect("login")

    doctor = get_object_or_404(Doctor, profile=request.user.profile)

    
    patients_recents = Patient.objects.filter(doctors=doctor).order_by('-consultation_date')[:5]

  
    demain = timezone.now().date() + timedelta(days=1)
    rendez_vous_demain = RendezVous.objects.filter(
        doctor=doctor,
        date__date=demain
    ).order_by('date')

    start_week = timezone.now().date() - timedelta(days=(timezone.now().date().weekday()+ 1) % 7)  # lundi
    end_week = start_week + timedelta(days=6)  

    
    patients_par_jour = Patient.objects.filter(
        doctors=doctor,
        consultation_date__date__gte=start_week,
        consultation_date__date__lte=end_week
    ).annotate(day=TruncDate('consultation_date')).values('day').annotate(total=Count('id')).order_by('day')

    
    jours_dict = {entry['day']: entry['total'] for entry in patients_par_jour}

    
    labels = []
    data = []
    for i in range(7):
        jour_date = start_week + timedelta(days=i)
        jour_en = jour_date.strftime('%A')
        jour_fr = JOURS_FR[jour_en]
        labels.append(jour_fr)
        data.append(jours_dict.get(jour_date, 0))  # 0 si aucun patient ce jour-là

    rendez_vous_all = RendezVous.objects.filter(doctor=doctor)
    events = []

    for rdv in rendez_vous_all:
     events.append({
        'title': f"RDV avec {rdv.patient.first_name}",
        'start': format(rdv.date, 'Y-m-d'),
        'display': 'background'  # style discret (pastille)
    })

    return render(request, "docteur/ophtalmologue_dashboard.html", {
        "doctor": doctor,
        "patients_recents": patients_recents,
        "rendez_vous_demain": rendez_vous_demain,
        "labels": labels,
        "data": data,
        "events": json.dumps(events, ensure_ascii=False),  # 🔁 Ajoute json.dumps ici

    })



@login_required
def profile_card(request):
    doctor = Doctor.objects.get(profile=request.user.profile)

    if request.method == "POST":
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    "success": True,
                    "photo": doctor.get_photo_url(),
                    "name": f"Dr. {doctor.profile.user.first_name} {doctor.profile.user.last_name}",
                    "specialization": doctor.specialization,
                    "workplace": f"{doctor.workplace_name} - {doctor.city}",
                    "phone": doctor.phone_number
                })
            messages.success(request, "Votre profil a été mis à jour avec succès !")
            return redirect("docteur:ophtalmologue_dashboard")
    
    else:
        form = DoctorProfileForm(instance=doctor)

    return render(request, "docteur/doc_card.html", {"form": form, "doctor": doctor})




@login_required
def edit_profile(request):
    doctor = Doctor.objects.get(profile=request.user.profile)

    if request.method == "POST":
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)
        remove_photo = request.POST.get("remove_photo", "0")

        if form.is_valid():
            if remove_photo == "1":
                doctor.photo = "doc_profile_pics/photo_defaut.jpg"  
            form.save()
            
            messages.success(request, "Votre profil a été mis à jour avec succès !")
            return redirect("docteur:profile_card")

    else:
        form = DoctorProfileForm(instance=doctor)

    return render(request, "docteur/profile.html", {"form": form, "doctor": doctor})
