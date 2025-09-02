from django.http import HttpResponse

def home(request):
	return HttpResponse("<h1>Bienvenidos</h1>")
