from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
# from .views import CustomPasswordResetView

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('termes/', views.termes, name='termes'),
    path('login/', views.user_login, name='login'),
    
    path('dashboard/optometriste/', views.optometriste_dashboard, name='optometriste_dashboard'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/registration/password_reset.html',
        email_template_name='users/registration/password_reset_email.html',
        subject_template_name='users/registration/password_reset_subject.txt',
        success_url= reverse_lazy('password_reset_done')
    ), name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/registration/password_reset_confirm.html',
        success_url= reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]

   








 # path('mot-de-passe-oublie/', auth_views.PasswordResetView.as_view(template_name='users/registration/password_reset.html'), name='password_reset'),
   
    # path('mot-de-passe-envoye/', auth_views.PasswordResetDoneView.as_view( template_name='users/registration/password_reset_done.html'), name='password_reset_done'),
   
    # path('reinitialisation/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/registration/password_reset_confirm.html'), name='password_reset_confirm'),
   
    # path('reinitialisation-terminee/', auth_views.PasswordResetCompleteView.as_view( template_name='users/registration/password_reset_complete.html'), name='password_reset_complete'),
   
    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),