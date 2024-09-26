from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

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
