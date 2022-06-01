from django import forms
import datetime

class FormularioProfesores(forms.Form):
    
    nombre = forms.CharField(max_length=22)
    apellido = forms.CharField(max_length=22)
    cumpleaños = forms.DateField()
    bio = forms.CharField()
    camada = forms.IntegerField()
    email = forms.EmailField()
    link_linkedin = forms.URLField()
    link_git = forms.URLField()
    accion = forms.CharField()

class FormularioAlumnos(forms.Form):

    nombre = forms.CharField(max_length=22)
    apellido = forms.CharField(max_length=22)
    cumpleaños = forms.DateField()
    camada = forms.IntegerField()
    cursos = forms.CharField()
    email = forms.EmailField()
    nota = forms.IntegerField()
    accion = forms.CharField()

class FormularioCursos(forms.Form):

    nombre = forms.CharField(max_length=22)
    descripcion = forms.CharField()
    camada = forms.IntegerField()
    cantidad_clases = forms.IntegerField()
    inicio=forms.DateField()
    portada=forms.ImageField()
    tipo=forms.CharField()
    accion = forms.CharField()