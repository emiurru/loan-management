from typing import Any, Dict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from app_creditos.models import Cliente, Tipo_Credito, Credito, Lista_cuota, Pago
from .utils import calcular_cuota, actualizar_creditos
from datetime import datetime, timedelta, date
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from dateutil.relativedelta import relativedelta
from django.contrib import messages


# VISTAS CLIENTES

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'app_creditos/lista_clientes.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        busqueda = self.request.GET.get('busqueda', '')
        queryset = queryset.filter(apellido__icontains=busqueda)
        return queryset

def crear_cliente(request):
    if request.method == "POST":
        dni = request.POST.get('dni')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        tel_fijo = request.POST.get('tel_fijo')
        celular = request.POST.get('celular')
        email = request.POST.get('email')

        cliente = Cliente(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            tel_fijo=tel_fijo,
            celular=celular,
            email=email
        )
        cliente.save()

        return redirect('lista_clientes')
    
    return render(request, 'app_creditos/cliente_create.html')

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    success_url = reverse_lazy('lista_clientes')

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ('fecha_nacimiento', 'tel_fijo', 'celular', 'email')
    
    def get_success_url(self):
        return reverse_lazy('ver_clientes', kwargs={'pk': self.object.pk})

def eliminar_cliente(request, pk):

    cliente=Cliente.objects.get(pk=pk)
    cliente.delete()

    return redirect('lista_clientes') 

def eliminar_credito(request, pk):

    credito=Credito.objects.get(pk=pk)
    credito.delete()

    return redirect('lista_creditos') 

# VISTAS TIPOS DE CREDITOS
class Tipo_creditoListView(ListView):
    model = Tipo_Credito
    template_name = 'app_creditos/lista_tipo_creditos.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        busqueda = self.request.GET.get('busqueda', '')
        queryset = queryset.filter(nombre_credito__icontains=busqueda)
        return queryset

