from typing import Any, Dict
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from app_creditos.models import Cliente, Tipo_Credito, Credito, Lista_cuota
from .utils import calcular_cuota
from datetime import datetime, timedelta, date
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from dateutil.relativedelta import relativedelta


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
        return context
      
class CreditoUpdateView(LoginRequiredMixin, UpdateView):
    model = Credito
    fields = ('importe_cuota', 'tipo_credito', 'cuotas', 'importe_credito')
    success_url = reverse_lazy('lista_creditos')

class CreditoDeleteView(LoginRequiredMixin, DeleteView):
    model = Credito
    success_url = reverse_lazy('lista_creditos')

def eliminar_credito(request, pk):

    credito=Credito.objects.get(pk=pk)
    credito.delete()

    return redirect('lista_creditos') 