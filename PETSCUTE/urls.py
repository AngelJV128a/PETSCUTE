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
    path('perfil/',views.irAPerfil,name="ir perfil"),
    path('publicar/',views.irAPublicar,name="ir publicar"),
    path('logout/',views.cerrarSesion,name="cerrar sesion"),
    path('olvide_password/',views.irOlvidePassword,name="olvide mi password"),
    path('enviarToken/',views.enviarToken,name="enviar token"),
    path('detallesPost/',views.irDetallesPublicacion,name="detalles publicacion"),

    path('publicar/salvar/',views.salvar_publicacion,name="salvar publicacion"),

    path('MASCOTAS/',include('MASCOTAS.urls')),
    path('PUBLICACIONES/',include('PUBLICACIONES.urls')),
    path('USUARIOS/',include('USUARIOS.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)