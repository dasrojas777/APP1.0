from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import forms

class FormUploadForm(forms.Form):
	archivo = forms.FileField(label="Archivo de formulario (PDF, Word, etc.)", required=True)

@login_required(login_url='/login/')
def portal_formularios(request):
	return render(request, 'formularios/portal.html')

@login_required(login_url='/login/')
def subir_formulario(request):
	if request.method == 'POST':
		form = FormUploadForm(request.POST, request.FILES)
		if form.is_valid():
			# Aquí se procesará el archivo subido
			archivo = form.cleaned_data['archivo']
			# Por ahora solo redirigimos de vuelta al portal
			return redirect('portal_formularios')
	else:
		form = FormUploadForm()
	return render(request, 'formularios/subir_formulario.html', {'form': form})
