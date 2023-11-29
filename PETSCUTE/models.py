# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Usuario(models.Model):
    id= models.AutoField(primary_key=True, db_column="id")
    nombre = models.CharField(max_length=45, db_column="nombre")
    apellido = models.CharField(max_length=45, db_column="apellido")
    nickname = models.CharField(max_length=45, db_column="nickname")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    correo = models.CharField(max_length=45, db_column="correo")
    contrasenia = models.BinaryField(max_length=128, db_column="contrasenia")
    foto = models.ImageField(upload_to='fotos_perfil/', db_column="foto")

    class Meta:
        managed = False
        db_table = 'usuarios'

class Ubicacion(models.Model):
    id= models.AutoField(primary_key=True, db_column="id")
    estado = models.CharField(max_length=45, db_column="estado")
    municipio = models.CharField(max_length=45, db_column="municipio")

    class Meta:
        managed = False
        db_table = 'ubicacion'

class Animal(models.Model):
    id= models.AutoField(primary_key=True, db_column="id")
    nombre = models.CharField(max_length=45, db_column="nombre")

    class Meta:
        managed = False
        db_table = 'animal'

class Publicacion(models.Model):
    id= models.AutoField(primary_key=True, db_column="id")
    idUsuario = models.ForeignKey(Usuario, db_column="id_usuario", on_delete=models.CASCADE)
    idAnimal = models.ForeignKey(Animal, db_column="id_animal", on_delete=models.CASCADE)
    idUbicacion = models.ForeignKey(Ubicacion, db_column="id_ubicacion", on_delete=models.CASCADE)
    nombreMascota = models.CharField(max_length=45, db_column="nombre_mascota")
    edadMascota = models.CharField(max_length=10, db_column="edad_mascota")
    sexoMascota = models.CharField(max_length=1, db_column="sexo")
    fechaPublicacion = models.DateTimeField(auto_now_add=True,db_column="fecha_publicacion")
    tamanioMascota = models.CharField(max_length=7, db_column="tamanio_mascota")
    direccion = models.CharField(max_length=45, db_column="direccion")
    foto = models.ImageField(upload_to='fotos_mascotas/', db_column="foto")
    foto2=models.ImageField(upload_to='fotos_mascotas/',db_column="foto2")
    foto3 = models.ImageField(upload_to='fotos_mascotas/', db_column="foto3")

    class Meta:
        managed = False
        db_table = 'publicaciones'

class Formulario(models.Model):
    id= models.AutoField(primary_key=True, db_column="id")
    idPublicacion = models.ForeignKey(Publicacion, db_column="id_publicacion", on_delete=models.CASCADE)
    idUsuarioAdoptador = models.ForeignKey(Usuario, db_column="id_usuario_adoptador", on_delete=models.CASCADE)
    razon = models.CharField(max_length=128, db_column="razon")
    lugar = models.CharField(max_length=128, db_column="lugar")
    experiencia = models.CharField(max_length=128, db_column="experiencia")
    comentario = models.CharField(max_length=128, db_column="comentario")

    class Meta:
        managed = False
        db_table = 'formularios'



class Adopcion(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    id_publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, db_column='id_publicacion')
    ciudad = models.CharField(max_length=45, db_column='ciudad')
    fecha = models.DateField(auto_now_add=True, db_column='fecha')
    revision = models.CharField(max_length=45, db_column='revision')
    id_formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE, db_column='id_formulario')

    def __str__(self):
        return f"Adopcion-{self.id}"

    class Meta:
        db_table = 'adopciones'

class Adopcion(models.Model):
    id= models.AutoField(primary_key=True, db_column="id")
    idPublicacion = models.ForeignKey(Publicacion, db_column="id_publicacion", on_delete=models.CASCADE)
    idFormulario = models.ForeignKey(Formulario, db_column="id_formulario", on_delete=models.CASCADE)
    ciudad = models.CharField(max_length=45, db_column="ciudad")
    revision = models.CharField(max_length=45, db_column="revision")
    fecha = models.DateField(auto_now_add=True, db_column='fecha')

    class Meta:
        managed = False
        db_table = 'adopciones'

