from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from . import models

def login(request):
    return render (request,'login.html')

def procesar(request):
    if request.method == 'POST':
        correo= request.POST.get('correo')
        # Haz algo con el valor 'nombre'
        password = request.POST.get('password')
        if models.Usuario.objects.filter(correo=correo,contrasenia=password).exists():
            return render(request,'foro.html')
        else:
            contexto={
                'Invalido': False
            }
            return render(request, 'login.html',contexto)
    return render(request, 'procesar.html')

def registrar(request):
    if request.method == 'POST':
        id=2
        nombre=request.POST.get('nombre')
        correo = request.POST.get('correo')
        password= request.POST.get('password')
        nuevoUsuario=models.Usuario()
        nuevoUsuario.id=id
        nuevoUsuario.nombre=nombre
        nuevoUsuario.correo=correo
        nuevoUsuario.password=password
        nuevoUsuario.save()
    return render(request, 'procesar.html')