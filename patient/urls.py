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
    path('supprimer/<int:patient_id>/', views.supprimer_patient, name='supprimer_patient'),
]