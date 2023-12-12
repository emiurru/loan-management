from django.contrib import admin
from django.urls import path

from app_creditos.views import ClienteListView, ClienteDetailView, ClienteUpdateView, ClienteDeleteView, crear_tipo_credito,\
      Tipo_creditoListView, Tipo_creditoUpdateView, Tipo_creditoDeleteView, Tipo_creditoDetailView, CreditoListView,\
      CreditoDeleteView, CreditoDetailView, CreditoUpdateView, crear_cliente, crear_credito, eliminar_credito

urlpatterns = [
    #URL Clientes
    path("clientes/", ClienteListView.as_view(), name="lista_clientes"),
    path('crear-clientes/', crear_cliente, name="crear_clientes"),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name="ver_clientes"),
    path('editar-clientes/<int:pk>/', ClienteUpdateView.as_view(), name="editar_clientes"),
    path('eliminar-clientes/<int:pk>/', ClienteDeleteView.as_view(), name="eliminar_clientes"),
    
    #URLs tipos de credito
    path('tipo-creditos/', Tipo_creditoListView.as_view(), name='lista_tipo_creditos'),
    path('crear-tipo-creditos/', crear_tipo_credito, name='crear_tipo_creditos'),
    path('tipo-creditos/<int:pk>/', Tipo_creditoDetailView.as_view(), name="ver_tipo_creditos"),
    path('editar-tipo-creditos/<int:pk>/', Tipo_creditoUpdateView.as_view(), name="editar_tipo_creditos"),
    path('eliminar-tipo-creditos/<int:pk>/', Tipo_creditoDeleteView.as_view(), name="eliminar_tipo_creditos"),
       
    #URLs creditos
    path('creditos/', CreditoListView.as_view(), name='lista_creditos'),
    path('crear-creditos/', crear_credito, name='crear_creditos'),
    path('creditos/<int:pk>/', CreditoDetailView.as_view(), name="ver_creditos"),
    path('editar-creditos/<int:pk>/', CreditoUpdateView.as_view(), name="editar_creditos"),
    path('eliminar-credito/<int:pk>/', eliminar_credito, name="eliminar_credito"),
    
    #Cobro cuotas
     
    
        
] 