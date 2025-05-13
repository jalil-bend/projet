from django.contrib import admin
from django.urls import path
from . import views


app_name = "patient"

urlpatterns = [
    path("liste/", views.liste_patients, name="liste_patients" ),
    path("generer_compte/<int:patient_id>/", views.generer_compte_patient, name="generer_compte_patient"),
    path("ajouter_patient/", views.ajouter_patient, name="ajouter_patient"),
    path('profil/<int:patient_id>/', views.voir_profil_patient, name="profil_patient"),
    path('modifier/<int:pk>/', views.modifier_patient, name='modifier_patient'),
    path('print_credentials/<str:username>/<str:password>/<str:access_code>/', views.patient_credentials, name='print_credentials'),
    path("supprimer/<int:pk>/", views.supprimer_patient, name="supprimer_patient"),
    path('liste/rendez_vous/', views.liste_rendez_vous, name='liste_rendez_vous'),
    path('confirmer_rendez_vous/<int:pk>/', views.confirmer_rendez_vous, name='confirmer_rendez_vous'),
    path('supprimer_rendez_vous/<int:pk>/', views.supprimer_rendez_vous, name='supprimer_rendez_vous'),
    path('annuler_rendez_vous/<int:pk>/', views.annuler_rendez_vous, name='annuler_rendez_vous'),
    path('dashboard/', views.dashboard_patient, name='patient_dashboard'),
    
    
    # path('ajouter_rendez_vous/', views.ajouter_rendez_vous, name='ajouter_rendez_vous'),
]