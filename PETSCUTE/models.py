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
    #fecha_creacion = models.DateTimeField(null=False, db_column="fecha_creacion")
    correo = models.CharField(max_length=45, db_column="correo")
    contrasenia = models.CharField(max_length=128, db_column="contrasenia")

    class Meta:
        managed = False
        db_table = 'usuarios'
