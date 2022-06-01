from django.shortcuts import render,redirect,HttpResponse
from django.conf import settings
from django.db.models import Q
from .models import Profesores,Cursos, Alumnos
from django.contrib.auth import authenticate, login
from app_coder.forms import FormularioAlumnos, FormularioCursos, FormularioProfesores

def ingresar(request):
    username = request.POST.get('username',None)
    password = request.POST.get('password',None)
    user = authenticate(request, username=username, password=password)  
    if user:
        login(request, user)
        return redirect('/')
    else:
        return HttpResponse('NOLOGIN')
        


def home(request):

    return render(request, 'home.html')

def profesores(request):
    login = False
    if request.user.is_authenticated:
        login = True
        
    profesores = Profesores.objects.all
    return render(request, 'profesores.html', {'profesores':profesores})

def alumnos(request):
    alumnos = []
    puesto = 0

    for x in Alumnos.objects.all().order_by('-nota'):
        alumnos.append({puesto:{}})
        alumnos[puesto].update({
            'id':x.id, 
            'nombre':x.nombre,
            'apellido':x.apellido,
            'camada':x.camada,
            'nota':x.nota, 
            'puesto':puesto + 1})
        puesto += 1
    return render(request, 'alumnos.html',{'alumnos':alumnos})

def cursos(request):
    colores = {"BACKEND": '#900C3F', "WEB": '#581845',"DISEÑO": '#FFC300',"DEVOPS": '#C70039'}
    cursos = []
    k = 0

    for key,val in colores.items():
        objeto = (Cursos.objects.filter(tipo=key))
        for x in objeto:
            cursos.append({k:{}})
            cursos[k].update({
                'nombre':x.nombre, 
                'descripcion':x.descripcion, 
                'color':val, 
                'portada':x.portada, 
                'tipo': x.tipo})
            k +=1
            
    return render(request, 'cursos.html', {'cursos': cursos})

def panel(request):
    active = 'buscar'
    consulta = set()

    if request.GET:
        if request.GET['active'] == 'profesores':
            active = request.GET['active']
            consulta = Profesores.objects.all()
        if request.GET['active'] == 'alumnos':
            active = request.GET['active']
            consulta = Alumnos.objects.all()
        if request.GET['active'] == 'cursos':
            active = request.GET['active']
            consulta = Cursos.objects.all()
    
    if request.POST:
        
        if request.POST['borrar']:
            db = ''
            consulta = set()
            if request.POST['db'] == 'cursos':
                db = Cursos(id=request.POST['borrar'])
                db.delete()
                db = f'Se borro: ID:{request.POST["borrar"]} DB: {request.POST["db"]} '
                consulta = Cursos.objects.all()
            elif request.POST['db'] == 'profesores':
                db = Profesores(id=request.POST['borrar'])
                db.delete()
                db = f'Se borro: ID:{request.POST["borrar"]} DB: {request.POST["db"]} '
                consulta = Profesores.objects.all()
            elif request.POST['db'] == 'alumnos':
                db = Alumnos(id=request.POST['borrar'])
                db.delete()
                db = f'Se borro: ID:{request.POST["borrar"]} DB: {request.POST["db"]} '
                consulta = Alumnos.objects.all()
            
            return render(request, 'panel.html', {'active':request.POST['db'], 'consulta':consulta, 'mensaje': db})


    return render(request, 'panel.html', {'active':active, 'consulta': consulta})
    
def buscar(request):

    if request.GET['buscar']:
        buscar = request.GET['buscar']
        profesores = Profesores.objects.filter(Q(nombre__icontains = buscar) | Q(apellido__icontains = buscar))
        alumnos = Alumnos.objects.filter(Q(nombre__icontains = buscar) | Q(apellido__icontains = buscar))
        cursos = Cursos.objects.filter(nombre__icontains = buscar)
        
        return render(request, 'resultados.html', {'profesores':profesores, 'alumnos':alumnos, 'cursos': cursos, 'busqueda':buscar,'active':'buscar'})
    else:
        return render(request,'resultados.html')

