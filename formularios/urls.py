from django.urls import path
from . import views

urlpatterns = [
    path('portal-formularios/', views.portal_formularios, name='portal_formularios'),
    path('subir-formulario/', views.subir_formulario, name='subir_formulario'),
    path('eliminar-formulario/<int:formulario_id>/', views.eliminar_formulario, name='eliminar_formulario'),
]
