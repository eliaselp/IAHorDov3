from django.shortcuts import render,redirect
from django.views import View
# Create your views here.
from django.contrib.auth.models import User
from app import models as app_models
from usuarios.views.perfilView import home
import re

###############################################################################################################
class Admin_Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.rol == "Administrador":
                return render(request, "administrador/home/home.html")
            else:
                return home(request=request)
        else:
            return redirect("login")

    def post(self, request):
        pass

###############################################################################################################
class Estudiantes(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.rol == "Administrador":
                lista_estudiantes = app_models.Estudiante.objects.all()
                return render(request, "administrador/usuarios/estudiante.html",{
                    'lista_estudiantes':lista_estudiantes
                })
            else:
                return home(request=request)
        else:
            return redirect("login")

    def Error(self, request,Error=None,Success=None):
        if request.user.is_authenticated:
            if request.user.rol == "Administrador":
                back = None
                if not Error is None:
                    back = request.POST
                lista_estudiantes = app_models.Estudiante.objects.all()
                return render(request, "administrador/usuarios/estudiante.html",{
                    'Error':Error,'Success':Success,'back':back,
                    'lista_estudiantes':lista_estudiantes
                })
            else:
                return home(request=request)
        else:
            return redirect("login")

    def post(self, request):
        if request.user.is_authenticated:
            if request.user.rol == "Administrador":
                def validar_datos_formulario(post_data):
                    errores = []

                    # Validar nombre (solo letras mayúsculas, minúsculas, espacios y letras en español)
                    nombre = post_data.get('nombre', '').strip()
                    if not nombre:
                        errores.append('El campo "Nombre" es obligatorio.')
                    elif not re.match(r'^[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ\s]+$', nombre):
                        errores.append('El campo "Nombre" solo puede contener letras y espacios.')

                    # Validar apellidos (solo letras mayúsculas, minúsculas, espacios y letras en español)
                    apellidos = post_data.get('apellidos', '').strip()
                    if not apellidos:
                        errores.append('El campo "Apellidos" es obligatorio.')
                    elif not re.match(r'^[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ\s]+$', apellidos):
                        errores.append('El campo "Apellidos" solo puede contener letras y espacios.')

                    # Validar username (solo letras minúsculas)
                    username = post_data.get('username', '').strip()
                    if not username:
                        errores.append('El campo "Username" es obligatorio.')
                    elif not re.match(r'^[a-z0-9]+$', username):
                        errores.append('El campo "Username" solo puede contener letras minúsculas y números.')
                    elif User.objects.filter(username=username).exists() == True:
                        errores.append('El campo "Username" ya esta en uso')

                    # Validar select numérico
                    select_numerico = post_data.get('anio')
                    if not select_numerico or select_numerico not in ['1', '2', '3', '4']:
                        errores.append('El campo "Seleccione un número del 1 al 4" es obligatorio y debe ser un valor entre 1 y 4.')
                    
                    # Validar contraseña
                    contrasena = post_data.get('password1', '').strip()
                    repetir_contrasena = post_data.get('password2', '').strip()
                    if not contrasena:
                        errores.append('El campo "Contraseña" es obligatorio.')
                    elif contrasena != repetir_contrasena:
                        errores.append('Las contraseñas no coinciden.')
                    elif len(contrasena) <= 8:
                        errores.append('La contraseña debe tener más de 8 caracteres.')
                    elif not re.search(r'[A-ZÁÉÍÓÚÜÑ]', contrasena):
                        errores.append('La contraseña debe contener al menos una letra mayúscula.')
                    elif not re.search(r'[a-záéíóúüñ]', contrasena):
                        errores.append('La contraseña debe contener al menos una letra minúscula.')
                    elif not re.search(r'[0-9]', contrasena):
                        errores.append('La contraseña debe contener al menos un número.')
                    elif not re.search(r'[\W_]', contrasena):
                        errores.append('La contraseña debe contener al menos un carácter especial.')

                    if errores:
                        return 'Errores encontrados: ' + ' '.join(errores)
                    return 'OK'


                validacion = validar_datos_formulario(post_data=request.POST)
                if validacion != "OK":
                    return self.Error(request=request,Error=validacion)                   

                usuario = User(
                                username = request.POST.get('username'), 
                                first_name = request.POST.get('nombre'),
                                last_name = request.POST.get('apellidos'), 
                                rol = 'Estudiante',
                            )
                
                usuario.set_password(request.POST.get('password1'))
                usuario.save()

                estudiante = app_models.Estudiante(userid=usuario, anio = request.POST.get('anio'))
                estudiante.save()

                return self.Error(request=request,Success="Estudiante Registrado correctamente")


            else:
                return home(request=request)
        else:
            return redirect("login")

class Eliminar_Estudiante(View):
    def Error(self, request,Error=None,Success=None):
        if request.user.is_authenticated:
            if request.user.rol == "Administrador":
                back = None
                if not Error is None:
                    back = request.POST
                lista_estudiantes = app_models.Estudiante.objects.all()
                return render(request, "administrador/usuarios/estudiante.html",{
                    'Error':Error,'Success':Success,'back':back,
                    'lista_estudiantes':lista_estudiantes
                })
            else:
                return home(request=request)
        else:
            return redirect("login")
        

    def post(self, request):
        if request.user.is_authenticated:
            if request.user.rol == "Administrador":
                id = request.POST.get('estudiante_id')
                if app_models.Estudiante.objects.filter(id=id).exists():
                    est = app_models.Estudiante.objects.get(id=id)
                    est.delete()
                else:
                    return self.Error(request=request,Error="El estudiante no existe")
                return self.Error(request=request, Success="Estudiante eliminado correctamente")
            else:
                return home(request=request)
        else:
            return redirect("login")
        
###############################################################################################################

class Profesor(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.rol == "Administrador":
                lista_profesores = app_models.Profesor.objects.all()
                return render(request, "administrador/usuarios/profesores.html",{
                    'lista_profesores':lista_profesores
                })
            else:
                return home(request=request)
        else:
            return redirect("login")
        
    def Error(self, request, Error=None, Success= None):
        if request.user.is_authenticated:
            if request.user.rol == "Administrador":
                lista_profesores = app_models.Profesor.objects.all()
                return render(request, "administrador/usuarios/profesores.html",{
                    'lista_profesores':lista_profesores,
                    "Error":Error,"Success":Success
                })
            else:
                return home(request=request)
        else:
            return redirect("login")

    def post(self,request):
        def validar_datos_formulario(post_data):
            errores = []

            # Validar nombre (solo letras mayúsculas, minúsculas, espacios y letras en español)
            nombre = post_data.get('nombre', '').strip()
            if not nombre:
                errores.append('El campo "Nombre" es obligatorio.')
            elif not re.match(r'^[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ\s]+$', nombre):
                errores.append('El campo "Nombre" solo puede contener letras y espacios.')

            # Validar apellidos (solo letras mayúsculas, minúsculas, espacios y letras en español)
            apellidos = post_data.get('apellidos', '').strip()
            if not apellidos:
                errores.append('El campo "Apellidos" es obligatorio.')
            elif not re.match(r'^[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ\s]+$', apellidos):
                errores.append('El campo "Apellidos" solo puede contener letras y espacios.')

            # Validar username (solo letras minúsculas)
            username = post_data.get('username', '').strip()
            if not username:
                errores.append('El campo "Username" es obligatorio.')
            elif not re.match(r'^[a-z0-9]+$', username):
                errores.append('El campo "Username" solo puede contener letras minúsculas y números.')

            # Validar categoría docente
            categoria = post_data.get('categoria', '').strip()
            categorias_validas = ["Profesor Titular", "Profesor Auxiliar", "Instructor", "Asistente", "ATD", "RGA"]
            if not categoria or categoria not in categorias_validas:
                errores.append('El campo "Seleccione la Categoría Docente" es obligatorio y debe ser un valor válido.')

            # Validar formación académica
            formacion = post_data.get('formacion', '').strip()
            formaciones_validas = ["Ms.C", "Dr.C"]
            if not formacion or formacion not in formaciones_validas:
                errores.append('El campo "Seleccione la formación académica" es obligatorio y debe ser un valor válido.')

            # Validar grupos_guia (opcional)
            grupos_guia = post_data.get('grupos_guia', '').strip()
            
            # Validar asignatura
            asignatura = post_data.get('asignatura', '').strip()
            if not asignatura:
                errores.append('El campo "Diga la o las Asignaturas" es obligatorio.')

            # Validar select numérico (anio)
            select_numerico = post_data.get('residente')
            anios_validos = ["Si", "No"]
            if not select_numerico or select_numerico not in anios_validos:
                errores.append('El campo "Es residente?" es obligatorio y debe ser "Si" o "No".')

            # Validar contraseña
            contrasena = post_data.get('password1', '').strip()
            repetir_contrasena = post_data.get('password2', '').strip()
            if not contrasena:
                errores.append('El campo "Contraseña" es obligatorio.')
            elif contrasena != repetir_contrasena:
                errores.append('Las contraseñas no coinciden.')
            elif len(contrasena) <= 8:
                errores.append('La contraseña debe tener más de 8 caracteres.')
            elif not re.search(r'[A-ZÁÉÍÓÚÜÑ]', contrasena):
                errores.append('La contraseña debe contener al menos una letra mayúscula.')
            elif not re.search(r'[a-záéíóúüñ]', contrasena):
                errores.append('La contraseña debe contener al menos una letra minúscula.')
            elif not re.search(r'[0-9]', contrasena):
                errores.append('La contraseña debe contener al menos un número.')
            elif not re.search(r'[\W_]', contrasena):
                errores.append('La contraseña debe contener al menos un carácter especial.')

            if errores:
                return 'Errores encontrados: ' + ' '.join(errores)
            return 'OK'
        validacion = validar_datos_formulario(request.POST)
        if validacion != "OK":
            return self.Error(request=request,Error=validacion)

        usuario = User(
                        username = request.POST.get('username'), 
                        first_name = request.POST.get('nombre'),
                        last_name = request.POST.get('apellidos'),
                        rol = 'Profesor'
                    )
        usuario.set_password(request.POST.get('password1'))
        usuario.save()
        profesor = app_models.Profesor(userid = usuario,
                                       guia_grupo = request.POST.get('grupos_guia'),
                                        cat_doc = request.POST.get('categoria'),
                                        formac_acad = request.POST.get('formacion'),
                                        asignatura = request.POST.get('asignatura'),
                                        residente = request.POST.get('residente'    )
                                    )
        profesor.save()

        return self.Error(request=request,Success="Profesor registrado correctamente")




class Eliminar_Profesor(View):
    def Error(self, request, Error=None, Success= None):
        if request.user.is_authenticated:
            if request.user.rol == "Administrador":
                lista_profesores = app_models.Profesor.objects.all()
                return render(request, "administrador/usuarios/profesores.html",{
                    'lista_profesores':lista_profesores,
                    "Error":Error,"Success":Success
                })
            else:
                return home(request=request)
        else:
            return redirect("login")
        

    def post(self, request):
        if request.user.is_authenticated:
            if request.user.rol == "Administrador":
                id = request.POST.get('profesor_id')
                if app_models.Profesor.objects.filter(id=id).exists():
                    pr = app_models.Profesor.objects.get(id=id)
                    pr.delete()
                else:
                    return self.Error(request=request,Error="El profesor no existe")
                return self.Error(request=request, Success="Profesor eliminado correctamente")
            else:
                return home(request=request)
        else:
            return redirect("login")
