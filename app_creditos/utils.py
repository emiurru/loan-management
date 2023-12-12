from datetime import datetime, timedelta
from django.shortcuts import render

def calcular_cuota(importe_credito, cuotas, tna):
    tasa_mensual = tna / 12 / 100
    importe_cuota = importe_credito * (tasa_mensual / (1 - (1 + tasa_mensual) ** -cuotas))
    return importe_cuota