from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('panel/', views.private_home, name='private_home'),
    path('logout/', views.logout_view, name='logout'),
]
