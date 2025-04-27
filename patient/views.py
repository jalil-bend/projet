from django.shortcuts import render, redirect
from .forms import PatientForm
from .models import Patient, MedicalImage
from docteur.models import Doctor
from users.models import User
from django.contrib import messages 
from django.contrib.auth.hashers import make_password
from django.contrib.messages.storage.fallback import FallbackStorage
import random
import string
import os


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient
from docteur.models import Doctor

@login_required
def liste_patients(request):
    """Affiche la liste des patients ajoutés par le médecin connecté, avec recherche et ajout via code d'accès."""
    from django.db.models import Q
    try:
        doctor = Doctor.objects.get(profile=request.user.profile)
    except Doctor.DoesNotExist:
        doctor = None

    # Ajout via code d'accès
    if request.method == 'POST':
        access_code = request.POST.get('access_code', '').strip()
        print(f"DEBUG: access_code reçu = {access_code}")
        if not access_code:
            messages.error(request, "Veuillez entrer un code d'accès.")
        else:
            try:
                patient = Patient.objects.get(access_password=access_code)
                print(f"DEBUG: patient trouvé = {patient}")
                if doctor not in patient.doctors.all():
                    patient.doctors.add(doctor)
                    messages.success(request, f"Le patient {patient} a été ajouté à votre liste.")
                else:
                    messages.info(request, f"Le patient {patient} est déjà dans votre liste.")
                return redirect('patient:liste_patients')
            except Patient.DoesNotExist:
                print("DEBUG: Aucun patient trouvé avec ce code d'accès")
                messages.error(request, "Code d'accès invalide.")

    patients = Patient.objects.filter(doctors=doctor) if doctor else Patient.objects.none()

    search = request.GET.get('search', '').strip()
    if search:
        # Recherche sur nom, prénom, pseudo, email, et date de naissance
        date_search = search.replace('/', '-').strip()
        patients = patients.filter(
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search) |
            Q(birth_date__icontains=date_search) |
            Q(birth_date__icontains=search)
        )

    # Annotate each patient with pathology flags for template display
    from records.models import MedicalRecord
    for patient in patients:
        records = MedicalRecord.objects.filter(patient=patient)
        patient.has_diabetique = records.filter(diabetique=True).exists()
        patient.has_keratoconique = records.filter(keratoconique=True).exists()
        patient.has_cataracte = records.filter(cataracte=True).exists()
        patient.has_glaucome = records.filter(glaucome=True).exists()
        patient.has_uveite = records.filter(uveite=True).exists()
        patient.has_conjonctivite = records.filter(conjonctivite=True).exists()
        patient.has_sclerose = records.filter(sclerose=True).exists()
        patient.has_hypertendu = records.filter(hypertendu=True).exists()

    return render(request, 'patient/liste_patients.html', {'patients': patients, 'doctor': doctor, 'search': search})



from django.shortcuts import render, get_object_or_404
from .models import Patient


@login_required
def voir_profil_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    doctor = get_object_or_404(Doctor, profile=request.user.profile)
    derniere_fiche = patient.fiches_cliniques.first()
    images = patient.medical_images.all()  # 🔹 récupère les images
    form = PatientForm(instance=patient)

    # ➕ Désactive tous les champs
    for field in form.fields.values():
        field.widget.attrs['readonly'] = True
        field.widget.attrs['disabled'] = True

    return render(request, 'patient/profil_patient.html', {
        'form': form,
        'patient': patient,
        'doctor': doctor,
        'derniere_fiche': derniere_fiche,
        'images': images,
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient
from .forms import PatientForm  # On crée ça juste après
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required
def modifier_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    doctor = get_object_or_404(Doctor, profile=request.user.profile)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.consultation_date = timezone.now()  # ➕ Met à jour la date
            patient.save()
            messages.success(request, "Modifications enregistrées.")
            return redirect('patient:liste_patients')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patient/modifier_patient.html', {
        'form': form,
        'patient': patient,
        'doctor': doctor
    })


from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render

def patient_credentials(request, username, password, access_code):
    context = {
        'username': username,
        'password': password,
        'access_code': access_code,
        'generated_date': timezone.now(),
    }
    return render(request, 'patient/print_credentials.html', context)

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def supprimer_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    doctor = Doctor.objects.get(profile=request.user.profile)
    if request.method == 'POST':
        # On retire seulement la relation, on ne supprime pas le patient globalement
        patient.doctors.remove(doctor)
        messages.success(request, "Le patient a été retiré de votre liste. Il reste accessible via le code d'accès.")
        return redirect('patient:liste_patients')
    else:
        messages.error(request, "Suppression non autorisée.")
        return redirect('patient:liste_patients')

