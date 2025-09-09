import re
import json
import PyPDF2
from django import forms

# Palabras clave para tipos de protocolo
PROTOCOLOS = {
	'GROUT': ['GROUT', 'CONTROL DE VACIADO'],
	'PINTURA': ['PINTURA'],
	'ANCLAJE': ['ANCLAJE', 'PERNO', 'BARRA'],
	# Agrega más tipos según tus necesidades
}

class PDFFormularioForm(forms.Form):
	archivo = forms.FileField(label="Archivo PDF del formulario")

def detectar_protocolo(texto):
	for tipo, claves in PROTOCOLOS.items():
		for clave in claves:
			if clave.upper() in texto.upper():
				return tipo
	return 'DESCONOCIDO'

def extraer_campos_encabezado(texto):
	"""Extrae campos clave del encabezado usando regex."""
	campos = {}
	patrones = {
			'fecha': r'Fecha[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})',
			'ubicacion': r'UBICACI[ÓO]N[:\s]*([^\n\r]+)',
			'fabricante': r'FABRICANTE[:\s]*([^\n\r]+)',
			'voltaje': r'VOLTAJE[\w ]*[:\s]*([0-9]+/?[0-9]* ?VAC)',
			'cliente': r'NOMBRE CLIENTE[:\s]*([^\n\r]+)',
			'protocolo': r'PROTOCOLO[:\s]*([\w\-\.]+)',
			'plano': r'PLANO[\w ]*[:\s]*([^\n\r]+)',
	}
	for campo, patron in patrones.items():
		m = re.search(patron, texto, re.IGNORECASE)
		if m:
			valor = m.group(1).strip()
			# Post-procesamiento para limpiar valores
			if campo == 'voltaje':
				valor = valor.replace(' ', '').replace('VAC', ' VAC')
			campos[campo] = valor
	return campos

def extraer_secciones(texto):
	patrones = [
		r'ENCABEZADO',
		r'LIBERACIÓN.*?GROUT',
		r'CONTROLES ANTES.*?GROUT',
		r'CONTROLES DURANTE.*?GROUT',
		r'APLICACIÓN DE PINTURA',
		r'ENSAYO DE ADHERENCIA',
		r'CONDICIÓN FINAL',
		r'OBSERVACIONES',
		r'RESPONSABLE.*?ENTREGADO',
		r'FIRMAS?',
	]
	regex = '|'.join(patrones)
	secciones = re.split(regex, texto, flags=re.IGNORECASE)
	nombres = ['encabezado', 'liberacion', 'controles_antes', 'controles_durante_post', 'aplicacion_pintura', 'ensayo_adherencia', 'condicion_final', 'observaciones', 'firmas']
	resultado = {}
	for i, nombre in enumerate(nombres):
		if i < len(secciones):
			if nombre == 'encabezado':
				texto_original = secciones[i].strip()
				texto_limpio = limpiar_texto(texto_original)
				relevantes = extraer_lineas_relevantes(texto_limpio)
				resultado[nombre] = {
					'texto_original': texto_original,
					'lineas_relevantes': relevantes,
					'campos': extraer_campos_encabezado(relevantes)
				}
			else:
				resultado[nombre] = secciones[i].strip()
	return resultado

def vista_detecta_formulario(request):
	resultado = None
	json_result = None
	texto = ""
	if request.method == 'POST':
		form = PDFFormularioForm(request.POST, request.FILES)
		if form.is_valid():
			archivo = form.cleaned_data['archivo']
			# Leer PDF y extraer texto
			pdf_reader = PyPDF2.PdfReader(archivo)
			for page in pdf_reader.pages:
				texto += page.extract_text() or ""
			tipo = detectar_protocolo(texto)
			secciones = extraer_secciones(texto)
			resultado = {
				'tipo_protocolo': tipo,
				'secciones': secciones
			}
			json_result = json.dumps(resultado, ensure_ascii=False, indent=2)
	else:
		form = PDFFormularioForm()
	return render(request, 'formularios/detecta_formulario.html', {'form': form, 'resultado': resultado, 'json_result': json_result})

# ================= HERRAMIENTAS EXPERIMENTALES =================

def limpiar_texto(texto):
	# Elimina caracteres no imprimibles y líneas vacías
	texto = re.sub(r'[^\x20-\x7EñÑáéíóúÁÉÍÓÚüÜ\n\r]', '', texto)
	lineas = [l.strip() for l in texto.splitlines() if l.strip()]
	return '\n'.join(lineas)

def extraer_lineas_relevantes(texto):
	claves = ['FECHA', 'UBICACION', 'CLIENTE', 'FABRICANTE', 'PROTOCOLO', 'PLANO', 'VOLT']
	lineas = texto.splitlines()
	relevantes = [l for l in lineas if any(clave in l.upper() for clave in claves)]
	return '\n'.join(relevantes)

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
