import random
import string
from django.core.management.base import BaseCommand
from account.models import User  

class Command(BaseCommand):
    help = "Crée un utilisateur pour chaque rôle défini dans le modèle User."

    def generate_password(self, length=10):
        """Génère un mot de passe aléatoire."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def handle(self, *args, **kwargs):
        roles = ['owner', 'admin', 'manager_sales', 'manager_stock', 'cashier', 'client']
        users_created = 0

        for role in roles:
            email = f"{role}@example.com"
            username = role.replace("_", "").capitalize()
            password = self.generate_password()

            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role=role
                )
                self.stdout.write(self.style.SUCCESS(f"Utilisateur {username} ({role}) créé avec succès. 📩 {email} | 🔑 {password}"))
                users_created += 1

        if users_created == 0:
            self.stdout.write(self.style.WARNING("Tous les utilisateurs existent déjà. Aucune création effectuée."))
        else:
            self.stdout.write(self.style.SUCCESS(f"{users_created} utilisateurs créés avec succès. 🚀"))
