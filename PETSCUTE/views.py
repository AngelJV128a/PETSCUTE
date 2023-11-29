from django.shortcuts import render,redirect,get_object_or_404
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password,check_password
from . import models
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest
import random
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator,  EmptyPage, PageNotAnInteger
import logging
from django.contrib.auth.backends import ModelBackend
from cryptography.fernet import Fernet

from django.db import connection
import nltk
from nltk.chat.util import Chat, reflections

logger = logging.getLogger(__name__)

clave_secreta="JLcvfX4si-8N3XwOK2zEchUdJwPm7hZw2hFlhXqHDC4="



# Descargar el conjunto de datos de pares de respuestas de ejemplo de NLTK
nltk.download('nps_chat')

# Importar el conjunto de datos de pares de respuestas
posts = nltk.corpus.nps_chat.xml_posts()

# Crear pares de respuestas para el chatbot
pairs = [
    (r'Hola', ['Mi nombre es PETBOT, dime en que te puedo ayudar']),
    (r'Necesito (.*)', ['¿Por qué necesitas %1?', '¿Cómo usarías %1?']),
    (r'(.*) ayuda (.*)', ['Puedo ayudarte con %1.']),
    (r'(.*) tu nombre?', ['Soy un chatbot.']),
    (r'(.*) (ubicación|ciudad) ?', ['Soy un asistente virtual. No tengo una ubicación física.']),
    (r'(.*) una publicacion?', ['Para hacer una publicacion, debes ir a la seccion de Publicar y seguir los pasos']),
    (r'Que es el foro?', ['El Foro es una seccion donde puedes ver a los animales en adopcion']),
    (r'Que son las asociaciones?', ['Las asociaciones son organizaciones que se encargan de ayudar a mas personas a encontrar animales en adopcion. Para ver alguna de ellas, solo ve a la seccion de Asociaciones']),
    (r'Que es el perfil?', ['En el Perfil puedes encontrar tu informacion personal, asi como la opcion de editarla en caso necesario']),
    (r'Como puedo adoptar?', ['Para adoptar una mascota, puedes ir a la seccion de Foro y elegir la que te guste. Despues, dale al boton de Adoptar para rellenar un formulario y seguir las instrucciones siguientes']),
    (r'Lo siento', ['No te preocupes, todos somos humanos, ...bueno yo no, yo soy un chatbot', 'Esta bien, te perdono', 'No te perdono. Ntc, si te perdono']),
    (r'(Buenos dias|Buenas tardes|Buenas noches)', [' a ti tambien']),
    (r'Para que es el switch que esta en la esquina?', ['Sirve para alternar entre el modo oscuro y el modo claro']),
    (r'Me quieres?', ['Perdon, solo te veo como usuario'])
]

# Crear el chatbot con los pares de respuestas
chatbot = Chat(pairs, reflections)

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
                return redirect( 'ir inicio')
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
    if request.method == 'POST':
        filtro_seleccionado = request.POST.get('filtro', 'all')
        paginator = None  # Define paginator antes de los bloques if/elif
    # Lógica de filtrado basada en el valor de "filtro_seleccionado"
        if filtro_seleccionado == 'All':
            todos_los_registros = models.Publicacion.objects.all()
            paginator = Paginator(todos_los_registros, 18)
        elif filtro_seleccionado in ['Perro', 'Gato', 'Pajaro', 'Cuyo']:
            print(filtro_seleccionado)
            especie_id = models.Animal.objects.get(nombre=filtro_seleccionado).id
            print(especie_id)
            registros_por_especie = models.Publicacion.objects.filter(idAnimal=especie_id).order_by('id')
            paginator = Paginator(registros_por_especie, 18)
        elif filtro_seleccionado in ['Chico', 'Grande']:
            registros_por_tamano = models.Publicacion.objects.filter(tamanioMascota=filtro_seleccionado)
            paginator = Paginator(registros_por_tamano, 18)


    publicaciones = paginator.page(1)
    print(publicaciones)
    return render(request, 'foro.html', {'publicaciones': publicaciones})

