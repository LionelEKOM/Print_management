from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

class HomePageView(TemplateView):
    template_name = "printers/Homepage.html"
    
class CustomLoginView(LoginView):
    template_name = 'auth/login.html'  # Le template pour la page de connexion
    
    def form_valid(self, form):
        # Récupérer le nom d'utilisateur de l'utilisateur authentifié
        username = self.request.user.username
        # Ajoute un message de succès lorsque l'utilisateur est authentifié avec succès
        messages.success(self.request, f"Connexion réussie. Bienvenue {username} sur votre tableau de bord !")
        return super().form_valid(form)
    
@login_required
def dashboard(request):
    return render(request, 'printers/dashboard.html')