from django.db import models
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta


class Cliente(models.Model):
    apellido = models.CharField(max_length=256)
    nombre = models.CharField(max_length=256)
    dni = models.CharField(max_length=32, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    tel_fijo = models.CharField(max_length=32, null=True, blank=True)
    celular = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField()
    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clientes_creados')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)   
    
    def __str__(self) -> str:
        return f'{self.apellido}  {self.nombre}'

class Tipo_Credito(models.Model):
    nombre_credito = models.CharField(max_length=256)
    interes = models.FloatField()
    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.nombre_credito}. Tasa de interes = {self.interes*100}%'

class Credito(models.Model):
    importe_credito = models.IntegerField()
    cuotas = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    importe_cuota = models.IntegerField(null=True)
    tipo_credito = models.ForeignKey(Tipo_Credito, on_delete=models.CASCADE, null=True)
    fecha = models.DateField(null=True, blank=True)
    fecha_otorgamiento = models.DateField(auto_now_add=True, null=True)
    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    

    def __str__(self) -> str:
        return f'{self.id} - {self.cliente} - Monto: {self.importe_credito} - Cuotas: {self.cuotas}'
    
    def save(self, *args, **kwargs):
        importe_credito = self.importe_credito
        cuotas = self.cuotas
        importe_cuota = self.importe_cuota
        
        super().save(*args, **kwargs)
        
        return importe_cuota
    
class Lista_cuota(models.Model):
    credito = models.ForeignKey(Credito, on_delete=models.CASCADE, related_name='lista_cuotas')
    numero_cuota = models.IntegerField()
    importe_cuota = models.IntegerField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)    
    fecha_pago = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=[('Pendiente', 'Pendiente'), ('Pagada', 'Pagada')], default='Pendiente')
            
