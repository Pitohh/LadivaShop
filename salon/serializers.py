from rest_framework import serializers
from .models import Client, Product, Service, Appointment, Sale, SaleProduct


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'nom', 'email', 'telephone']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'nom', 'description', 'prix', 'quantite', 'limite_stock', 'image', 'stock_status']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'nom', 'description', 'prix', 'duree', 'image']


class AppointmentSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.nom', read_only=True)
    service_nom = serializers.CharField(source='service.nom', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'client', 'client_nom', 'service', 'service_nom', 'date', 'heure', 'statut']


class SaleProductSerializer(serializers.ModelSerializer):
    product_nom = serializers.CharField(source='product.nom', read_only=True)

    class Meta:
        model = SaleProduct
        fields = ['id', 'sale', 'product', 'product_nom', 'quantite']


class SaleSerializer(serializers.ModelSerializer):
    produits_details = SaleProductSerializer(source='saleproduct_set', many=True, read_only=True)
    total_calculated = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'produits_details', 'total', 'total_calculated', 'moyen_paiement', 'date']

    def get_total_calculated(self, obj):
        return sum(item.total_price() for item in obj.saleproduct_set.all())
