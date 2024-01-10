from django.contrib import admin
from django.urls import path

from app_creditos.views import ClienteListView, ClienteDetailView, ClienteUpdateView, eliminar_cliente, crear_tipo_credito,\
      Tipo_creditoListView, Tipo_creditoUpdateView, eliminar_tipo_credito, Tipo_creditoDetailView, CreditoListView,\
      CreditoDeleteView, CreditoDetailView, CreditoUpdateView, crear_cliente, crear_credito, eliminar_credito, registrar_pago,\
      actualizar_credito_individual, borrar_pago

urlpatterns = [
    #URL Clientes
    path("clientes/", ClienteListView.as_view(), name="lista_clientes"),
    path('crear-clientes/', crear_cliente, name="crear_clientes"),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name="ver_clientes"),
    path('editar-clientes/<int:pk>/', ClienteUpdateView.as_view(), name="editar_clientes"),
    path('eliminar-cliente/<int:pk>/', eliminar_cliente, name="eliminar_cliente"),
    
    #URLs tipos de credito
    path('tipo-creditos/', Tipo_creditoListView.as_view(), name='lista_tipo_creditos'),
    path('crear-tipo-creditos/', crear_tipo_credito, name='crear_tipo_creditos'),
    path('tipo-creditos/<int:pk>/', Tipo_creditoDetailView.as_view(), name="ver_tipo_creditos"),
    path('editar-tipo-creditos/<int:pk>/', Tipo_creditoUpdateView.as_view(), name="editar_tipo_creditos"),
    path('eliminar-tipo-creditos/<int:pk>/', eliminar_tipo_credito, name="eliminar_tipo_creditos"),
       
    #URLs creditos
    path('creditos/', CreditoListView.as_view(), name='lista_creditos'),
    path('crear-creditos/', crear_credito, name='crear_creditos'),
    path('creditos/<int:pk>/', CreditoDetailView.as_view(), name="ver_creditos"),
    path('editar-creditos/<int:pk>/', CreditoUpdateView.as_view(), name="editar_creditos"),
    path('eliminar-credito/<int:pk>/', eliminar_credito, name="eliminar_credito"),
    path('actualizar-credito/<int:pk>/', actualizar_credito_individual, name='actualizar_credito_individual'),
    
    #Cobro cuotas
    path('registrar_pago/<int:cuota_id>/', registrar_pago, name='registrar_pago'),
    path('borrar_pago/<int:id_pago>/', borrar_pago, name='borrar_pago'),
    
        
] 