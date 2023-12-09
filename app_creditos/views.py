from typing import Any, Dict
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from app_creditos.models import Cliente, Tipo_Credito, Credito, Lista_cuota, CobroCuota
from .utils import calcular_descuento_cheque
from datetime import datetime, timedelta
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse


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

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    success_url = reverse_lazy('lista_clientes')

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
    
class Tipo_creditoDeleteView(LoginRequiredMixin, DeleteView):
    model = Tipo_Credito
    success_url = reverse_lazy('lista_tipo_creditos')

#VISTAS DE CREDITOS

class CreditoListView(LoginRequiredMixin, ListView):
    model = Credito
    template_name = 'app_creditos/lista_creditos.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        busqueda = self.request.GET.get('busqueda', '')
               
        queryset = queryset.filter(tipo_credito__nombre_credito__icontains=busqueda)
       
        return queryset
     
class CreditoCreateView(LoginRequiredMixin, CreateView):
    model = Credito
    fields = ('cliente', 'importe_credito', 'tipo_credito', 'cuotas', 'importe_cuota')
    success_url = reverse_lazy('lista_creditos')

class CreditoDetailView(LoginRequiredMixin, DetailView):
    model = Credito
    success_url = reverse_lazy('lista_creditos')
    
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        credito = context['object']

        cuotas = credito.lista_cuotas.all()
        context['cuotas'] = cuotas
        return context
      
class CreditoUpdateView(LoginRequiredMixin, UpdateView):
    model = Credito
    fields = ('importe_cuota', 'tipo_credito', 'cuotas', 'importe_credito')
    success_url = reverse_lazy('lista_creditos')

class CreditoDeleteView(LoginRequiredMixin, DeleteView):
    model = Credito
    success_url = reverse_lazy('lista_creditos')

#COBRO CUOTAS
def registrar_cobro_cuota(request):
    if request.method == 'POST':
        credito_id = request.POST.get('credito_id')
        numero_cuota = request.POST.get('numero_cuota')
        fecha_pago = request.POST.get('fecha_pago')
        monto_pago = request.POST.get('monto_pago')

        try:
            credito = Credito.objects.get(id=credito_id)
            cuota = credito.lista_cuotas.get(numero_cuota=numero_cuota)
        except (Credito.DoesNotExist, Lista_cuota.DoesNotExist):
            # Manejar el caso cuando el crédito o la cuota no existen
            return HttpResponse('Error: Crédito o cuota no encontrados')

        # Actualizar el estado de la cuota a "Pagada"
        cuota.estado = 'Pagada'
        cuota.fecha_pago = fecha_pago
        cuota.monto_pago = monto_pago
        cuota.save()

        # Crear el registro de cobro
        CobroCuota.objects.create(
            credito=credito,
            numero_cuota=numero_cuota,
            estado='Pagada',
            fecha_pago=fecha_pago,
            monto_pago=monto_pago
        )

        return HttpResponse('Cobro registrado exitosamente')

    return render(request, 'registrar_cobro.html')

def cotizar_cheque(request):
    if request.method == 'POST':
        monto = float(request.POST.get('monto'))
        tna1 = 120
        tna = tna1 / 100
        fecha_deposito = datetime.strptime(request.POST.get('fecha_deposito'), '%Y-%m-%d').date()

        valor_descontado = calcular_descuento_cheque(monto, tna, fecha_deposito)

        return render(request, 'app_creditos/resultado_cotizacion.html', {'valor_descontado': valor_descontado, 'monto': int(monto), 'tna1': tna1, 'fecha_deposito': fecha_deposito})
    else:
        return render(request, 'app_creditos/formulario_cotizacion.html')
    
def resultado_cotizacion(request):
    return render(request, 'app_creditos/resultado_cotizacion.html')

