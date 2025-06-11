import logging
from django.forms import formset_factory
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from collections import defaultdict
from datetime import date, timedelta
from django.db.models import Sum, Count, F
from django.shortcuts import get_object_or_404, redirect, render
from account.permissions import IsManagerSales, IsManagerStock
from salon.forms import ClientForm, SaleForm, SaleProductForm, SaleServiceForm
from salon.models import Appointment, Sale, Client, Product

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from django.core.paginator import Paginator

from .models import Client, Product, SaleService, Service, Appointment, Sale, SaleProduct
from .serializers import (
    ClientSerializer, ProductSerializer, ServiceSerializer, 
    AppointmentSerializer, SaleSerializer, SaleProductSerializer
)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Configuration du logger
logger = logging.getLogger(__name__)

# Permission personnalisée : seulement les administrateurs peuvent accéder
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'owner']



class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['nom', 'email', 'telephone']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsManagerStock]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['nom', 'description']

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('date', 'heure')
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        appointment = self.get_object()
        new_status = request.data.get('statut')
        if new_status in dict(Appointment.STATUTS):
            appointment.statut = new_status
            appointment.save()
            return Response({'message': 'Statut mis à jour', 'statut': new_status}, status=status.HTTP_200_OK)
        return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by("-date")
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsManagerSales]

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        sale = self.get_object()
        products = SaleProduct.objects.filter(sale=sale)
        serializer = SaleProductSerializer(products, many=True)
        return Response(serializer.data)
    
@login_required
def dashboard_view(request):
    username = request.user.username

    today = date.today()
    tomorrow = today + timedelta(days=1)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Rendez-vous
    appointments_today = Appointment.objects.filter(date=today)
    appointments_tomorrow = Appointment.objects.filter(date=tomorrow)
    appointments_week = Appointment.objects.filter(date__range=[start_of_week, end_of_week])
    appointments_month = Appointment.objects.filter(date__range=[start_of_month, end_of_month])

    # Total des ventes (corrigé)
    sales_today = SaleProduct.objects.filter(sale__date__date=today).aggregate(
        total=Sum(F('quantite') * F('product__prix'))
    )['total'] or 0

    sales_week = SaleProduct.objects.filter(sale__date__date__range=[start_of_week, end_of_week]).aggregate(
        total=Sum(F('quantite') * F('product__prix'))
    )['total'] or 0

    sales_month = SaleProduct.objects.filter(sale__date__date__range=[start_of_month, end_of_month]).aggregate(
        total=Sum(F('quantite') * F('product__prix'))
    )['total'] or 0

    # Total clients
    clients_today = Client.objects.filter(appointments__date=today).distinct().count()
    clients_week = Client.objects.filter(appointments__date__range=[start_of_week, end_of_week]).distinct().count()
    clients_month = Client.objects.filter(appointments__date__range=[start_of_month, end_of_month]).distinct().count()

    # Produits en faible stock
    low_stock_products = Product.objects.filter(quantite__lte=F('limite_stock'))

    context = {
        'username': username,
        'appointments': {
            'today': appointments_today,
            'tomorrow': appointments_tomorrow,
            'week': appointments_week,
            'month': appointments_month,
        },
        'sales': {
            'today': sales_today,
            'week': sales_week,
            'month': sales_month,
        },
        'clients': {
            'today': clients_today,
            'week': clients_week,
            'month': clients_month,
        },
        'low_stock_products': low_stock_products,
    }

    return render(request, 'dashboard.html', context)

@login_required
def appointment_view(request):
    appointments = Appointment.objects.all().order_by('date', 'heure')
    appointments_by_date = defaultdict(list)
    for appointment in appointments:
        appointments_by_date[appointment.date].append(appointment)
    return render(request, 'appointment.html', {
        'appointments_by_date': dict(appointments_by_date),
        'clients': Client.objects.all(),
        'services': Service.objects.all()
    })
    
@login_required
def product_view(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'product.html', context)

@login_required
def client_view(request):
    search_query = request.GET.get('search', '')

    # Filtrer les clients par nom si une recherche est faite
    if search_query:
        clients = Client.objects.filter(nom__icontains=search_query)
    else:
        clients = Client.objects.all()

    # Pagination : 10 clients par page
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'clients': page_obj,  # Liste paginée des clients
        'search_query': search_query
    }
    return render(request, 'client.html', context)


@login_required
def sales_view(request):
    sales = Sale.objects.prefetch_related("sale_products__product", "sale_services__service").order_by("-date")
    for sale in sales:
        total_products = sum(sp.total_price() for sp in sale.sale_products.all())
        total_services = sum(ss.service.prix for ss in sale.sale_services.all())
        sale.total_sale = total_products + total_services
    return render(request, 'sales.html', {'sales': sales})

@login_required
def services_view(request):
    context = {
        'services': Service.objects.all(),
    }
    return render(request, 'services.html', context)


@login_required
def pos_view(request):
    SaleProductFormSet = formset_factory(SaleProductForm, extra=1)
    SaleServiceFormSet = formset_factory(SaleServiceForm, extra=1)
    if request.method == "POST":
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            sale = sale_form.save()
            return redirect("sales_view")
    return render(request, "pos.html", {
        "sale_form": SaleForm(),
        "product_formset": SaleProductFormSet(),
        "service_formset": SaleServiceFormSet(),
        "products": Product.objects.all(),
        "services": Service.objects.all(),
        "clients": Client.objects.all()
    })

@csrf_exempt
def add_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return JsonResponse({
                "success": True,
                "client_id": client.id,
                "client_name": client.nom
            })
    return JsonResponse({"success": False})
