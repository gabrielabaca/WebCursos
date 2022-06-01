from email.policy import default
from django.db import models

# Create your models here.

class Cursos(models.Model):
    CURSOS_CHOICES = (
    ("WEB", "Desarrollo WEB"),
    ("BACKEND", "Desarrollo BackEnd"),
    ("DISEÑO", "Diseño Grafico"),
    ("DEVOPS", "DevOps"),
)
    nombre = models.CharField(max_length=22)
    descripcion = models.TextField()
    camada = models.IntegerField()
    cantidad_clases = models.IntegerField()
    inicio=models.DateField()
    portada=models.ImageField(upload_to='cursos/portadas/', default='')
    tipo=models.TextField(max_length=40,choices=CURSOS_CHOICES, default='')

class Profesores(models.Model):
    nombre = models.CharField(max_length=22)
    apellido = models.CharField(max_length=22)
    cumpleaños = models.DateField()
    bio = models.TextField()
    camada = models.IntegerField()
    foto = models.ImageField(upload_to='perfiles/profesores/')
    email = models.EmailField(default='mail@mail.com')
    link_linkedin = models.URLField()
    link_git = models.URLField()
    

class Alumnos(models.Model):
    nombre = models.CharField(max_length=22)
    apellido = models.CharField(max_length=22)
    cumpleaños = models.DateField()
    camada = models.IntegerField()
    foto = models.ImageField(upload_to='perfiles/alumnos')
    cursos = models.TextField()
    email = models.EmailField(default='mail@mail.com')
    nota = models.IntegerField(default='0')