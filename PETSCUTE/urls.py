"""
URL configuration for PETSCUTE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='ruta global'),
    path('home/',views.irAInicio,name="ir inicio"),
    path('procesar/', views.procesar, name="Procesar datos"),
    path('registrar/',views.registrar,name="registrar usuario"),
    path('foro/',views.irAForo,name="ir foro"),
    path('buscar/',views.busquedaPersonalizada,name="busqueda personalizada"),
    path('buscarPorMunicipio/',views.busquedaMunicipio,name="busqueda_municipio"),
    path('perfil/',views.irAPerfil,name="ir perfil"),
    path('publicar/',views.irAPublicar,name="ir publicar"),
    path('asociaciones/',views.irAAsociaciones,name="ir asociaciones"),
    path('logout/',views.cerrarSesion,name="cerrar sesion"),
    path('olvide_password/',views.irOlvidePassword,name="olvide mi password"),
    path('enviarToken/',views.enviarToken,name="enviar token"),
    path('detallesPost/<int:id>/',views.irDetallesPublicacion,name="detalles publicacion"),
    path('adopcionForm/<int:id>/',views.irAFormularioAdopcion,name="formulario adopcion"),
    path('insertarForm/',views.insertarFormulario,name="insertar formulario"),
    path('detallesForm/<int:id>/',views.verDetallesForm,name="detalles_formulario"),
    path('actualizarPerfil/',views.actualizarPerfil,name="actualizar perfil"),
    path('chatbot/',views.irAChatbot,name="ir chatbot"),
    path('chatbot/ajax/', views.ajax_chat, name='ajax_chat'),

    path('admin_usuarios/delete_user/<int:id>', views.borrarUsuario,name='usuario borrar'),
    path('admin_publicaciones/delete_post/<int:id>', views.borrarPublicacion,name='publicacion borrar'),
    path('admin_adopciones/delete_adoption/<int:id>', views.borrarAdopcion,name='adopcion borrar'),

    path('admin_home/',views.irHomeAdmin,name='home admin'),
    path('admin_usuarios/',views.irUsuariosAdmin,name='usuarios admin'),
    path('admin_publicaciones/',views.irPublicacionesAdmin,name='publicaciones admin'),
    path('admin_adopciones/',views.irAdopcionesAdmin,name='adopciones admin'),

    path('publicar/salvar/',views.salvar_publicacion,name="salvar publicacion"),

    path('MASCOTAS/',include('MASCOTAS.urls')),
    path('PUBLICACIONES/',include('PUBLICACIONES.urls')),
    path('USUARIOS/',include('USUARIOS.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)