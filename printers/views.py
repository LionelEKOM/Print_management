from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic import ListView, DetailView
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
    success_url = reverse_lazy('create_user')  # Rediriger vers la page de login après création
    
    def form_valid(self, form):
        # Enregistrer l'utilisateur
        response = super().form_valid(form)
        # Ajouter un message de confirmation
        username = form.cleaned_data.get('username')
        messages.success(self.request, f"Utilisateur {username} créé avec succès !")
        return response
    
class UserListView(ListView):
    model = CustomUser
    template_name = 'users/user_list.html'  # Le template que tu vas créer
    context_object_name = 'users'  # Nom du contexte utilisé dans le template
    paginate_by = 10  # Paginer si tu as beaucoup d'utilisateurs
    
class CustomUserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/edit_user.html'
    success_url = reverse_lazy('user_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
class CustomUserDetailView(DetailView):
    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'user'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'