from django.shortcuts import render
from django.http import HttpResponse


def login(request):
    return render (request,'login.html')

def procesar(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo= request.POST.get('correo')
        # Haz algo con el valor 'nombre'
        return HttpResponse(f"Nombre recibido: {nombre}, Correo: {correo}")

    return render(request, 'procesar.html')