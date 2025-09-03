
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import forms
from .models import Formulario

@login_required(login_url='/login/')
def eliminar_formulario(request, formulario_id):
	formulario = Formulario.objects.filter(id=formulario_id, creado_por=request.user).first()
	if formulario:
		formulario.delete()
	return redirect('portal_formularios')

class FormUploadForm(forms.Form):
	nombre = forms.CharField(label="Nombre del formulario", max_length=100, required=True)
	archivo = forms.FileField(label="Archivo de formulario (PDF, Word, etc.)", required=True)


@login_required(login_url='/login/')
def portal_formularios(request):
	formularios = request.user.formularios.all().order_by('-creado_en')
	return render(request, 'formularios/portal.html', {'formularios': formularios})


@login_required(login_url='/login/')
def subir_formulario(request):
	error_nombre = None
	if request.method == 'POST':
		form = FormUploadForm(request.POST, request.FILES)
		if form.is_valid():
			nombre = form.cleaned_data['nombre']
			archivo = form.cleaned_data['archivo']
			# Validar unicidad de nombre por usuario
			if Formulario.objects.filter(nombre=nombre, creado_por=request.user).exists():
				error_nombre = "Ya tienes un formulario con ese nombre. Elige otro."
			else:
				Formulario.objects.create(
					nombre=nombre,
					descripcion='',
					archivo=archivo,
					creado_por=request.user
				)
				return redirect('portal_formularios')
	else:
		form = FormUploadForm()
	return render(request, 'formularios/subir_formulario.html', {'form': form, 'error_nombre': error_nombre})
