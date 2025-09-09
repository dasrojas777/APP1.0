
from django.db import models
from django.contrib.auth.models import User

class Formulario(models.Model):
    """
    Modelo que representa un formulario subido por un usuario.
    - nombre: nombre único del formulario por usuario
    - descripcion: descripción opcional
    - archivo: archivo adjunto (PDF, Word, etc.)
    - creado_por: usuario que subió el formulario
    - creado_en: fecha de creación
    - actualizado_en: fecha de última actualización
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='formularios/', blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formularios')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('nombre', 'creado_por')
        verbose_name = 'Formulario'
        verbose_name_plural = 'Formularios'

    def __str__(self):
        """Representación legible del formulario."""
        return self.nombre
