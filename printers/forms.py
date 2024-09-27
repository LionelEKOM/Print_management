from django import forms
from .models import CustomUser, PrintJob, Printer
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'sexe', 'password1', 'password2']
        
        # Personnalisation des labels et des messages d'erreur
        labels = {
            'username': _('Nom d\'utilisateur'),
            'first_name': _('Prénom'),
            'last_name': _('Nom de famille'),
            'email': _('Adresse e-mail'),
            'role': _('Rôle'),
            'sexe': _('Sexe'),
            'password1': _('Mot de passe'),
            'password2': _('Confirmation du mot de passe'),
        }

        error_messages = {
            'username': {
                'required': _('Le nom d\'utilisateur est obligatoire.'),
                'max_length': _('Le nom d\'utilisateur ne peut pas dépasser 150 caractères.'),
            },
            'email': {
                'invalid': _('Veuillez entrer une adresse e-mail valide.'),
                'required': _('L\'adresse e-mail est obligatoire.'),
            },
            'password1': {
                'required': _('Le mot de passe est obligatoire.'),
            },
            'password2': {
                'required': _('Veuillez confirmer votre mot de passe.'),
                'password_mismatch': _('Les mots de passe ne correspondent pas.'),
            },
        }
        
    # Personnaliser l'initialisation pour ajouter des classes CSS ou d'autres attributs aux champs
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
         # Personnaliser l'apparence des champs
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label

class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ['name', 'ink_level', 'paper_remaining', 'address', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control mb-3", 
                'placeholder': 'Nom de l’imprimante'
            }),
            'ink_level': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Niveau d\'encre (%)'
            }),
            'paper_remaining': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre de feuilles restantes'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Adresse de l’imprimante (192.168.0.xxx)'
            }),
            'status': forms.Select(attrs={
                'class': "form-control mb-3", 
            }),
        }
            
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Récupérer l'utilisateur connecté
        super().__init__(*args, **kwargs)
        
    def clean_ink_level(self):
        ink_level = self.cleaned_data.get('ink_level')
        if not (0 < ink_level <= 100):
            raise ValidationError("Le niveau d'encre doit être compris entre 1 et 100.")
        return ink_level
    
    def clean_paper_remaining(self):
        paper_remaining = self.cleaned_data.get('paper_remaining')
        if paper_remaining <= 0:
            raise ValidationError("Le nombre de feuilles restantes doit être supérieur à 0.")
        return paper_remaining
    
    def clean_address(self):
        address = self.cleaned_data.get('address')
        # Valider l'adresse sous le format "192.168.xxx.xxx"
        if not re.match(r'^192\.168\.\d{1,3}\.\d{1,3}$', address):
            raise ValidationError("L'adresse doit être au format '192.168.xxx.xxx'.")
        return address
            
    def save(self, commit=True):
        printer = super().save(commit=False)
        if self.user:
            printer.admin_user = self.user  # Attribuer l'utilisateur connecté comme admin_user
        if commit:
            printer.save()
        return printer
    
class PrintJobForm(forms.ModelForm):
    class Meta:
        model = PrintJob
        fields = ['printer', 'document', 'copies']
        widgets = {
            'printer': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'copies': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Nombre de copies'}),
        }
        labels = {
            'printer': 'Choisissez une imprimante',
            'document': 'Document à imprimer',
            'copies': 'Nombre de copies',
        }

    def clean_document(self):
        document = self.cleaned_data.get('document')
        # Ajouter une validation pour le format de fichier si nécessaire
        if not document.name.endswith(('.pdf', '.docx', '.txt')):
            raise forms.ValidationError("Le format de fichier n'est pas supporté. Veuillez uploader un fichier PDF, DOCX ou TXT.")
        return document