from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import re

class RegisterForm(forms.ModelForm):
    """
    Formulario de registro de usuario con validaciones personalizadas:
    - username: máximo 20 caracteres, debe contener al menos un número.
    - email: debe ser único en la base de datos.
    - password y password2: deben coincidir.
    """
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico"
        }
        widgets = {
            "username": forms.TextInput(attrs={"maxlength": 20}),
        }
        help_texts = {
            "username": ""
        }

    def clean_username(self):
        """Valida que el nombre de usuario cumpla las reglas de longitud y contenga al menos un número."""
        username = self.cleaned_data.get("username", "")
        reglas = "Debe tener máximo 20 caracteres, contener al menos un número y puede incluir cualquier caracter especial."
        if len(username) > 20:
            raise ValidationError(f"{reglas}")
        if not re.search(r"\d", username):
            raise ValidationError(f"{reglas}")
        return username

    def clean_email(self):
        """Valida que el email no esté registrado previamente."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean(self):
        """Valida que las contraseñas coincidan."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned_data
