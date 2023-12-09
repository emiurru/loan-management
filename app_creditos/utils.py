from datetime import datetime, timedelta
from django.shortcuts import render

def calcular_descuento_cheque(monto, tna, fecha_deposito):
    # Calcular los días hasta la fecha de depósito
    fecha_actual = datetime.now().date()
    dias = (fecha_deposito - fecha_actual).days

       # Calcular el valor descontado del cheque
    valor_descontado = int(monto - (tna / 360 * dias) * monto)

    return valor_descontado

def calcular_fecha_vencimiento(fecha, mes):
    # Se agrega 1 mes a la fecha de vencimiento anterior
    fecha_vencimiento = fecha + timedelta(days=30*mes)
    return fecha_vencimiento
