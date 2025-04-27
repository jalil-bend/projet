from django.db import models
from patient.models import Patient
from docteur.models import Doctor
from django.core.validators import FileExtensionValidator
from .validators import validate_image_type

# Modèle pour les dossiers médicaux
class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        'patient.Patient',
        on_delete=models.CASCADE,
        related_name='medical_records'
    )
    doctor = models.ForeignKey(
        'docteur.Doctor',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_records'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    details = models.TextField()
    description_generale = models.TextField(blank=True)



    file = models.FileField(upload_to='medical_records/%Y/%m/%d/', blank=True, null=True)
    diabetique = models.BooleanField(default=False, verbose_name="Diabétique")
    keratoconique = models.BooleanField(default=False, verbose_name="Kératoconique")
    STADE_KERATOCONIQUE_CHOICES = [
        ('fruste', 'Kératocône fruste'),
        ('stade_1', 'Stade 1'),
        ('stade_2', 'Stade 2'),
        ('stade_3', 'Stade 3'),
        ('stade_4', 'Stade 4'),
    ]
    stade_keratoconique = models.CharField(
        max_length=10,
        choices=STADE_KERATOCONIQUE_CHOICES,
        blank=True,
        verbose_name="Stade du kératoconique"
    )
    cataracte = models.BooleanField(default=False, verbose_name="Cataracte")
    TYPE_CATARACTE_CHOICES = [
        ('', '-- Sélectionner --'),
        ('nucléaire', 'Cataracte nucléaire'),
        ('corticale', 'Cataracte corticale'),
        ('sous-capsulaire postérieure', 'Cataracte sous-capsulaire postérieure'),
        ('congénitale', 'Cataracte congénitale'),
        ('traumatique', 'Cataracte traumatique'),
        ('secondaire', 'Cataracte secondaire'),
    ]
    cataracte_type = models.CharField(
        max_length=200,
        choices=TYPE_CATARACTE_CHOICES,
        blank=True,
        verbose_name="Type de cataracte"
    )
    glaucome = models.BooleanField(default=False, verbose_name="Glaucome")
    GLAUCOME_CHOICES = [
        ('', '-- Sélectionner --'),
        ('angle_ouvert', 'Glaucome à angle ouvert'),
        ('angle_ferme', 'Glaucome à angle fermé')
    ]
    glaucome_type = models.CharField(
        max_length=20,
        choices=GLAUCOME_CHOICES,
        blank=True,
        verbose_name="Type de glaucome"
    )
    uveite = models.BooleanField(default=False, verbose_name="Uvéite")
    UVEITE_CHOICES = [
        ('', '-- Sélectionner --'),
        ('anterieure', 'Uvéite antérieure'),
        ('intermediaire', 'Uvéite intermédiaire'),
        ('posterieure', 'Uvéite postérieure'),
        ('panuveite', 'Panuvéite')
    ]
    uveite_type = models.CharField(
        max_length=20,
        choices=UVEITE_CHOICES,
        blank=True,
        verbose_name="Type d'uvéite"
    )
    conjonctivite = models.BooleanField(default=False, verbose_name="Conjonctivite")
    CONJONCTIVITE_CHOICES = [
        ('', '-- Sélectionner --'),
        ('bacterienne', 'Conjonctivite bactérienne'),
        ('virale', 'Conjonctivite virale'),
        ('allergique', 'Conjonctivite allergique'),
        ('irritative', 'Conjonctivite irritative'),
        ('toxique', 'Conjonctivite toxique'),
        ('autoimmune', 'Conjonctivite auto-immune'),
        ('neonatale', 'Conjonctivite néonatale')
    ]
    conjonctivite_type = models.CharField(
        max_length=20,
        choices=CONJONCTIVITE_CHOICES,
        blank=True,
        verbose_name="Type de conjonctivite"
    )
    sclerose = models.BooleanField(default=False, verbose_name="Sclérose")
    SCLEROSE_CHOICES = [
        ('', '-- Sélectionner --'),
        ('anterieure', 'Sclérite antérieure'),
        ('posterieure', 'Sclérite postérieure'),
        ('episclerite', 'Épisclérite'),
        ('nodulaire', 'Sclérite nodulaire'),
        ('necrosante_inflammation', 'Sclérite nécrosante avec inflammation'),
        ('necrosante_sans_inflammation', 'Sclérite nécrosante sans inflammation (scléromalacie perforante)')
    ]
    sclerose_type = models.CharField(
        max_length=30,
        choices=SCLEROSE_CHOICES,
        blank=True,
        verbose_name="Type de sclérose"
    )
    hypertendu = models.BooleanField(default=False, verbose_name="Hypertendu")
    v3m = models.BooleanField(default=False, verbose_name="V3M")
    description_v3m = models.TextField(blank=True, verbose_name="Description V3M")
    fo = models.BooleanField(default=False, verbose_name="F.O")
    description_fo = models.TextField(blank=True, verbose_name="Description F.O")
    ce = models.BooleanField(default=False, verbose_name="C.E")
    description_ce = models.TextField(blank=True, verbose_name="Description C.E")
    scjr = models.BooleanField(default=False, verbose_name="S/Cj -R/B")
    description_scjr = models.TextField(blank=True, verbose_name="Description S/Cj -R/B")
    vi = models.BooleanField(default=False, verbose_name="V.I")
    description_vi = models.TextField(blank=True, verbose_name="Description V.I")
    ablation_fils = models.BooleanField(default=False, verbose_name="Ablation de Fils")
    description_ablation_fils = models.TextField(blank=True, verbose_name="Description Ablation de Fils")
    echo_a = models.BooleanField(default=False, verbose_name="Echo A")
    description_echo_a = models.TextField(blank=True, verbose_name="Description Echo A")
    echo_b = models.BooleanField(default=False, verbose_name="Echo B")
    description_echo_b = models.TextField(blank=True, verbose_name="Description Echo B")
    skiascopie = models.BooleanField(default=False, verbose_name="Skiascopie")
    description_skiascopie = models.TextField(blank=True, verbose_name="Description Skiascopie")
    laser_argon = models.BooleanField(default=False, verbose_name="Laser Argon")
    description_laser_argon = models.TextField(blank=True, verbose_name="Description Laser Argon")
    laser_yag = models.BooleanField(default=False, verbose_name="Laser YAG")
    description_laser_yag = models.TextField(blank=True, verbose_name="Description Laser YAG")
    angio = models.BooleanField(default=False, verbose_name="Angio")
    description_angio = models.TextField(blank=True, verbose_name="Description Angio")
    lentille_therap = models.BooleanField(default=False, verbose_name="Lentille Therap")
    description_lentille_therap = models.TextField(blank=True, verbose_name="Description Lentille Therap")
    bouchons_lacrym = models.BooleanField(default=False, verbose_name="Bouchons Lacrym")
    description_bouchons_lacrym = models.TextField(blank=True, verbose_name="Description Bouchons Lacrym")
    prochain_rendez_vous = models.DateField(null=True, blank=True, verbose_name="Prochain rendez-vous")

    # Lentilles de contact
    lentille_souple = models.BooleanField(default=False, verbose_name="Lentille souple")
    lentille_souple_spherique = models.BooleanField(default=False, verbose_name="Lentille souple sphérique")
    lentille_souple_torique = models.BooleanField(default=False, verbose_name="Lentille souple torique")
    lentille_rpg = models.BooleanField(default=False, verbose_name="Lentille RPG")
    lrpg_spherique = models.BooleanField(default=False, verbose_name="LRPG sphérique")
    lrpg_torique_ant = models.BooleanField(default=False, verbose_name="LRPG torique face antérieure")
    lrpg_torique_post = models.BooleanField(default=False, verbose_name="LRPG torique face postérieure")
    lrpg_bitorique = models.BooleanField(default=False, verbose_name="LRPG bi-torique")
    lentille_sclerale = models.BooleanField(default=False, verbose_name="Lentille sclérale")

    def get_examens(self):
        examens = [
            'v3m', 'fo', 'ce', 'scjr', 'vi', 'ablation_fils',
            'echo_a', 'echo_b', 'skiascopie', 'laser_argon',
            'laser_yag', 'angio', 'lentille_therap', 'bouchons_lacrym'
        ]
        
        result = []
        for examen in examens:
            if getattr(self, examen, False):
                result.append({
                    'nom': examen,
                    'description': getattr(self, f'description_{examen}')
                })
        return result



    def __str__(self):
        return f"Dossier de {self.patient.user.username} - {self.created_at.strftime('%Y-%m-%d')}"

# Modèle pour les images médicales
class MedicalImage(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='images')
    category = models.CharField(
        max_length=20,
        choices=[
            ('topographie', 'Topographie'),
            ('oct', 'OCT'),
            ('lampe_a_fente', 'Lampe à fente')
        ]
    )
    image = models.ImageField(
        upload_to='medical_images/%Y/%m/%d/',
        validators=[validate_image_type]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validation personnalisée pour le nombre d'images
        if self.record and self.category:
            if self.record.images.filter(category=self.category).count() >= 50:
                raise ValidationError(f"Vous ne pouvez pas ajouter plus de 50 images pour cette catégorie.")

    def save(self, *args, **kwargs):
        # Validation avant sauvegarde
        self.full_clean()
        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.get_category_display()} - {self.record.patient}"

# Modèle pour les prescriptions
class Prescription(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    od_sph = models.CharField(max_length=10, blank=True)
    od_cyl = models.CharField(max_length=10, blank=True)
    od_axe = models.CharField(max_length=10, blank=True)
    od_add = models.CharField(max_length=10, blank=True)
    og_sph = models.CharField(max_length=10, blank=True)
    og_cyl = models.CharField(max_length=10, blank=True)
    og_axe = models.CharField(max_length=10, blank=True)
    og_add = models.CharField(max_length=10, blank=True)
    od_dia = models.CharField(max_length=10, blank=True)
    od_rc = models.CharField(max_length=10, blank=True)
    og_dia = models.CharField(max_length=10, blank=True)
    og_rc = models.CharField(max_length=10, blank=True)
    od_sph_lc = models.CharField(max_length=10, blank=True)
    od_cyl_lc = models.CharField(max_length=10, blank=True)
    od_axe_lc = models.CharField(max_length=10, blank=True)
    og_sph_lc = models.CharField(max_length=10, blank=True)
    og_cyl_lc = models.CharField(max_length=10, blank=True)
    og_axe_lc = models.CharField(max_length=10, blank=True)
    prescription_details = models.TextField(blank=True)  # Ordonnance médicaments/dosages/fréquences
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"Prescription du {self.created_at.strftime('%Y-%m-%d')}"
