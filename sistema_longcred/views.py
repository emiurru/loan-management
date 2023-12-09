from django.shortcuts import render, redirect
from django.http import HttpResponse



def html(request):
    contexto = {}
    http_responde = render(
        request=request,
        template_name='app_creditos/base.html',
        context=contexto
    )
    return http_responde

def inicio(request):
    contexto = {}
    http_response = render(
        request=request,
        template_name='app_creditos/index.html',
        context=contexto,
    )
    return redirect('login')

def about(request):
    contexto = {}
    http_response = render(
        request=request,
        template_name='app_creditos/about.html',
        context=contexto,
    )
    return http_response