
from django.urls import re_path
from django.shortcuts import redirect
from django.contrib import admin
from .models import Client, Product, Service, Appointment, Sale, SaleProduct

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone')
    search_fields = ('nom', 'email')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'prix', 'quantite')
    search_fields = ('nom',)
    list_filter = ('prix',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'prix', 'duree')
    search_fields = ('nom',)
    list_filter = ('prix',)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'date', 'heure', 'statut')
    search_fields = ('client__nom', 'service__nom')
    list_filter = ('date', 'statut')
    date_hierarchy = 'date'
    
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'date', 'heure', 'statut')
    search_fields = ('client__nom', 'service__nom')
    list_filter = ('date', 'statut')
    date_hierarchy = 'date'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(r'^custom-view/$', self.admin_site.admin_view(self.custom_view), name='appointment_custom_view'),
        ]
        return custom_urls + urls

    def custom_view(self, request):
        return redirect('appointment_view')


class SaleProductInline(admin.TabularInline):
    model = SaleProduct
    extra = 1

class SaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'total', 'moyen_paiement')
    search_fields = ('date', 'moyen_paiement')
    inlines = [SaleProductInline]

admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Sale, SaleAdmin)
