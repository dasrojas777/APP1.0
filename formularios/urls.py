from django.urls import path
from . import views

urlpatterns = [
    path('portal-formularios/', views.portal_formularios, name='portal_formularios'),
]
