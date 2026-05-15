from django.urls import path

from . import views


urlpatterns = [

    # =========================================
    # LOGIN
    # =========================================

    path(
        '',
        views.login_view,
        name='login'
    ),

    # =========================================
    # DASHBOARD
    # =========================================

    path(
        'dashboard/',
        views.dashboard_view,
        name='dashboard'
    ),

    # =========================================
    # PACIENTES
    # =========================================

    path(
        'pacientes/',
        views.pacientes_view,
        name='pacientes'
    ),

    # =========================================
    # PERFIL DO PACIENTE
    # =========================================

    path(
        'pacientes/<int:id>/',
        views.perfil_paciente,
        name='perfil_paciente'
    ),

    # =========================================
    # EDITAR PACIENTE
    # =========================================

    path(

        'pacientes/editar/<int:id>/',

        views.editar_paciente,

        name='editar_paciente'

    ),

    # =========================================
    # LOGOUT
    # =========================================

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

]