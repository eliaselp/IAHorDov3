
from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.Admin_Home.as_view(), name='admin_home'),
    path('usuarios/estudiantes/',views.Estudiantes.as_view(),name="admin_usuario_estudiantes"),
    path('usuarios/estudiantes/eliminar/',views.Eliminar_Estudiante.as_view(),name="admin_usuario_estudiantes_eliminar"),

    path('usuarios/profesor/',views.Profesor.as_view(),name="admin_usuario_profesor"),
    path('usuarios/profesor/eliminar/',views.Eliminar_Profesor.as_view(),name="admin_usuario_profesor_eliminar"),
]
