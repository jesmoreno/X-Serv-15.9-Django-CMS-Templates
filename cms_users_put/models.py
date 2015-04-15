from django.db import models

# Create your models here.

class Tabla (models.Model):
    nombre = models.CharField(max_length=30)
    fecha = models.DateTimeField()