def editar(request):
    formulario = ''

    if request.POST:
        if request.POST['accion'] == 'profesores':
            formulario = FormularioProfesores(request.POST)
        elif request.POST['accion'] == 'alumnos':
            formulario = FormularioAlumnos(request.POST)
        elif request.POST['accion'] == 'cursos':
            formulario = FormularioCursos(request.POST)

    if formulario.is_valid():
        if formulario.cleaned_data:
            datos = formulario.cleaned_data
        else:
            return HttpResponse(formulario.errors)
        if request.POST['accion'] == 'profesores':
            guardar = Profesores(
                id=request.POST['id'],
                nombre=datos['nombre'],
                apellido=datos['apellido'],
                cumpleaños=datos['cumpleaños'],
                bio=datos['bio'],
                camada=datos['camada'],
                foto=request.FILES['foto'],
                email=datos['email'],
                link_linkedin=datos['link_linkedin'],
                link_git=datos['link_git']
            )
            guardar.save()
            consulta = Profesores.objects.all()
            return render(request, 'panel.html', {'consulta': consulta, 'active':'profesores', 'mensaje': f'Se actualizo a: {request.POST["id"]} - {datos["nombre"]} {datos["apellido"]}'})
        
        if request.POST['accion'] == 'alumnos':
            guardar = Alumnos(
                id=request.POST['id'],
                nombre=datos['nombre'],
                apellido=datos['apellido'],
                cumpleaños=datos['cumpleaños'],
                camada=datos['camada'],
                foto=request.FILES['foto'],
                cursos=datos['cursos'],
                email=datos['email'],
                nota=datos['nota']
            )
            guardar.save()
            consulta = Alumnos.objects.all()
            return render(request, 'panel.html', {'consulta': consulta, 'active':'alumnos', 'mensaje': f'Se actualizo a: {request.POST["id"]} - {datos["nombre"]} {datos["apellido"]}'})
        
        if request.POST['accion'] == 'cursos':
            guardar = Cursos(
                id=request.POST['id'],
                nombre=datos['nombre'],
                descripcion=datos['descripcion'],
                camada=datos['camada'],
                cantidad_clases=datos['cantidad_clases'],
                inicio=datos['inicio'],
                portada=request.FILES['portada'],
                tipo=datos['tipo'],
                nota=datos['nota']
            )
            guardar.save()
            consulta = Cursos.objects.all()
            return render(request, 'panel.html', {'consulta': consulta, 'active':'cursos', 'mensaje': f'Se actualizo a: {request.POST["id"]} - {datos["nombre"]} {datos["apellido"]}'})
    

def nuevo(request):
    formulario = ''

    if request.POST:
        if request.POST['db'] == 'profesores':
            formulario = FormularioProfesores(request.POST)
        elif request.POST['db'] == 'alumnos':
            formulario = FormularioAlumnos(request.POST)
        elif request.POST['db'] == 'cursos':
            formulario = FormularioCursos(request.POST)

    if formulario.is_valid():
        if formulario.cleaned_data:
            datos = formulario.cleaned_data
        else:
            return HttpResponse(formulario.errors)
        if request.POST['db'] == 'profesores':
            guardar = Profesores(
                nombre=datos['nombre'],
                apellido=datos['apellido'],
                cumpleaños=datos['cumpleaños'],
                bio=datos['bio'],
                camada=datos['camada'],
                foto=request.FILES['foto'],
                email=datos['email'],
                link_linkedin=datos['link_linkedin'],
                link_git=datos['link_git']
            )
            guardar.save()
            consulta = Profesores.objects.all()
            return render(request, 'panel.html', {'consulta': consulta, 'active':'profesores', 'mensaje': f'Se creo un nuevo registro para: {datos["nombre"]} {datos["apellido"]}'})
        
        if request.POST['db'] == 'alumnos':
            guardar = Alumnos(
                nombre=datos['nombre'],
                apellido=datos['apellido'],
                cumpleaños=datos['cumpleaños'],
                camada=datos['camada'],
                foto=request.FILES['foto'],
                cursos=datos['cursos'],
                email=datos['email'],
                nota=datos['nota']
            )
            guardar.save()
            consulta = Alumnos.objects.all()
            return render(request, 'panel.html', {'consulta': consulta, 'active':'alumnos', 'mensaje': f'Se creo un nuevo registro para: {datos["nombre"]} {datos["apellido"]}'})
        
        if request.POST['db'] == 'cursos':
            guardar = Cursos(
                nombre=datos['nombre'],
                descripcion=datos['descripcion'],
                camada=datos['camada'],
                cantidad_clases=datos['cantidad_clases'],
                inicio=datos['inicio'],
                portada=request.FILES['portada'],
                tipo=datos['tipo'],
                nota=datos['nota']
            )
            guardar.save()
            consulta = Cursos.objects.all()
            return render(request, 'panel.html', {'consulta': consulta, 'active':'cursos', 'mensaje': f'Se creo un nuevo registro para: {datos["nombre"]} {datos["apellido"]}'})
    