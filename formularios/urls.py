from django.urls import path
from . import views
from .views import vista_detecta_formulario

urlpatterns = [
    path('portal-formularios/', views.portal_formularios, name='portal_formularios'),
    path('subir-formulario/', views.subir_formulario, name='subir_formulario'),
    path('eliminar-formulario/<int:formulario_id>/', views.eliminar_formulario, name='eliminar_formulario'),
    path('detecta-formulario/', vista_detecta_formulario, name='detecta_formulario'),
]
