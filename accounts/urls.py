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

    path(
        'pacientes/<int:id>/status/',
        views.alterar_status_paciente,
        name='alterar_status_paciente'
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

   path(
        'pacientes/<int:id>/procedimento-geral/',
        views.salvar_procedimento_geral,
        name='procedimento_geral'
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
        views.convenios,
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
    'documento/<int:id>/pdf/',
    views.imprimir_documento,
    name='imprimir_documento'
),

# =========================================
# USUÁRIOS
# =========================================

path(
    'usuarios/',
    views.usuarios,
    name='usuarios'
),

path(
    'usuarios/novo/',
    views.novo_usuario,
    name='novo_usuario'
),

path(
    'usuarios/<int:id>/editar/',
    views.editar_usuario,
    name='editar_usuario'
),

path(
    'usuarios/<int:id>/ativar/',
    views.ativar_usuario,
    name='ativar_usuario'
),

path(
    'usuarios/<int:id>/desativar/',
    views.desativar_usuario,
    name='desativar_usuario'
),

# =========================================
# MEDICAMENTOS
# =========================================

path(
    'medicamentos/',
    views.medicamentos,
    name='medicamentos'
),

path(
    'medicamentos/novo/',
    views.novo_medicamento,
    name='novo_medicamento'
),

# =========================================
# RECEITAS
# =========================================

path(
    'pacientes/<int:id>/receitas/',
    views.receitas,
    name='receitas'
),

path(
    'pacientes/<int:id>/receita/nova/',
    views.nova_receita,
    name='nova_receita'
),

path(
    'receita/editar/<int:id>/',
    views.editar_receita,
    name='editar_receita'
),

path(
    'receita/excluir/<int:id>/',
    views.excluir_receita,
    name='excluir_receita'
),

path(
    'receita/<int:id>/pdf/',
    views.imprimir_receita,
    name='imprimir_receita'
),

path(
    'modelo-receita/<int:id>/',
    views.buscar_modelo_receita,
    name='buscar_modelo_receita'
),

path(
    'modelos-receita/',
    views.modelos_receita,
    name='modelos_receita'
),

path(
    'modelos-receita/<int:id>/editar/',
    views.editar_modelo_receita,
    name='editar_modelo_receita'
),

path(
    'modelos-receita/<int:id>/excluir/',
    views.excluir_modelo_receita,
    name='excluir_modelo_receita'
),

# =========================================
# EXAMES
# =========================================

path(
    'pacientes/<int:id>/exames/',
    views.exames,
    name='exames'
),

path(
    'pacientes/<int:id>/exame/novo/',
    views.novo_exame,
    name='novo_exame'
),

path(
    'exame/<int:id>/excluir/',
    views.excluir_exame,
    name='excluir_exame'
),

path(
    'pacientes/<int:id>/procedimento-geral/',
    views.salvar_procedimento_geral,
    name='salvar_procedimento_geral'
),

path(
    'documento/excluir/<int:id>/',
    views.excluir_documento,
    name='excluir_documento'
),

# =========================================
# SOLICITAÇÕES DE EXAMES
# =========================================

path(
    'pacientes/<int:id>/solicitacoes-exames/',
    views.solicitacoes_exames,
    name='solicitacoes_exames'
),

path(
    'pacientes/<int:id>/solicitacao-exame/nova/',
    views.nova_solicitacao_exame,
    name='nova_solicitacao_exame'
),

path(
    'solicitacao-exame/<int:id>/excluir/',
    views.excluir_solicitacao_exame,
    name='excluir_solicitacao_exame'
),

path(
    'solicitacao-exame/<int:id>/pdf/',
    views.imprimir_solicitacao_exame,
    name='imprimir_solicitacao_exame'
),

path(
    'fornecedores/',
    views.fornecedores,
    name='fornecedores'
),

path(
    'fornecedores/novo/',
    views.novo_fornecedor,
    name='novo_fornecedor'
),

path(
    'meu-perfil/',
    views.meu_perfil,
    name='meu_perfil'
),

path(
    'alterar-senha/',
    views.alterar_senha,
    name='alterar_senha'
),

path(
    'usuarios/<int:id>/status/',
    views.alterar_status_usuario,
    name='alterar_status_usuario'
),

path(
    'fornecedores/novo/',
    views.novo_fornecedor,
    name='novo_fornecedor'
),

path(
    'fornecedores/<int:fornecedor_id>/editar/',
    views.editar_fornecedor,
    name='editar_fornecedor'
),

path(
    'fornecedores/<int:fornecedor_id>/status/',
    views.alterar_status_fornecedor,
    name='alterar_status_fornecedor'
),

path(
    'fornecedores/<int:fornecedor_id>/excluir/',
    views.excluir_fornecedor,
    name='excluir_fornecedor'
),

# =========================================
# PRODUTOS
# =========================================

path(
    'produtos/',
    views.produtos,
    name='produtos'
),

path(
    'estoque/',
    views.estoque,
    name='estoque'
),

path(
    'estoque/movimentacoes/',
    views.movimentacoes_estoque,
    name='movimentacoes_estoque'
),

path(
    'estoque/movimentacoes/nova/',
    views.nova_movimentacao_estoque,
    name='nova_movimentacao_estoque'
),

path(
    'produtos/novo/',
    views.novo_produto,
    name='novo_produto'
),

path(
    'produtos/<int:produto_id>/editar/',
    views.editar_produto,
    name='editar_produto'
),

path(
    'produtos/<int:produto_id>/status/',
    views.alterar_status_produto,
    name='alterar_status_produto'
),

path(
    'produtos/<int:produto_id>/excluir/',
    views.excluir_produto,
    name='excluir_produto'
),

path(
    'estoque/produtos-criticos/',
    views.produtos_criticos,
    name='produtos_criticos'
),

path(
    'lotes/',
    views.lotes,
    name='lotes'
),

path(
    'lotes/novo/',
    views.novo_lote,
    name='novo_lote'
),

# =========================================
# COMPRAS
# =========================================

path(
    'compras/',
    views.compras,
    name='compras'
),

path(
    'compras/nova/',
    views.nova_compra,
    name='nova_compra'
),

path(
    'compras/<int:compra_id>/',
    views.visualizar_compra,
    name='visualizar_compra'
),

path(
    'compras/<int:compra_id>/editar/',
    views.editar_compra,
    name='editar_compra'
),

path(
    'compras/<int:compra_id>/excluir/',
    views.excluir_compra,
    name='excluir_compra'
),

# =========================================
# CONTAS A PAGAR
# =========================================

path(
    'financeiro/contas-pagar/',
    views.contas_pagar,
    name='contas_pagar'
),

path(
    'financeiro/contas-pagar/nova/',
    views.nova_conta_pagar,
    name='nova_conta_pagar'
),

path(
    'financeiro/contas-pagar/<int:conta_id>/pagar/',
    views.pagar_conta,
    name='pagar_conta'
),

# =========================================
# CONTAS A RECEBER
# =========================================

path(
    'financeiro/contas-receber/',
    views.contas_receber,
    name='contas_receber'
),

path(
    'orcamento/<int:id>/aprovar/',
    views.aprovar_orcamento,
    name='aprovar_orcamento'
),

path(
    'financeiro/contas-receber/<int:conta_id>/receber/',
    views.receber_conta,
    name='receber_conta'
),

path(
    'financeiro/caixa/',
    views.caixa,
    name='caixa'
),

path(
    'orcamentos/central/',
    views.central_orcamentos,
    name='central_orcamentos'
),

path(
    'orcamentos/<int:id>/excluir/',
    views.excluir_orcamento,
    name='excluir_orcamento'
),

# =========================================
# TRATAMENTOS
# =========================================

path(
    "tratamentos/<int:tratamento_id>/encerrar/",
    views.encerrar_tratamento,
    name="encerrar_tratamento",
),



]


