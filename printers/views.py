from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from printers.forms import CustomUserCreationForm, PrintJobForm, PrinterForm
from printers.models import CustomUser, PrintJob, Printer
from django import forms
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

# Dans Django, par sécurité, les champs liés au mot de passe ne sont jamais pré-remplis lors 
# de l'édition d'un utilisateur, 
# même si l'utilisateur a déjà un mot de passe. 
# C'est une bonne pratique pour éviter d'exposer les mots de passe existants dans les formulaires.
class CustomUserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/edit_user.html'
    success_url = reverse_lazy('user_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Un utilisateur avec ce nom d'utilisateur existe déjà.")
        return username
    
    def form_valid(self, form):
        # Enregistrer l'utilisateur
        response = super().form_valid(form)
        # Ajouter un message de confirmation
        username = form.cleaned_data.get('username')
        messages.success(self.request, f"Utilisateur {username} a été édité avec succès !")
        return response
    
class CustomUserDetailView(DetailView):
    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'user'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
class PrinterCreateView(CreateView):
    model = Printer
    form_class = PrinterForm  # Utilise PrinterForm si tu as un formulaire personnalisé
    template_name = 'printers/create_printer.html'
    success_url = reverse_lazy('dashboard')  # Rediriger après la création
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Passer l'utilisateur connecté
        return kwargs

    def form_valid(self, form):
        printer = form.save(commit=False)
        printer.save()
        return super().form_valid(form)
    
    def form_valid(self, form):
        # Enregistrer l'utilisateur
        response = super().form_valid(form)
        # Ajouter un message de confirmation
        messages.success(self.request, f"imprimante a été créé avec succès !")
        return response

class PrinterUpdateView(UpdateView):
    model = Printer
    form_class = PrinterForm  # Assure-toi que tu as un formulaire approprié
    template_name = 'printers/edit_printer.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return Printer.objects.get(slug=self.kwargs['slug'])  # Récupérer par slug
    
    def form_valid(self, form):
        # Enregistrer l'imprimante
        response = super().form_valid(form)
        name = form.cleaned_data.get('name')
        # Ajouter un message de confirmation
        messages.success(self.request, f"imprimante {name} a édité avec succès !")
        return response
    
class PrintJobCreateView(LoginRequiredMixin, CreateView):
    model = PrintJob
    form_class = PrintJobForm
    template_name = 'printers/print_job_form.html'
    success_url = reverse_lazy('print_job_list')  # Rediriger vers une page où les utilisateurs peuvent voir leurs travaux d'impression

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associer l'utilisateur connecté au travail d'impression
        messages.success(self.request, "Votre travail d'impression a été soumis avec succès!")
        return super().form_valid(form)
    
class PrintJobListView(LoginRequiredMixin, ListView):
    model = PrintJob
    template_name = 'printers/print_job_list.html'
    context_object_name = 'print_jobs'

    def get_queryset(self):
        return PrintJob.objects.filter(user=self.request.user).order_by('-submitted_at')