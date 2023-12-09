from django.contrib import admin

from .models import Cliente, Tipo_Credito, Credito

admin.site.register(Cliente)
admin.site.register(Tipo_Credito)
admin.site.register(Credito)
