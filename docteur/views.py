from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import DoctorProfileForm
from .models import Doctor  


@login_required
def ophtalmologue_dashboard(request):
    if not request.user.profile.speciality == "ophtalmologue":
        messages.error(request, "Accès non autorisé")
        return redirect("login")
    
    doctor = Doctor.objects.get(profile=request.user.profile)
    return render(request, "docteur/ophtalmologue_dashboard.html", {"doctor": doctor})


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



