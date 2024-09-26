from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from printers.forms import CustomUserCreationForm
from printers.models import CustomUser, PrintJob, Printer
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
    printers = Printer.objects.all()
    print_jobs = PrintJob.objects.all()
    return render(request, 'printers/dashboard.html', {
        'printers': printers,
        'print_jobs': print_jobs
    })
class CustomUserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/create_user.html'  # Le template que tu vas créer
    success_url = reverse_lazy('login')  # Rediriger vers la page de login après création