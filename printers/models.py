from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.template.defaultfilters import slugify

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
    sexe = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name='Sexe')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_on = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = "Utilisateur"
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role == self.ADMIN:
            group = Group.objects.get(name='ADMIN')
            group.user_set.add(self)
        elif self.role == self.PERSONNEL:
            group = Group.objects.get(name='Personnel')
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
    created_on = models.DateField(blank=True, null=True, verbose_name="Date de création")
    
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
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name="print_jobs")  # Imprimante utilisée
    pages = models.IntegerField(verbose_name="Nombre de pages")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de la tâche")
    status = models.CharField(max_length=50, choices=[('PENDING', 'En attente'), ('COMPLETED', 'Terminé'), ('FAILED', 'Échoué')], default='PENDING', verbose_name="Statut de la tâche")
    file = models.FileField(upload_to='uploads/', null=True, blank=True, verbose_name="Fichier à imprimer")  # Fichier téléchargé par l'utilisateur
    
    def __str__(self):
        return f"Tâche d'impression de {self.user.username} sur {self.printer.name}"

    
    