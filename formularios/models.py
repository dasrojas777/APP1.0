from django.db import models
from django.contrib.auth.models import User



class Formulario(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='formularios/', blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formularios')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('nombre', 'creado_por')

    def __str__(self):
        return self.nombre

# Create your models here.
