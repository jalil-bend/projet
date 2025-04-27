from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages 
from django.core.mail import send_mail, BadHeaderError
from django.contrib.sites.shortcuts import get_current_site
from .models import User, Profile
from django.contrib.auth.decorators import login_required
from django.conf import settings



def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        speciality = request.POST.get("speciality")
        email = request.POST.get("email")
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")

        # Vérifications des erreurs
        if User.objects.filter(username=username).exists():
            return render(request, "users/register.html", {
    "username": username,
    "first_name": first_name,
    "last_name": last_name,
    "speciality": speciality,
    "email": email
})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse email est déjà utilisée")
            return render(request, "users/register.html", {
    "username": username,
    "first_name": first_name,
    "last_name": last_name,
    "speciality": speciality,
    "email": email
})

        if not email.endswith(".com"):
            messages.error(request, "Veuillez entrer une adresse email valide")
            return render(request, "users/register.html", {
    "username": username,
    "first_name": first_name,
    "last_name": last_name,
    "speciality": speciality,
    "email": email
})

        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return render(request, "users/register.html", {
    "username": username,
    "first_name": first_name,
    "last_name": last_name,
    "speciality": speciality,
    "email": email
})

        try:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1
            )
            user.is_active = False
            user.save()

            Profile.objects.create(user=user, speciality=speciality)

            
            title = "Dr" if speciality == "ophtalmologue" else "Mr"
            subject = "Validation de votre compte"
            message = (
                f"Bonjour {title} {user.first_name},\n\n"
                "Merci de vous inscrire sur notre site web. Pour activer votre compte, "
                "veuillez envoyer une photo de votre agrément ou tout autre fichier permettant de "
                "confirmer que vous êtes un professionnel de la santé.\n\n"
                "Après validation par l'administrateur, vous recevrez un email confirmant l'activation de votre compte.\n\n"
                "Cordialement,\nL'équipe OPTO DZ"
            )

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )
                messages.success(request, "Inscription réussie ! Vérifiez votre boîte mail pour activer votre compte.")
            except Exception as e:
                messages.error(request, f"Erreur lors de l'envoi de l'email : {str(e)}")
                print(f"Erreur d'envoi d'email : {str(e)}")

        except Exception as e:
            messages.error(request, f"Une erreur est survenue : {str(e)}")
            return render(request, "users/register.html", {
    "username": username,
    "first_name": first_name,
    "last_name": last_name,
    "speciality": speciality,
    "email": email
})

        # Afficher le message de confirmation d'inscription
        return render(request, "users/inscription_mail.html")

    return render(request, "users/register.html")


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")  # récupère la case à cocher
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Gestion de la session persistante
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 semaines
                else:
                    request.session.set_expiry(0)  # session expire à la fermeture du navigateur
                if hasattr(user, 'profile'):
                    if user.profile.speciality == "ophtalmologue":
                        return redirect("docteur:ophtalmologue_dashboard")
                    elif user.profile.speciality == "optometriste":
                        return redirect("optometriste_dashboard")
                else:
                    messages.error(request, "Votre profil n'est pas encore configuré.")
                    return render(request, "users/login.html", {"username": username})
            else:
                messages.error(request, "Votre compte est inactif. Veuillez vérifier votre email.")
                return render(request, "users/login.html", {"username": username})
        else:
            messages.error(request, "Identifiants incorrects.")
            return render(request, "users/login.html", {"username": username})

    return render(request, "users/login.html")



@login_required
def optometriste_dashboard(request):
    if not request.user.profile.speciality == "optometriste":
        messages.error(request, "Accès non autorisé")
        return redirect("login")
    return render(request, "users/optometriste_dashboard.html")

def termes(request):
    return render(request, "users/termes.html")






# Create your views here.