def crear_tipo_credito(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_credito')
        tna = request.POST.get('tna')

        tipo_credito = Tipo_Credito(nombre_credito=nombre, interes=tna)
        tipo_credito.save()

        return redirect('lista_tipo_creditos')
    
    return render(request, 'app_creditos/tipo_credito_create.html')

class Tipo_creditoDetailView(DetailView):
    model = Tipo_Credito
    success_url = reverse_lazy('lista_tipo_creditos')

class Tipo_creditoUpdateView(LoginRequiredMixin, UpdateView):
    model = Tipo_Credito
    fields = ('nombre_credito', 'interes')
    
    def get_success_url(self):
        return reverse_lazy('ver_tipo_creditos', kwargs={'pk': self.object.pk})
    
def eliminar_tipo_credito(request, pk):

    tipo_credito=Tipo_Credito.objects.get(pk=pk)
    tipo_credito.delete()

    return redirect('lista_tipo_creditos') 

#VISTAS DE CREDITOS

class CreditoListView(LoginRequiredMixin, ListView):
    model = Credito
    template_name = 'app_creditos/lista_creditos.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        busqueda = self.request.GET.get('busqueda', '')               
        queryset = queryset.filter(tipo_credito__nombre_credito__icontains=busqueda)
       
        return queryset
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        
        context['clientes'] = Cliente.objects.all()
        context['tipos_creditos'] = Tipo_Credito.objects.all()

        return context

def crear_credito(request):    
    if request.method == "POST":
        importe_credito = int(request.POST.get('importe_credito'))
        cuotas = int(request.POST.get('cuotas'))
        cliente_id = request.POST.get('cliente')
        id_tipo_credito = request.POST.get('tipo_credito') 

        tipo_credito = Tipo_Credito.objects.get(id=id_tipo_credito)
       
        tna = tipo_credito.interes
        importe_cuota = calcular_cuota(importe_credito, cuotas, tna)

        cliente = Cliente.objects.get(id=cliente_id)
        clientes = Cliente.objects.all()
        tipos_credito = Tipo_Credito.objects.all()

        credito = Credito(
            importe_credito=importe_credito,
            cuotas = cuotas,
            cliente = cliente,
            tipo_credito = tipo_credito,
            importe_cuota = importe_cuota
        )
        credito.save()
        
        for num_cuota in range(1, int(cuotas) + 1):
                    fecha_vencimiento = date.today() + relativedelta(months=+num_cuota-1)
                    
                    Lista_cuota.objects.update_or_create(
                        credito=credito,
                        numero_cuota=num_cuota,
                        defaults={
                            'importe_cuota': importe_cuota,
                            'fecha_vencimiento': fecha_vencimiento
                        }
                    )

        return redirect('lista_creditos')
    
    return render(request, 'app_creditos/lista_creditos.html')

class CreditoDetailView(LoginRequiredMixin, DetailView):
    model = Credito
    success_url = reverse_lazy('lista_creditos')
    
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        credito = context['object']

        cuotas = credito.lista_cuotas.all()
        context['cuotas'] = cuotas

        hoy_local = timezone.localtime(timezone.now())
        fecha_hoy = hoy_local.date().strftime('%Y-%m-%d')

        context['fecha_hoy'] = fecha_hoy
        pagos_por_cuota = {cuota.id: cuota.pagos.all() for cuota in cuotas}
        context['pagos_por_cuota'] = pagos_por_cuota

        deuda = 0
        pago_credito = 0
        for cuota in cuotas:
            total_pagado = sum(pago.monto_pagado for pago in cuota.pagos.all())
            mora = max(0, total_pagado - cuota.importe_cuota)
            cuota.total_pagado = total_pagado
            cuota.mora = mora
            pago_credito += total_pagado

            
            if cuota.estado == 'PENDIENTE' and cuota.importe_actualizado is not None:
                deuda += cuota.importe_actualizado
            
        context['deuda'] = deuda
        context['pago_credito'] = pago_credito

        return context
      
class CreditoUpdateView(LoginRequiredMixin, UpdateView):
    model = Credito
    fields = ('importe_cuota', 'tipo_credito', 'cuotas', 'importe_credito')
    success_url = reverse_lazy('lista_creditos')

class CreditoDeleteView(LoginRequiredMixin, DeleteView):
    model = Credito
    success_url = reverse_lazy('lista_creditos')

def registrar_pago(request, cuota_id):
    cuota = get_object_or_404(Lista_cuota, pk=cuota_id)
    credito_id = cuota.credito.id
    
    if request.method == 'POST':
        try:
            fecha_pago = request.POST.get('fecha_pago')
            monto_pagado = request.POST.get('monto_pagado')
            medio_pago = request.POST.get('medio_pago')
            tipo_pago = request.POST.get('tipo_pago')
            # Crear el objeto de Pago y guardar
            pago = Pago(
                cuota=cuota,
                monto_pagado=monto_pagado,
                fecha_pago=fecha_pago,
                medio_pago=medio_pago,
                tipo_pago=tipo_pago
            )
            pago.save()
            
            # Actualizar el estado de la cuota si el pago es total o saldo cuota
            if tipo_pago in ['Total', 'Pago Saldo']:
                cuota.estado = 'PAGADA'
                cuota.save()
                
            actualizar_creditos(credito_id)
            
            return redirect('ver_creditos', pk=credito_id)
        
        except Exception as e:
            messages.error(request, f'Se produjo un error al registrar el pago: {e}')
            return redirect('ver_creditos', pk=credito_id)
        
def actualizar_credito_individual(request, pk):

    if request.method == 'POST':
        actualizar_creditos(pk)
        
        return redirect('ver_creditos', pk=pk)
    
def borrar_pago(request, id_pago):
    pago = get_object_or_404(Pago, pk=id_pago)
    
    cuota = pago.cuota
    credito_id = cuota.credito.id

    if request.method == 'POST':
        pago.delete()
        cuota.estado = 'PENDIENTE'
        cuota.save()
        actualizar_creditos(credito_id)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))