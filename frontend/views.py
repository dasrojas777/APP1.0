from django.contrib.auth import logout

def logout_view(request):
	logout(request)
	return redirect('home')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label='Usuario', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('private_home')
			else:
				messages.error(request, 'Usuario o contraseña incorrectos')
	else:
		form = LoginForm()
	return render(request, 'frontend/login.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def private_home(request):
	return render(request, 'frontend/private_home.html')

def home(request):
	return render(request, 'frontend/home.html')


def register_view(request):
	from .forms import RegisterForm
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data['password'])
			user.save()
			messages.success(request, 'Usuario registrado correctamente. Ahora puedes iniciar sesión.')
			return redirect('login')
	else:
		form = RegisterForm()
	return render(request, 'frontend/register.html', {'form': form})
