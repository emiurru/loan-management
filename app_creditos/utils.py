from datetime import datetime, timedelta, date
from django.shortcuts import render
from app_creditos.models import Credito, Lista_cuota, Pago, Cliente
from django.utils import timezone

import logging
import random

import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Max
from decimal import Decimal


def calcular_cuota(importe_credito, cuotas, tna):
    tasa_mensual = tna / 12 / 100
    importe_cuota = importe_credito * (tasa_mensual / (1 - (1 + tasa_mensual) ** -cuotas))
    return importe_cuota

def proximo_vencimiento(id):
    credito=Credito.objects.get(pk=id)
    cuotas = Lista_cuota.objects.filter(credito_id=id, estado='PENDIENTE')
    listado_cuotas = cuotas.first()
    prox_venc = listado_cuotas.fecha_vencimiento
    
    return prox_venc

def ultimo_pago(id):
    cuota_pagada = Lista_cuota.objects.filter(credito_id=id, pagos__isnull=False).aggregate(max_fecha_pago=Max('pagos__fecha_pago'))
    return cuota_pagada['max_fecha_pago'] if cuota_pagada['max_fecha_pago'] else None

def actualizar_creditos(id):
        cuotas = Lista_cuota.objects.filter(credito_id=id)        
        tasa_anual = Decimal('2.0') # puse una tna del 200%
        tasa_diaria = tasa_anual / Decimal('365')     
        
        for cuota in cuotas:
            if cuota.estado == "PAGADA":
                cuota.importe_actualizado = 0
                cuota.save()
            else:
                pagos = cuota.pagos.filter(fecha_pago__lte=date.today()).order_by('fecha_pago')
                saldo = Decimal(str(cuota.importe_cuota))
                fecha_inicio = cuota.fecha_vencimiento
                

                if cuota.fecha_vencimiento < date.today():
                    for pago in pagos:
                        # Calcular días vencidos hasta el pago
                        dias_vencidos = (pago.fecha_pago - fecha_inicio).days
                        interes = saldo * Decimal(str(tasa_diaria * dias_vencidos))                    
                        saldo = saldo + interes - Decimal(str(pago.monto_pagado))
                        fecha_inicio = pago.fecha_pago  # Actualizar fecha inicio para el próximo ciclo
                        
                    # Si después de todos los pagos, el saldo es mayor que cero y la fecha de inicio es anterior a hoy, calculamos el interés restante
                    if saldo > 0 and fecha_inicio < date.today():
                        dias_vencidos = (date.today() - fecha_inicio).days
                        interes = saldo * Decimal(str(tasa_diaria * dias_vencidos))
                        saldo += interes  # Actualizar saldo con intereses no pagados desde el último pago hasta hoy
                        
                    cuota.importe_actualizado = max(saldo, Decimal('0'))  # Asegurarse de que el importe actualizado no sea negativo
                else:
                    # Si la cuota no está vencida, el importe actualizado es el importe de la cuota
                    cuota.importe_actualizado = cuota.importe_cuota

                cuota.save()
                     
        credito = Credito.objects.get(id=id)            
        cuotas_pendientes = credito.lista_cuotas.filter(estado='PENDIENTE').count()
        credito.cuotas_restante = cuotas_pendientes
       
       
        

        credito.save()
