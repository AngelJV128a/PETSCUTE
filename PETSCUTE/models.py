# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Animal(models.Model):
    nombre = models.CharField(max_length=45, db_column="nombre")

    class Meta:
        managed = False
        db_table = 'animal'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Publicacion(models.Model):
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    id_ubicacion = models.ForeignKey('Ubicacion', models.DO_NOTHING, db_column = 'id_ubicacion')
    id_animal = models.ForeignKey('Animal', models.DO_NOTHING, db_column='id_animal')
    nombre_mascota = models.CharField(max_length=45, db_column="nombre_mascota")
    edad_mascota = models.IntegerField(db_column="edad_mascota")
    tamanio_mascota = models.CharField(max_length=7, db_column="tamanio_mascota")
    sexo_mascota = models.CharField(max_length=1, db_column="sexo")
    direccion = models.CharField(max_length=45, db_column="direccion")
    fecha_publicacion = models.DateTimeField(db_column="fecha_publicacion")

    class Meta:
        managed = False
        db_table = 'publicaciones'


class Ubicacion(models.Model):
    estado = models.CharField(max_length=45, db_column="estado")
    municipio = models.CharField(max_length=45, db_column="municipio")

    class Meta:
        managed = False
        db_table = 'ubicacion'


class Usuario(models.Model):
    id= models.AutoField(primary_key=True, db_column="id")
    nombre = models.CharField(max_length=45, db_column="nombre")
    apellido = models.CharField(max_length=45, db_column="apellido")
    nickname = models.CharField(max_length=45, db_column="nickname")
    #fecha_creacion = models.DateTimeField(null=False, db_column="fecha_creacion")
    correo = models.CharField(max_length=45, db_column="correo")
    contrasenia = models.CharField(max_length=45, db_column="contrasenia")

    class Meta:
        managed = False
        db_table = 'usuarios'
