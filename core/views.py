from django.shortcuts import render

def index(request):
    # L'utilisateur connecté verra la navigation spéciale (gérée côté template)
    return render(request, 'core/index.html')

# Create your views here.
