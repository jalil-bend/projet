from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MedicalRecord, MedicalImage, Prescription
from patient.models import Patient
from docteur.models import Doctor
from django.core.exceptions import PermissionDenied

@login_required
def upload_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    doctor = getattr(getattr(request.user, 'profile', None), 'doctor_profile', None)
    if not doctor:
        raise PermissionDenied

    if request.method == 'POST':
        prochain_rdv = request.POST.get('prochain_rendez_vous') or None
        cataracte_type = request.POST.get('cataracte_type', '')
        if not request.POST.get('cataracte'):
            cataracte_type = ''

        record = MedicalRecord.objects.create(
            patient=patient,
            doctor=doctor,
            description_generale=request.POST.get('description', ''),
            lentille_souple=bool(request.POST.get('lentille_souple')),
            lentille_souple_spherique=bool(request.POST.get('lentille_souple_spherique')),
            lentille_souple_torique=bool(request.POST.get('lentille_souple_torique')),
            lentille_rpg=bool(request.POST.get('lentille_rpg')),
            lrpg_spherique=bool(request.POST.get('lrpg_spherique')),
            lrpg_torique_ant=bool(request.POST.get('lrpg_torique_ant')),
            lrpg_torique_post=bool(request.POST.get('lrpg_torique_post')),
            lrpg_bitorique=bool(request.POST.get('lrpg_bitorique')),
            lentille_sclerale=bool(request.POST.get('lentille_sclerale')),
            cataracte=bool(request.POST.get('cataracte')),
            cataracte_type=request.POST.get('cataracte_type', ''),
            diabetique=bool(request.POST.get('diabetique')),
            hypertendu=bool(request.POST.get('hypertendu')),
            glaucome=bool(request.POST.get('glaucome')),
            glaucome_type=request.POST.get('glaucome_type', ''),
            uveite=bool(request.POST.get('uveite')),
            uveite_type=request.POST.get('uveite_type', ''),
            conjonctivite=bool(request.POST.get('conjonctivite')),
            conjonctivite_type=request.POST.get('conjonctivite_type', ''),
            sclerose=bool(request.POST.get('sclerose')),
            sclerose_type=request.POST.get('sclerose_type', ''),
            keratoconique=bool(request.POST.get('keratoconique')),
            stade_keratoconique=request.POST.get('stade_keratoconique', ''),
            v3m=bool(request.POST.get('v3m')),
            description_v3m=request.POST.get('description_v3m', ''),
            fo=bool(request.POST.get('fo')),
            description_fo=request.POST.get('description_fo', ''),
            ce=bool(request.POST.get('ce')),
            description_ce=request.POST.get('description_ce', ''),
            scjr=bool(request.POST.get('scjr')),
            description_scjr=request.POST.get('description_scjr', ''),
            vi=bool(request.POST.get('vi')),
            description_vi=request.POST.get('description_vi', ''),
            ablation_fils=bool(request.POST.get('ablation_fils')),
            description_ablation_fils=request.POST.get('description_ablation_fils', ''),
            echo_a=bool(request.POST.get('echo_a')),
            description_echo_a=request.POST.get('description_echo_a', ''),
            echo_b=bool(request.POST.get('echo_b')),
            description_echo_b=request.POST.get('description_echo_b', ''),
            skiascopie=bool(request.POST.get('skiascopie')),
            description_skiascopie=request.POST.get('description_skiascopie', ''),
            laser_argon=bool(request.POST.get('laser_argon')),
            description_laser_argon=request.POST.get('description_laser_argon', ''),
            laser_yag=bool(request.POST.get('laser_yag')),
            description_laser_yag=request.POST.get('description_laser_yag', ''),
            angio=bool(request.POST.get('angio')),
            description_angio=request.POST.get('description_angio', ''),
            lentille_therap=bool(request.POST.get('lentille_therap')),
            description_lentille_therap=request.POST.get('description_lentille_therap', ''),
            bouchons_lacrym=bool(request.POST.get('bouchons_lacrym')),
            description_bouchons_lacrym=request.POST.get('description_bouchons_lacrym', '')
        )
        

        # Synchronise la donnée avec le modèle Patient pour affichage cohérent dans la liste
        if prochain_rdv:
            patient.next_appointment = prochain_rdv
            patient.save()

        if request.FILES.get('file'):
            record.file = request.FILES['file']
            record.save()

        # Gérer les images multiples pour chaque catégorie
        categories = ['topographie', 'oct', 'lampe_a_fente']
        for category in categories:
            files = request.FILES.getlist(f'{category}[]')
            for image_file in files:
                try:
                    # Créer l'objet MedicalImage avec le record
                    image = MedicalImage(
                        record=record,
                        category=category,
                        image=image_file
                    )
                    # Valider manuellement avant sauvegarde
                    image.full_clean()
                    image.save()
                except ValidationError as e:
                    messages.error(request, str(e))

        # Log des données de prescription
        print("Données de prescription reçues :", {
            'od_sph_lc': request.POST.get('od_sph_lc'),
            'od_cyl_lc': request.POST.get('od_cyl_lc'),
            'od_axe_lc': request.POST.get('od_axe_lc'),
            'od_dia': request.POST.get('od_dia'),
            'od_rc': request.POST.get('od_rc'),
            'og_sph_lc': request.POST.get('og_sph_lc'),
            'og_cyl_lc': request.POST.get('og_cyl_lc'),
            'og_axe_lc': request.POST.get('og_axe_lc'),
            'og_dia': request.POST.get('og_dia'),
            'og_rc': request.POST.get('og_rc')
        })

        # Enregistrer les prescriptions
        Prescription.objects.create(
            record=record,
            od_sph=request.POST.get('od_sph', ''),
            od_cyl=request.POST.get('od_cyl', ''),
            od_axe=request.POST.get('od_axe', ''),
            og_sph=request.POST.get('og_sph', ''),
            og_cyl=request.POST.get('og_cyl', ''),
            og_axe=request.POST.get('og_axe', ''),
            od_sph_lc=request.POST.get('od_sph_lc', ''),
            od_cyl_lc=request.POST.get('od_cyl_lc', ''),
            od_axe_lc=request.POST.get('od_axe_lc', ''),
            od_dia=request.POST.get('od_dia', ''),
            od_rc=request.POST.get('od_rc', ''),
            og_sph_lc=request.POST.get('og_sph_lc', ''),
            og_cyl_lc=request.POST.get('og_cyl_lc', ''),
            og_axe_lc=request.POST.get('og_axe_lc', ''),
            og_dia=request.POST.get('og_dia', ''),
            og_rc=request.POST.get('og_rc', '')
        )

        messages.success(request, 'Dossier médical créé avec succès.')
        return redirect('view_records', patient_id=patient.id)

    return render(request, 'records/upload_record.html', {'patient': patient})

