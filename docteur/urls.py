from django.contrib import admin
from django.urls import path
from . import views

app_name = "docteur"  

urlpatterns = [
     path("dashboard/ophtalmologue/", views.ophtalmologue_dashboard, name="ophtalmologue_dashboard"),
     path("profile/card/", views.profile_card, name="profile_card"),
     path("profile/", views.edit_profile, name="edit_profile"),
     
     
    ]

