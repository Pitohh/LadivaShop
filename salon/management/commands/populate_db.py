import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from salon.models import Client, Product, SaleProduct, Service, Appointment, Sale
from account.models import User
import string

class Command(BaseCommand):
    help = "Remplit la base de données avec des données d'exemple."

    def handle(self, *args, **kwargs):
        # Créer un utilisateur administrateur si aucun n'existe
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username="admin", email="admin@example.com", password="admin123"
            )
            self.stdout.write("Utilisateur admin créé.")

        # 1. Clients
        clients = []
        for i in range(20):
            while True:
                # Générer un email aléatoire pour garantir l'unicité
                random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                email = f"client{i+1}_{random_suffix}@example.com"
                if not Client.objects.filter(email=email).exists():
                    break

            # Générer un numéro de téléphone unique aléatoire
            random_phone = f"012345678{random.randint(0, 99):02d}"
            while Client.objects.filter(telephone=random_phone).exists():
                random_phone = f"012345678{random.randint(0, 99):02d}"

            # Créer le client
            client = Client.objects.create(
                nom=f"Client {i+1}",
                email=email,
                telephone=random_phone,
            )
            clients.append(client)

        self.stdout.write(self.style.SUCCESS(f"{len(clients)} clients créés."))


        # 2. Produits
        produits = []
        for i in range(10):
            produit = Product.objects.create(
                nom=f"Produit {i+1}",
                description=f"Description pour le produit {i+1}",
                prix=random.uniform(10, 100),
                quantite=random.randint(1, 50),
            )
            produits.append(produit)
        self.stdout.write(self.style.SUCCESS(f"{len(produits)} produits créés."))

        # 3. Services
        services = []
        for i in range(10):
            service = Service.objects.create(
                nom=f"Service {i+1}",
                description=f"Description pour le service {i+1}",
                prix=random.uniform(20, 200),
                duree=timedelta(hours=random.randint(0, 2), minutes=random.randint(10, 59)),  # Utilise timedelta
            )
            services.append(service)
        self.stdout.write(self.style.SUCCESS(f"{len(services)} services créés."))

        # 4. Rendez-vous
        appointments = []
        for _ in range(50):
            appointment = Appointment.objects.create(
                client=random.choice(clients),
                service=random.choice(services),
                date=date.today() + timedelta(days=random.randint(-30, 30)),
                heure=f"{random.randint(9, 18):02d}:{random.randint(0, 59):02d}:00",
                statut=random.choice(['pending', 'confirmed', 'cancelled'])
            )
            appointments.append(appointment)
        self.stdout.write(self.style.SUCCESS(f"{len(appointments)} rendez-vous créés."))

        # 5. Ventes
        sales = []
        for _ in range(30):
            sale = Sale.objects.create(
                client=random.choice(clients),
                moyen_paiement=random.choice(["cash", "card", "mobile"]),
            )
            sale_products = []
            for produit in random.sample(produits, random.randint(1, 5)):
                sale_product = SaleProduct.objects.create(
                    sale=sale,
                    product=produit,
                    quantite=random.randint(1, 10)  # Set a random quantity between 1 and 10
                )
                sale_products.append(sale_product)
            sales.append(sale)
        self.stdout.write(self.style.SUCCESS(f"{len(sales)} ventes créées."))

        self.stdout.write(self.style.SUCCESS("Base de données remplie avec succès !"))
