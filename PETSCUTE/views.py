from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password,check_password
from . import models
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest
import random
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
import logging
from django.contrib.auth.backends import ModelBackend
from cryptography.fernet import Fernet
from django.db import connection
logger = logging.getLogger(__name__)

clave_secreta="JLcvfX4si-8N3XwOK2zEchUdJwPm7hZw2hFlhXqHDC4="

def login(request):
    contexto = {'Invalido': False,
                'msg': ''}
    return render (request,'login.html', contexto)


def procesar(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password_ingresada = request.POST.get('password')

        try:
            print("Usuario admitido")
            usuario = models.Usuario.objects.get(correo=correo)
            fernet = Fernet(clave_secreta)
            password_descifrado = fernet.decrypt(usuario.contrasenia).decode('utf-8')
            if password_ingresada==password_descifrado:
                request.session['username'] = correo
                request.session['password'] = password_ingresada  # No es una buena práctica guardar la contraseña en la sesión, incluso si está en texto plano
                request.session['id'] = usuario.id
                return render(request, 'menu2.html')
            else:
                print("Usuario no admitido")
                contexto = {'Invalido': False,
                            'msg': 'Usuario no admitido'}
                return render(request, 'login.html', contexto)
        except models.Usuario.DoesNotExist:
            print("Usuario no admitido")
            contexto = {'Invalido': False,
                            'msg': 'Usuario no admitido'}
            return render(request, 'login.html', contexto)
    print("Usuario no admitido")
    return render(request, 'procesar.html')
def registrar(request):
    if request.method == 'POST':
        nombre=request.POST.get('nombre')
        correo = request.POST.get('correo')
        password= request.POST.get('contrasenia')
        fernet = Fernet(clave_secreta)
        mydata = models.Usuario.objects.filter(correo=correo).values()
        if (mydata):
            print("Correo ya existente")
            contexto = {'Invalido': False,
                            'msg': 'Este correo ya esta registrado'}
            return render(request, 'login.html', contexto)
        else:
            nuevoUsuario=models.Usuario()
            nuevoUsuario.nombre=nombre
            nuevoUsuario.correo=correo
            nuevoUsuario.contrasenia= fernet.encrypt(password.encode('utf-8'))
            nuevoUsuario.save()
            print("Cuenta registrada con exito!")
            contexto = {'Invalido': False,
                            'msg': 'Cuenta registrada con exito!'}
    return render(request, 'login.html', contexto)

def irAForo(request):
    publicaciones_lista = models.Publicacion.objects.all()
    paginator = Paginator(publicaciones_lista, 18)  # Muestra 18 publicaciones por página

    page = request.GET.get('page')
    publicaciones = paginator.get_page(page)

    return render(request, 'foro.html', {'publicaciones': publicaciones})

def busquedaPersonalizada(request):
    ciudad = request.POST.get('ciudad')
    tamanio = request.POST.get('tamanio')
    print(ciudad)
    print(tamanio)

    query = models.Publicacion.objects.all()  # Obtén todos los registros

    if ciudad:
        query = query.filter(idUbicacion__estado=ciudad)

    if tamanio:
        query = query.filter(tamanioMascota=tamanio)

    query = query.order_by('-fechaPublicacion')  # Ordena la consulta por fecha de publicación
    # Crea un objeto Paginator para los resultados
    paginator = Paginator(query, 18)  # Muestra 18 resultados por página

    page_number = request.GET.get('page')  # Obtén el número de página de la solicitud GET
    page = paginator.get_page(page_number)  # Obtén la página actual

    return render(request, 'foro.html', {'publicaciones': page})

def irAPerfil(request):
    id=request.session['id']
    usuario = get_object_or_404(models.Usuario, id=id)
    return render(request, 'perfil.html',{'usuario':usuario})

def irAAsociaciones(request):
    return render(request,'organizaciones.html')
def irAInicio(request):
    return render(request,'menu2.html')

def irOlvidePassword(request):
    return render(request,'olvideContrasenia.html')

def irAPublicar(request):
    return render(request,'publicar.html')

def irDetallesPublicacion(request,id):
    try:
        resultado = models.Publicacion.objects.get(id=id)
    except models.Publicacion.DoesNotExist:
        resultado = None
    return render(request,'detallesPublicacion.html',{'mascota': resultado})

def cerrarSesion(request):
    username = request.session.get('username')
    user_id = request.session.get('password')
    print(username)
    print(user_id)
    print(request.session.get('id'))
    request.session.flush()
    return render(request, 'login.html')


def enviarToken(request):
    if request.method == 'POST':
        email_destinatario = request.POST.get('correo', None)

        if not email_destinatario:
            return HttpResponseBadRequest('Se requiere un correo.')

            # Generar el token de 6 dígitos
        token = str(random.randint(100000, 999999))

        # Definir el cuerpo del correo en formato HTML
        html_message = """
        <h2>Recuperación de Contraseña</h2>
        <p>Recibimos una solicitud para restablecer tu contraseña.</p>
        <p>Para continuar con el proceso, utiliza el siguiente token:</p>
        <h3 style="color: #4CAF50;">{}</h3>
        <p>Si no realizaste esta solicitud, puedes ignorar este correo.</p>
        """.format(token)

        send_mail(
            'Recuperación de Contraseña',
            '',  # Dejamos el mensaje normal vacío porque estamos enviando en formato HTML.
            'petscuecucei@gmail.com',
            [email_destinatario],
            fail_silently=False,
            html_message=html_message  # Usamos el argumento html_message para el contenido HTML.
        )
        return render(request, 'olvideContrasenia.html')
    else:
        return HttpResponseBadRequest('Método no permitido.')


def salvar_publicacion(request):
    logger.info("salvar_publicacion ha sido llamada")
    if request.method == 'POST'  and 'foto' in request.FILES:
        nombre_mascota = request.POST.get('nombre_mascota')
        tamanio = request.POST.get('tamanio')
        edad = request.POST.get('edad')
        sexo = request.POST.get('sexo')
        tipo = request.POST.get('tipo')
        pais = request.POST.get('pais')
        estado = request.POST.get('estado')
        municipio = request.POST.get('municipio')
        comentario = request.POST.get('comentario')

        foto = request.FILES['foto']
        fs = FileSystemStorage()
        filename = fs.save('fotos_mascotas/' + foto.name, foto)
        uploaded_file_url = fs.url(filename)

        ubicacion=models.Ubicacion(
            estado=estado,
            municipio=municipio
        )
        ubicacion.save()  # Guarda la ubicación en la base de datos

        publicacion = models.Publicacion(
            foto=uploaded_file_url,
            idUsuario_id=request.session['id'],
            idAnimal_id=tipo,
            idUbicacion_id=ubicacion.id,
            nombreMascota=nombre_mascota,
            edadMascota=edad,
            sexoMascota=sexo,
            tamanioMascota=tamanio,
        )
        publicacion.save()

        return redirect('ir foro')

    return render(request, 'publicar.html')


def actualizarPerfil(request):
    id = request.session['id']
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        nickname = request.POST['nickname']
        correo = request.POST['correo']
        contrasenia=request.POST['password']
        fernet = Fernet(clave_secreta)

        usuario = models.Usuario.objects.get(id=id)
        usuario.nombre = nombre
        usuario.apellido = apellidos
        usuario.nickname = nickname
        usuario.correo = correo
        usuario.contrasenia=fernet.encrypt(contrasenia.encode('utf-8'))

        if 'foto' in request.FILES:
            foto = request.FILES['foto']
            fs = FileSystemStorage()
            filename = fs.save('fotos_perfil/' + foto.name, foto)
            uploaded_file_url = fs.url(filename)
            usuario.foto=uploaded_file_url

        usuario.save()

        return redirect('ir perfil')
    return render(request,'perfil.html')