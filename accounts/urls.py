from django.urls import path

from . import views

from .views import convenios



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
    # ODONTOGRAMA
    # =========================================

    path(
        'pacientes/<int:id>/odontograma/',
        views.odontograma,
        name='odontograma'
    ),

    # =========================================
    # ANAMNESE
    # =========================================

    path(
        'pacientes/<int:id>/anamnese/',
        views.anamnese,
        name='anamnese'
    ),

    # =========================================
    # FICHA CLÍNICA
    # =========================================

    path(
        'pacientes/<int:id>/ficha-clinica/',
        views.ficha_clinica,
        name='ficha_clinica'
    ),

    # =========================================
    # ORÇAMENTO
    # =========================================

    path(

        'pacientes/<int:id>/orcamento/',

        views.orcamento,

        name='orcamento'

    ),

    # =========================================
    # PROCEDIMENTOS
    # =========================================

    path(
        'procedimentos/',
        views.procedimentos,
        name='procedimentos'
    ),

    # =========================================
    # LOGOUT
    # =========================================

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(

    'convenios/',

    convenios,

    name='convenios'

),

path(
    'procedimentos/editar/<int:id>/',
    views.editar_procedimento,
    name='editar_procedimento'
),

path(
    'procedimentos/excluir/<int:id>/',
    views.excluir_procedimento,
    name='excluir_procedimento'
),


path(
    'convenios/editar/<int:id>/',
    views.editar_convenio,
    name='editar_convenio'
),

path(
    'convenios/excluir/<int:id>/',
    views.excluir_convenio,
    name='excluir_convenio'
),

path(

    'orcamento/item/<int:id>/excluir/',

    views.excluir_item_orcamento,

    name='excluir_item_orcamento'

),

path(

    'orcamento/item/<int:id>/editar/',

    views.editar_item_orcamento,

    name='editar_item_orcamento'

),

path(
    'procedimento/<int:id>/status/',
    views.alterar_status_procedimento,
    name='alterar_status_procedimento'
),

]