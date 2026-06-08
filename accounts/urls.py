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
        'pacientes/novo/',
        views.novo_paciente,
        name='novo_paciente'
    ),

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

    path(
        'pacientes/excluir/<int:id>/',
        views.excluir_paciente,
        name='excluir_paciente'
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
    
    path(
        'pacientes/<int:id>/anexo/',
        views.upload_anexo,
        name='upload_anexo'
    ),

    # =========================================
    # ORÇAMENTO
    # =========================================

    path(
        'pacientes/<int:id>/orcamento/',
        views.orcamento,
        name='orcamento'
    ),

    path(
        'orcamento/<int:id>/pdf/',
        views.gerar_pdf_orcamento,
        name='gerar_pdf_orcamento'
    ),

    path(
        'documento/novo/<int:id>/',
        views.novo_documento,
        name='novo_documento'
    ),

    path(
        'documento/editar/<int:id>/',
        views.editar_documento,
        name='editar_documento'
    ),

    path(
        'documento/visualizar/<int:id>/',
        views.visualizar_documento,
        name='visualizar_documento'
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

path(

    'pacientes/<int:id>/prontuario/pdf/',

    views.imprimir_prontuario,

    name='imprimir_prontuario'

),

path(
    'pacientes/<int:id>/anamnese/pdf/',
    views.imprimir_anamnese,
    name='imprimir_anamnese'
),

path(
    'configuracao-clinica/',
    views.configuracao_clinica,
    name='configuracao_clinica'
),



path(
    'pacientes/<int:id>/procedimento-geral/',
    views.salvar_procedimento_geral,
    name='salvar_procedimento_geral'
)

]

