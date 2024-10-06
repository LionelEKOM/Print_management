from django.test import TestCase
from .models import Printer
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils import timezone
from printers.models import CustomUser  # Import du modèle CustomUser

class PrinterModelTest(TestCase):
    def setUp(self):
        # Crée un utilisateur admin pour tester avec le modèle CustomUser
        """
        Crée un utilisateur admin pour tester avec le modèle CustomUser.
        """
        
        self.user = CustomUser.objects.create_user(username='admin', password='admin123')

    def test_create_printer(self):
        """
        Test que l'on peut créer une imprimante en enregistrant correctement
        les informations.
        """
        printer = Printer.objects.create(
            name="HP LaserJet",
            admin_user=self.user,
            ink_level=80,
            paper_remaining=200,
            address="Bureau A23",
            status="EN LIGNE"
        )
        self.assertEqual(printer.name, "HP LaserJet")
        self.assertEqual(printer.ink_level, 80)
        self.assertEqual(printer.paper_remaining, 200)
        self.assertEqual(printer.address, "Bureau A23")
        self.assertEqual(printer.status, "EN LIGNE")
        
class CustomUserCreateViewTest(TestCase):

    def test_user_creation(self):
        # Données pour la création d'un utilisateur, y compris 'role' et 'sexe'
        """
        Test de la création d'un utilisateur avec les données valides.

        Vérifie que l'utilisateur est bien créé, que la redirection est correcte
        et qu'un message de succès est affiché.
        """
        data = {
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newuser@example.com',
            'role': 'ADMIN',  # Ajouter le rôle ici (par exemple : 'admin')
            'sexe': 'M',  # Ajouter le sexe ici (par exemple : 'M' pour masculin, 'F' pour féminin)
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        }

        # Envoyer une requête POST à l'URL de création d'utilisateur
        response = self.client.post(reverse('create_user'), data)

        # Vérifier le statut de la réponse et afficher les erreurs du formulaire si la création échoue
        if response.status_code == 200:
            print(response.context['form'].errors)  # Affiche les erreurs du formulaire pour débogage

        # Vérifier que la redirection est correcte après la création
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.assertRedirects(response, reverse('create_user'))  # Vérifier la redirection vers l'URL spécifiée

        # Vérifier si l'utilisateur a bien été créé
        user_exists = CustomUser.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists)  # L'utilisateur doit exister dans la base de données

        # Vérifier le message de succès
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  # Il devrait y avoir un seul message
        self.assertEqual(str(messages[0]), "Utilisateur newuser créé avec succès !")
