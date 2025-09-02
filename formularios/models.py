from django.db import models
from django.contrib.auth.models import User

class Formulario(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formularios')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

# Create your models here.
