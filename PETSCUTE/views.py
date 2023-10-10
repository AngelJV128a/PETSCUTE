from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from . import models

def login(request):
    return render (request,'login.html')

def procesar(request):
    if request.method == 'POST':
        correo= request.POST.get('correo')
        # Haz algo con el valor 'nombre'
        password = request.POST.get('password')
        usuario=models.Usuario.objects.filter(correo=correo,contrasenia=password)
        if usuario.exists():
            request.session['username']=correo
            request.session['password']=password
            request.session['id']=usuario.first().id
            return render(request,'menu2.html')
        else:
            contexto={
                'Invalido': False
            }
            return render(request, 'login.html',contexto)
    return render(request, 'procesar.html')
def registrar(request):
    if request.method == 'POST':
        nombre=request.POST.get('nombre')
        correo = request.POST.get('correo')
        password= request.POST.get('contrasenia')
        nuevoUsuario=models.Usuario()
        nuevoUsuario.nombre=nombre
        nuevoUsuario.correo=correo
        nuevoUsuario.contrasenia=password
        nuevoUsuario.save()
    return render(request, 'login.html')

def irAForo(request):
    return render(request, 'foro.html')

def irAPerfil(request):
    return render(request, 'perfil.html')

def irAInicio(request):
    return render(request,'menu2.html')

def irAPublicar(request):
    return render(request,'publicar.html')
def cerrarSesion(request):
    username = request.session.get('username')
    user_id = request.session.get('password')
    print(username)
    print(user_id)
    print(request.session.get('id'))
    request.session.flush()
    return render(request, 'login.html')