@login_required
def patient_records(request):
    if not hasattr(request.user, 'patient'):
        raise PermissionDenied
    
    patient = request.user.patient  # Get the patient instance
    records = MedicalRecord.objects.filter(patient=patient)
    return render(request, 'records/patient_records.html', {
        'records': records,
        'patient': patient,  # Pass the patient instance to the template
        'date_of_birth': patient.date_of_birth  # Pass the patient's date of birth to the template
    })

@login_required
def view_records(request, patient_id):
    # Cette vue est maintenant réservée aux professionnels
    doctor = getattr(getattr(request.user, 'profile', None), 'doctor_profile', None)
    if not doctor:
        raise PermissionDenied
    
    patient = get_object_or_404(Patient, id=patient_id)
    records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')
    
    # Liste des examens et leurs descriptions
    EXAMENS = [
        'v3m', 'fo', 'ce', 'scjr', 'vi', 'ablation_fils', 
        'echo_a', 'echo_b', 'skiascopie', 'laser_argon', 
        'laser_yag', 'angio', 'lentille_therap', 'bouchons_lacrym'
    ]
    
    context = {
        'patient': patient,
        'records': records,
        'examens': EXAMENS
    }
    return render(request, 'records/view_records.html', context)

@login_required
def create_prescription(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    doctor = getattr(getattr(request.user, 'profile', None), 'doctor_profile', None)
    if not doctor:
        raise PermissionDenied

    if request.method == 'POST':
        medicaments = request.POST.getlist('medicament')
        dosages = request.POST.getlist('dosage')
        frequences = request.POST.getlist('frequence')
        details = []
        for med, dose, freq in zip(medicaments, dosages, frequences):
            if med:
                details.append(f"{med} | {dose} | {freq} fois/jour")

        record = MedicalRecord.objects.filter(patient=patient).order_by('-created_at').first()
        if not record:
            record = MedicalRecord.objects.create(patient=patient, doctor=doctor)
        Prescription.objects.create(record=record, prescription_details="; ".join(details))
        messages.success(request, "Ordonnance créée avec succès.")
        return redirect('view_records', patient_id=patient.id)

    return render(request, 'records/create_prescription.html', {'patient': patient})
