from django.urls import path
from app_coder import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('ingresar', views.ingresar, name='ingresar'),
    path('profesores', views.profesores, name='profesores'),
    path('alumnos', views.alumnos, name='alumnos'),
    path('cursos', views.cursos, name='cursos'),
    path('panel',views.panel, name='panel'),
    path('buscar', views.buscar ),
    path('editar', views.editar),
    path('nuevo', views.nuevo),
    path(r'^$', LoginView.as_view(), name= 'login'),
    path(r'^logout$', LogoutView.as_view(), name= 'logout'),
]
