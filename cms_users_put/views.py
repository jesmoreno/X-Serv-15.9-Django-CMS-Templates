# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from models import Tabla
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context

# Create your views here.
def contenido():
    salida = "<p><b>Lista personas</b></p>"
    fechas = Tabla.objects.all()
    for fila in fechas:
        salida += "<p>" + fila.nombre + " con fecha: " + str(fila.fecha) + "</p>"
    return salida

@csrf_exempt
def server(request):
    verb = request.method
    recurso = request.path

    if verb == 'GET':
        if recurso == '/':
            texto = contenido()
            print texto
            return HttpResponse("<html>"
                                "<a href= http://127.0.0.1:1234/cerrar_sesion>"
                                "<p align = right>Cerrar sesion</a></p>"
                                "<h1>Insertar en el put con el siguiente formato:</h1>"
                                "<p>nombre,fecha(YYYY-MM-DD)</p>"+
                                "<body>"+
                                texto+
                                "<body>"+
                                "</html>")
        else:
            try:
                record = Tabla.objects.get(nombre = recurso[1:])
                return HttpResponse("<p>Fecha de "+recurso[1:]+"= "+ str(record.fecha) +"</p>")
            except Tabla.DoesNotExist:
                return HttpResponseNotFound("Page not found: %s." % recurso[1:])

    elif verb == 'PUT':
        cuerpo = request.body.split(',')
        name = cuerpo[0]
        date = cuerpo[1]
        db = Tabla(nombre = name,fecha = date)
        db.save()
        return HttpResponse('<h1>Nombre y fecha almacenados</h1>')


@csrf_exempt     
def authenticated(request):

    if request.user.is_authenticated():
        return HttpResponse(server(request))
    else:
        verb = request.method
        
        if verb == 'GET':
            texto = contenido()
            return HttpResponse("<html>"
                                "<a href= http://127.0.0.1:1234/nuevo_usuario>"
                                "<p align = right>Registrarse</a></p>"
                                "<a href= http://127.0.0.1:1234/inicio_sesion>"
                                "<p align = right>Iniciar sesion</a></p>"+
                                texto+
                                "</html>")
        elif verb == 'PUT':
            return HttpResponse("<p>Registrarse para insertar</p>")


@csrf_exempt     
def authenticatedAnnotated(request):

    if request.user.is_authenticated():
        return HttpResponse(server(request))
    else:
        verb = request.method
        
        if verb == 'GET':
            texto = contenido()
            #Indicar plantilla
            plantilla = get_template('index.html')
            #Definir el contexto
            c = Context({'title': "Página cumpleaños",'content': texto, 'parrafo':"Lista personas", 'Registro': "Registrarse",'Inicio':"Inicio sesion"})
            #Renderizar
            renderizado = plantilla.render(c)
            return HttpResponse(renderizado)

        elif verb == 'PUT':
            return HttpResponse("<p>Registrarse para insertar</p>")

def css(request):
    
    #Indicar plantilla
    plantilla = get_template('images/style.css')
    #Definir el contexto
    c = Context()
    #Renderizar
    renderizado = plantilla.render(c)

    return HttpResponse(renderizado, content_type = 'text/css')

@csrf_exempt
def signUp(request):
    
    verb = request.method
    if verb == 'GET':    
        return HttpResponse("<html>"
                            "<body>"
                            "<h1>NUEVO USUARIO</h1>"
                            "<form action = http://127.0.0.1:1234/nuevo_usuario method=POST>"
                            "Nombre: <input type= text  name = nombre><br>"
                            "Contraseña: <input type= password name = passw></br>"
                            "<input type= submit value= Enviar >"
                            "</form>"
                            "</body>"
                            "</html>")

    elif verb == 'POST':
        usuario = request.body.split('&')[0].split('=')[1]
        passw = request.body.split('&')[1].split('=')[1]
        user = User.objects.create_user(usuario, '/', passw)
        return HttpResponse("<html>"
                            "<body>"
                            "<p><b>Usuario registrado</b></p>"
                            "<a href= http://127.0.0.1:1234/inicio_sesion>"
                            "Iniciar sesión</a></p>"
                            "</body>"
                            "</html>")

@csrf_exempt
def signIn(request):

    verb = request.method

    if verb == 'GET':    
        return HttpResponse("<html>"
                            "<body>"
                            "<h1>INICIAR SESIÓN</h1>"
                            "<form action = http://127.0.0.1:1234/inicio_sesion method=POST>"
                            "Nombre: <input type= text  name = nombre><br>"
                            "Contraseña: <input type= password name = passw></br>"
                            "<input type= submit value= Enviar >"
                            "</form>"
                            "</body>"
                            "</html>")

    elif verb == 'POST':

        usuario = request.body.split('&')[0].split('=')[1]
        passw = request.body.split('&')[1].split('=')[1]
        user = authenticate(username= usuario, password= passw)

        if user is not None:
        
            if user.is_active:
                login(request, user)
                print("User is valid, active and authenticated")
                return HttpResponse("<html>"
                                "<body>"
                                "<p>¡Bienvenido "+usuario+"!"+"</p>"
                                "<a href= http://127.0.0.1:1234>"
                                "<p align = left>Ir a la página principal</a></p>"
                                "</body>"
                                "</html>")
            else:
                print("The password is valid, but the account has been disabled!")
                return HttpResponse("<html>"
                                    "<body>"
                                    "<p>Usuario deshablitado</p>"
                                    "<a href= http://127.0.0.1:1234>"
                                    "<p align = left>Ir a pagina principal</a></p>"
                                    "</body>"
                                    "</html>")
        else:
            
            print("The username and password were incorrect.")
            return HttpResponse("<html>"
                                "<p>Contraseña o usuario incorrectos</p>"
                                "<body>"
                                "<h1>INICIAR SESION</h1>"
                                "<form action = http://127.0.0.1:1234/inicio_sesion method=POST>"
                                "Nombre: <input type= text  name = nombre><br>"
                                "Contraseña: <input type= password name = passw></br>"
                                "<input type= submit value= Enviar >"
                                "</form>"
                                "</body>"
                                "</html>")


def logOut(request):

    logout(request)
    return HttpResponse("<html>"
                       "<p>Sesión cerrada</p>"
                       "<body>"
                       "<a href= http://127.0.0.1:1234>"
                       "<p align = left>Ir a pagina principal</a></p>"
                       "</body>"
                       "</html>")



   