def busquedaMunicipio(request):
    # Obtener el municipio del formulario
    municipio = request.POST.get('busqueda')

    # Filtrar publicaciones por municipio
    publicaciones = models.Publicacion.objects.filter(idUbicacion__municipio=municipio)
    # Hacer algo con las publicaciones, por ejemplo, pasarlas a la plantilla
    paginator = Paginator(publicaciones, 18)

    # Puedes pasar las publicaciones a tu plantilla o realizar otras acciones
    return render(request, 'foro.html', {'publicaciones': paginator.page(1)})


def irAPerfil(request):
    id=request.session['id']
    usuario = get_object_or_404(models.Usuario, id=id)
    return render(request, 'perfil.html',{'usuario':usuario})

def irAAsociaciones(request):
    return render(request,'organizaciones.html')
def irAInicio(request):
    if request.session['username']=="admin@petscue.com":
        return redirect('home admin')
    return render(request,'menu2.html')

def irOlvidePassword(request):
    return render(request,'olvideContrasenia.html')

def irAPublicar(request):
    return render(request,'publicar.html')

def irAChatbot(request):
    return render(request,'chatbot.html')

def irDetallesPublicacion(request,id):
    try:
        resultado = models.Publicacion.objects.get(id=id)
        resultado.fechaPublicacion=resultado.fechaPublicacion.date()
    except models.Publicacion.DoesNotExist:
        resultado = None
    return render(request,'detallesPublicacion.html',{'mascota': resultado})

def irAFormularioAdopcion(request,id):
    return render(request,'formulario.html',{'id_mascota':id})

def insertarFormulario(request):

    id_publicacion_valor = request.POST.get('id_publicacion') # Reemplaza con el valor correcto
    id_usuario_adoptador_valor = request.session['id']  # Reemplaza con el valor correcto
    razon_valor = request.POST.get('razon')
    lugar_valor = request.POST.get('lugar')
    experiencia_valor = request.POST.get('experiencia')
    comentario_valor = request.POST.get('comentario')

    # Crear un nuevo objeto Formulario
    nuevo_formulario = models.Formulario(
        idPublicacion=models.Publicacion.objects.get(id=id_publicacion_valor),
        idUsuarioAdoptador=models.Usuario.objects.get(id=id_usuario_adoptador_valor),
        razon=razon_valor,
        lugar=lugar_valor,
        experiencia=experiencia_valor,
        comentario=comentario_valor
    )

    # Guardar el nuevo formulario en la base de datos
    nuevo_formulario.save()


    #ciudad_valor = "EjemploCiudad"
    revision_valor = "Sin revisar"
    id_formulario_valor = nuevo_formulario.id  # Reemplaza con el valor correcto

    publicacion = get_object_or_404(models.Publicacion, id=id_publicacion_valor)

    # Recuperar la información de ubicación desde la tabla Ubicacion mediante la relación de clave foránea en la Publicacion
    ubicacion = get_object_or_404(models.Ubicacion, id=publicacion.idUbicacion.id)
    ciudad = ubicacion.municipio  # Ajusta según tu modelo y relaciones

    # Crear un nuevo objeto Adopcion y guardarlo en la base de datos
    nueva_adopcion = models.Adopcion(
        idPublicacion=models.Publicacion.objects.get(id=id_publicacion_valor),
        ciudad=ciudad,
        revision=revision_valor,
        idFormulario=models.Formulario.objects.get(id=id_formulario_valor)
    )
    nueva_adopcion.save()

    # Resto de tu lógica de vista

    return render(request,'foro.html')

def verDetallesForm(request,id):
    formulario = get_object_or_404(models.Formulario, pk=id)
    # Acceder al usuario asociado al formulario
    usuario = formulario.idUsuarioAdoptador  # Ajusta el nombre según la relación en tu modelo

    return render(request,'detallesFormulario.html',{'formulario':formulario,'usuario':usuario})