from random import randint

def ajouter_patient(request):
    doctor = Doctor.objects.get(profile=request.user.profile)
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        birth_date = request.POST.get('birth_date')
        email = request.POST.get('email')
        if last_name and first_name and birth_date and email:
            # Vérifie doublon pour ce médecin
            if Patient.objects.filter(first_name=first_name, last_name=last_name, birth_date=birth_date, doctors=doctor).exists():
                messages.error(request, "Un patient avec ce nom et cette date de naissance existe déjà dans votre liste.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Cet email est déjà utilisé.")
            else:
                username = f"{first_name.lower()}{randint(100,999)}"
                while User.objects.filter(username=username).exists():
                    username = f"{first_name.lower()}{randint(100,999)}"
                # Générer un mot de passe temporaire et un code d'accès
                import string
                import random
                temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                access_code = ''.join(random.choices(string.digits, k=6))
                user = User.objects.create_user(username=username, email=email, password=temp_password, first_name=first_name, last_name=last_name)
                patient = Patient.objects.create(user=user, first_name=first_name, last_name=last_name, birth_date=birth_date, access_password=access_code)
                patient.doctors.add(doctor)
                patient.save()
                # Redirige vers la page d'impression des identifiants
                return redirect('patient:print_credentials', username=user.username, password=temp_password, access_code=access_code)
        else:
            messages.error(request, "Tous les champs, y compris l'email, sont obligatoires pour créer un compte patient.")
    return render(request, 'patient/ajouter_patient.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient
from users.models import User
import random
import string

def generer_compte_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)

    # Vérifier si un compte a déjà été généré et stocké en session
    temp_data = request.session.get(f"temp_patient_data_{patient.id}", None)
    account_generated = temp_data is not None
    username, password, access_password = None, None, None  

    if request.method == 'POST':
        if 'generate_account' in request.POST:  # 🔹 Si le docteur clique sur "Générer un compte"
            email = request.POST.get("email")

            if email:
                # Vérifier si l'email est déjà utilisé par un autre patient
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Cet email est déjà utilisé par un autre patient.")
                    return redirect("patient:generer_compte_patient", patient_id)

                # Vérifier si le patient a déjà un compte
                if patient.has_account:
                    messages.warning(request, "Ce patient a déjà un compte.")
                    return redirect("patient:liste_patients")

                # 🔹 Générer les identifiants
                username = patient.generate_username()
                password = patient.generate_password()
                access_password = patient.generate_password()  # Mot de passe secondaire

                # 🔹 Stocker les identifiants temporairement en session pour ce patient
                request.session[f"temp_patient_data_{patient.id}"] = {
                    "username": username,
                    "password": password,
                    "access_password": access_password,
                    "email": email
                }
                
                messages.success(request, "Compte généré avec succès. Cliquez sur 'Enregistrer' pour finaliser.")
                return redirect("patient:generer_compte_patient", patient_id)

        elif 'save_account' in request.POST:  # 🔹 Si le docteur clique sur "Enregistrer"
            temp_data = request.session.get(f"temp_patient_data_{patient.id}")

            if temp_data:
                # 🔹 Création du compte utilisateur
                user = User.objects.create_user(
                    username=temp_data["username"],
                    email=temp_data["email"],
                    password=temp_data["password"]
                )

                # 🔹 Associer définitivement le compte au patient
                patient.user = user
                patient.email = temp_data["email"]
                patient.has_account = True
                patient.access_password = temp_data["access_password"]
                patient.save()

                # 🔹 Supprimer les données temporaires de la session pour éviter qu'elles ne soient réutilisées
                del request.session[f"temp_patient_data_{patient.id}"]

                messages.success(request, "Compte enregistré avec succès !")
                return redirect("patient:liste_patients")

        elif 'cancel' in request.POST:  # 🔹 Si le docteur clique sur "Annuler"
            # Supprimer les données de session pour ce patient
            request.session.pop(f"temp_patient_data_{patient.id}", None)
            messages.info(request, "Ajout annulé. Le patient est enregistré sans compte.")
            return redirect("patient:liste_patients")

    # Charger les identifiants en session si présents
    if temp_data:
        username = temp_data["username"]
        password = temp_data["password"]
        access_password = temp_data["access_password"]

    return render(request, "patient/generer_compte.html", {
        "patient": patient,
        "username": username,
        "password": password,
        "access_password": access_password,
        "account_generated": account_generated
    })



