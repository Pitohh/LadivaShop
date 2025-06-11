from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('manager_sales', 'Manager Sales'),
        ('manager_stock', 'Manager Stock'),
        ('cashier', 'Cashier'),
        ('client', 'Client'),
    ]
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)  # Utiliser l'email comme identifiant principal
    role = models.CharField(max_length=20, choices=ROLES, default='client')
    phone = models.CharField(max_length=15, blank=True)

    USERNAME_FIELD = 'email'  # Utiliser l'email comme identifiant principal
    REQUIRED_FIELDS = ['phone', 'role', 'username']  # Les champs obligatoires en plus de USERNAME_FIELD

    def __str__(self):
        return f"{self.username} ({self.email})"
