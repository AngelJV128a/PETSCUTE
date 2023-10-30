from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password,check_password
from . import models
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
import random
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
import logging
logger = logging.getLogger(__name__)

def login(request):
    return render (request,'login.html')


def procesar(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password_ingresada = request.POST.get('password')

        try:
            usuario = models.Usuario.objects.get(correo=correo)
            if check_password(password_ingresada, usuario.contrasenia):
                request.session['username'] = correo
                request.session['password'] = password_ingresada  # No es una buena práctica guardar la contraseña en la sesión, incluso si está en texto plano
                request.session['id'] = usuario.id
                return render(request, 'menu2.html')
            else:
                contexto = {'Invalido': False}
                return render(request, 'login.html', contexto)
        except models.Usuario.DoesNotExist:
            contexto = {'Invalido': False}
            return render(request, 'login.html', contexto)
    return render(request, 'procesar.html')
def registrar(request):
    if request.method == 'POST':
        nombre=request.POST.get('nombre')
        correo = request.POST.get('correo')
        password= request.POST.get('contrasenia')
        nuevoUsuario=models.Usuario()
        nuevoUsuario.nombre=nombre
        nuevoUsuario.correo=correo
        nuevoUsuario.contrasenia=make_password(password)
        nuevoUsuario.save()
    return render(request, 'login.html')

def irAForo(request):
    publicaciones_lista = models.Publicacion.objects.all()
    paginator = Paginator(publicaciones_lista, 18)  # Muestra 18 publicaciones por página

    page = request.GET.get('page')
    publicaciones = paginator.get_page(page)

    return render(request, 'foro.html', {'publicaciones': publicaciones})
    return render(request, 'foro.html')

def irAPerfil(request):
    return render(request, 'perfil.html')

def irAInicio(request):
    return render(request,'menu2.html')

def irOlvidePassword(request):
    return render(request,'olvideContrasenia.html')

def irAPublicar(request):
    return render(request,'publicar.html')

def irDetallesPublicacion(request):
    return render(request,'detallesPublicacion.html')

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
    if request.method == 'POST' and request.FILES['foto']:
        foto = request.FILES['foto']
        fs = FileSystemStorage()
        filename = fs.save('fotos_mascotas/' + foto.name, foto)
        uploaded_file_url = fs.url(filename)

        publicacion = models.Publicacion(
            foto=uploaded_file_url,
            idUsuario_id=4,
            idAnimal_id=2,
            idUbicacion_id=1
        )
        publicacion.save()

        return redirect('ir foro')

    return render(request, 'publicar.html')