#ADMIN
def irHomeAdmin(request):
    return render(request,'index.html')

def irUsuariosAdmin(request):
    usuarios = models.Usuario.objects.annotate(num_publicaciones=Count('publicacion'))
    for usuario in usuarios:
        usuario.fecha_creacion = usuario.fecha_creacion.date()
    return render(request,'usuariosadmin copy.html',{'usuarios':usuarios})

def borrarUsuario(request, id):
    usuario_borrar = models.Usuario.objects.get(id=id)
    usuario_borrar.delete()
    return redirect("/admin_usuarios/")

def borrarPublicacion(request, id):
    publicacion_borrar = models.Publicacion.objects.get(id=id)
    publicacion_borrar.delete()
    return redirect("/admin_publicaciones/")

def borrarAdopcion(request, id):
    adopcion_borrar = models.Adopcion.objects.get(id=id)
    adopcion_borrar.delete()
    return redirect("/admin_adopciones/")

def irPublicacionesAdmin(request):
    publicaciones = models.Publicacion.objects.all()
    return render(request,'publicaciones.html',{'publicaciones':publicaciones})

def irAdopcionesAdmin(request):
    adopciones = models.Adopcion.objects.select_related('idPublicacion').all()
    return render(request,'adopciones.html',{'adopciones':adopciones})



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
    print("entro 1")
    print(request.FILES['foto'])
    if request.method == 'POST' and 'foto' in request.FILES:
        print("entro 2")
        nombre_mascota = request.POST.get('nombre_mascota')
        tamanio = request.POST.get('tamanio')
        edad = request.POST.get('edad')
        sexo = request.POST.get('sexo')
        tipo = request.POST.get('tipo')
        pais = request.POST.get('pais')
        estado = request.POST.get('estado')
        municipio = request.POST.get('municipio')
        comentario = request.POST.get('comentario')

        fotos = request.FILES.getlist('foto')

        fs = FileSystemStorage()
        filename = fs.save('fotos_mascotas/' + fotos[0].name, fotos[0])
        uploaded_file_url = fs.url(filename)

        if len(fotos)>=2:
            fs = FileSystemStorage()
            filename = fs.save('fotos_mascotas/' + fotos[1].name, fotos[1])
            uploaded_file_url2 = fs.url(filename)

        if len(fotos)>=3:
            fs = FileSystemStorage()
            filename = fs.save('fotos_mascotas/' + fotos[2].name, fotos[2])
            uploaded_file_url3 = fs.url(filename)

        ubicacion=models.Ubicacion(
            estado=estado,
            municipio=municipio
        )
        ubicacion.save()  # Guarda la ubicación en la base de datos

        publicacion = models.Publicacion(
            foto=uploaded_file_url,
            foto2=uploaded_file_url2,
            foto3=uploaded_file_url3,
            idUsuario_id=request.session['id'],
            idAnimal_id=tipo,
            idUbicacion_id=ubicacion.id,
            nombreMascota=nombre_mascota,
            edadMascota=edad,
            sexoMascota=sexo,
            tamanioMascota=tamanio,
        )
        publicacion.save()
        print("termino")
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

@csrf_exempt
def ajax_chat(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        user_input=data.get('user_input')

        # Resto de la lógica aquí
        response_data = get_chatbot_response(user_input)
        print(response_data)
        return JsonResponse(response_data,safe=False)
    except KeyError:
        return JsonResponse({'error': 'No se proporcionó la clave "user_input" en la solicitud'}, status=400)
    except Exception as e:
        print(f'Error: {str(e)}')
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)

def get_chatbot_response(user_input):
    # Aquí iría tu lógica para obtener la respuesta del chatbot
    # Puedes usar el código que proporcionaste anteriormente

    user="Cual es tu nombre?"
    response=chatbot.respond(user)
    print("chatbot: ",response)

    return chatbot.respond(user_input)