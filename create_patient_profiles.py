from users.models import Profile
from patient.models import Patient
from django.db import transaction

if __name__ == "__main__":
    count = 0
    with transaction.atomic():
        for patient in Patient.objects.all():
            user = patient.user
            if user and not hasattr(user, 'profile'):
                Profile.objects.create(user=user, speciality='patient')
                count += 1
    print(f'Profils créés pour {count} patients.')
