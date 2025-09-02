from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def portal_formularios(request):
	return render(request, 'formularios/portal.html')
from django.shortcuts import render

# Create your views here.
