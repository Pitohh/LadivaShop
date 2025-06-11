from django.db import models

# Client model
class Client(models.Model):
    nom = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.nom

class Product(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField(default=0)
    limite_stock = models.PositiveIntegerField(default=10)  # Ajouter un champ pour la limite de stock
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Ajouter le champ image

    def __str__(self):
        return self.nom

    @property
    def stock_status(self):
        if self.quantite == 0:
            return "Indisponible"
        elif self.quantite <= self.limite_stock:
            return "Low on stock"
        else:
            return "En stock"


# Service model
class Service(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    duree = models.DurationField()
    image = models.ImageField(upload_to='services/', blank=True, null=True)  # Ajouter le champ image

    def __str__(self):
        return self.nom

# Appointment model
class Appointment(models.Model):
    STATUTS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    heure = models.TimeField()
    statut = models.CharField(max_length=20, choices=STATUTS, default='pending')

    def __str__(self):
        return f"Rendez-vous pour {self.client.nom} - {self.service.nom}"

    class Meta:
        ordering = ['date', 'heure']  # Tri par défaut

# Sale model
class Sale(models.Model):
    client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name="sales")  # Vente associée à un client
    produits = models.ManyToManyField("Product", through="SaleProduct", related_name="products")  # Produits vendus
    moyen_paiement = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)  # Date et heure de la vente

    @property
    def total(self):
        return sum(item.total_price() for item in self.sale_products.all())  # Calcul du total
    
    def get_product_list(self):
        return [str(item.product) for item in self.sale_products.all()]  # Récupérer la liste des produits vendus

    def __str__(self):
        return f"Vente #{self.id} - {self.client.nom} ({self.date.strftime('%Y-%m-%d %H:%M')})"

# Sale Product model
class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="sale_products")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    def total_price(self):
        return self.quantite * self.product.prix

    def __str__(self):
        return f"{self.quantite}x {self.product.nom}"

class SaleService(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="sale_services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service.nom} (Vente #{self.sale.id})"
