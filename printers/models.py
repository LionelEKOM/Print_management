from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.template.defaultfilters import slugify
import string
import random
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    
    ADMIN = 'ADMIN'
    PERSONNEL = 'Personnel'
    
    MALE = 'M'
    FEMALE = 'F'
    
    ROLE_CHOICES = (
        (ADMIN, 'ADMIN'),
        (PERSONNEL, 'Personnel'),
    )
    
    SEX_CHOICES = (
        (MALE, 'Masculin'),
        (FEMALE, 'Feminin'),
    )
    
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
    sexe = models.CharField(max_length=10, choices=SEX_CHOICES, verbose_name='Sexe')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_on = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = "Utilisateur"
    def __str__(self):
        """
        Retourne une représentation lisible de l'objet CustomUser, à savoir son nom d'utilisateur.
        """
        
        return self.username
    
    def save(self, *args, **kwargs):
        # Générer un slug unique basé sur le username s'il n'existe pas
        if not self.slug:
            self.slug = slugify(self.username)
            # Vérifier l'unicité du slug
            while CustomUser.objects.filter(slug=self.slug).exists():
                random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
                self.slug = f"{self.slug}-{random_suffix}"

        # Ajouter l'utilisateur au groupe en fonction de son rôle
        super().save(*args, **kwargs)  # Appeler la méthode save du parent pour sauvegarder l'utilisateur
        if self.role == self.ADMIN:
            group, created = Group.objects.get_or_create(name='ADMIN')
            group.user_set.add(self)
        elif self.role == self.PERSONNEL:
            group, created = Group.objects.get_or_create(name='Personnel')
            group.user_set.add(self)
class Printer(models.Model):
    STATUS_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('PANNE', 'En panne'),
    ]
    name = models.CharField(max_length=100, verbose_name="Nom de l'imprimante")
    admin_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="managed_printers")  # Utilisateur qui gère l'imprimante
    ink_level = models.IntegerField(verbose_name="Niveau d'encre (%)")
    paper_remaining = models.IntegerField(verbose_name="Feuilles restantes")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Adresse de l'imprimante")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DISPONIBLE', verbose_name="Statut")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    created_on = models.DateTimeField(default=timezone.now, verbose_name="Date de création")  # Auto-enregistrer la date lors de la création
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = "Imprimante"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
class PrintJob(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="print_jobs")  # Utilisateur qui demande l'impression
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name='print_jobs', verbose_name="Imprimante")  # Imprimante utilisée
    # pages = models.IntegerField(verbose_name="Nombre de pages")
    copies = models.PositiveIntegerField(default=1, verbose_name="Nombre de copies")
    submitted_at = models.DateTimeField(default=timezone.now, verbose_name="Soumis le")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Terminé le")
    status = models.CharField(max_length=50, choices=[('PENDING', 'En attente'), ('COMPLETED', 'Terminé'), ('FAILED', 'Échoué')], default='PENDING', verbose_name="Statut de la tâche")
    document = models.FileField(upload_to='documents/', null=True, blank=True, verbose_name="Fichier à imprimer")  # Fichier téléchargé par l'utilisateur
    
    def __str__(self):
        """
        Afficher une représentation lisible de l'objet PrintJob, en incluant le nom du document, le nom de l'utilisateur et le nom de l'imprimante.
        """
        
        return f"Impression de {self.document.name} par {self.user.username} sur {self.printer.name}"

    
    