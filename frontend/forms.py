from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import re

class RegisterForm(forms.ModelForm):
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
        username = self.cleaned_data.get("username", "")
        # Mensaje personalizado con todas las reglas
        reglas = "Debe tener máximo 20 caracteres, contener al menos un número y puede incluir cualquier caracter especial."
        if len(username) > 20:
            raise ValidationError(f"{reglas}")
        if not re.search(r"\d", username):
            raise ValidationError(f"{reglas}")
        # Permitimos cualquier caracter especial universal, solo validamos longitud y número
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned_data
