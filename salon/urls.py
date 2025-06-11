from django.urls import path
from .views import (
    ClientViewSet,
    ProductViewSet,
    ServiceViewSet,
    AppointmentViewSet,
    SaleViewSet,
    add_client,
    dashboard_view,
    appointment_view,
    client_view,
    product_view,
    sales_view,
    services_view,
    pos_view,
)

urlpatterns = [
    # Tableau de bord
    path('', dashboard_view, name='dashboard'),

    # Clients
    path('api/clients/', ClientViewSet.as_view({'get': 'list', 'post': 'create'}), name='client-list-create'),
    path('api/clients/<int:pk>/', ClientViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='client-detail'),

    # Produits
    path('api/products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list-create'),
    path('api/products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-detail'),

    # Services
    path('api/services/', ServiceViewSet.as_view({'get': 'list', 'post': 'create'}), name='service-list-create'),
    path('api/services/<int:pk>/', ServiceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='service-detail'),

    # Appointments
    path('api/appointments/', AppointmentViewSet.as_view({'get': 'list', 'post': 'create'}), name='appointment-list-create'),
    path('api/appointments/<int:pk>/', AppointmentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='appointment-detail'),
    path('api/appointments/<int:pk>/update_status/', AppointmentViewSet.as_view({'patch': 'update_status'}), name='appointment-update-status'),

    # Ventes
    path('api/sales/', SaleViewSet.as_view({'get': 'list', 'post': 'create'}), name='sale-list-create'),
    path('api/sales/<int:pk>/', SaleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='sale-detail'),
    path('api/sales/<int:pk>/products/', SaleViewSet.as_view({'get': 'products'}), name='sale-products'),

    # Vues de l'application
    path('appointments/', appointment_view, name='appointment_view'),
    path('clients/', client_view, name='client_view'),
    path('products/', product_view, name='product_view'),
    path('sales/', sales_view, name='sales_view'),
    path('services/', services_view, name='services_view'),
    path('pos/', pos_view, name='pos_view'),
    path("add_client/", add_client, name="add_client"),
]
