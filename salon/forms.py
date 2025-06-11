from django import forms
from .models import Sale, SaleProduct, Client, SaleService

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["client", "moyen_paiement"]

class SaleProductForm(forms.ModelForm):
    class Meta:
        model = SaleProduct
        fields = ["product", "quantite"]

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["nom", "email", "telephone"]


class SaleServiceForm(forms.ModelForm):
    class Meta:
        model = SaleService
        fields = ["service"]
