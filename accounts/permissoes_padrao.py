from .models import Modulo, Permissao

# =====================================================
# MATRIZ DE PERMISSÕES PADRÃO
# =====================================================

PERMISSOES_PADRAO = {

    "Administrador": {

        "Dashboard": ("v","i","e","x","p"),

        "Agenda": ("v","i","e","x","p"),
        "Pacientes": ("v","i","e","x","p"),
        "Anamnese": ("v","i","e","x","p"),
        "Odontograma": ("v","i","e","x","p"),
        "Tratamentos": ("v","i","e","x","p"),
        "Orçamentos": ("v","i","e","x","p"),

        "Financeiro": ("v","i","e","x","p"),
        "Livro Caixa": ("v","i","e","x","p"),
        "Contas a Receber": ("v","i","e","x","p"),
        "Contas a Pagar": ("v","i","e","x","p"),
        "Fluxo de Caixa": ("v","i","e","x","p"),
        "DRE": ("v","i","e","x","p"),
        "Fechamento Mensal": ("v","i","e","x","p"),

        "Fornecedores": ("v","i","e","x","p"),
        "Produtos": ("v","i","e","x","p"),
        "Compras": ("v","i","e","x","p"),
        "Estoque": ("v","i","e","x","p"),

        "Relatórios": ("v","i","e","x","p"),
        "Auditoria": ("v","i","e","x","p"),

        "Usuários": ("v","i","e","x","p"),
        "Perfis": ("v","i","e","x","p"),
        "Clínica": ("v","i","e","x","p"),
    },

    # =====================================================
    # GESTOR
    # =====================================================

    "Gestor": {

        "Dashboard": ("v",),

        "Agenda": ("v","i","e"),
        "Pacientes": ("v","i","e"),
        "Orçamentos": ("v","i","e"),
        "Tratamentos": ("v",),

        "Financeiro": ("v",),
        "Livro Caixa": ("v",),
        "Contas a Receber": ("v",),
        "Contas a Pagar": ("v",),
        "Fluxo de Caixa": ("v",),
        "DRE": ("v",),
        "Fechamento Mensal": ("v",),

        "Fornecedores": ("v","i","e"),
        "Produtos": ("v","i","e"),
        "Compras": ("v","i","e"),
        "Estoque": ("v","i","e"),

        "Relatórios": ("v","p"),
    },

    # =====================================================
    # DENTISTA
    # =====================================================

    "Dentista": {

        "Dashboard": ("v",),

        "Agenda": ("v",),
        "Pacientes": ("v",),
        "Anamnese": ("v","e"),
        "Odontograma": ("v","e"),
        "Tratamentos": ("v","i","e"),
        "Orçamentos": ("v","i","e"),
    },

    # =====================================================
    # SECRETÁRIA
    # =====================================================

    "Secretária": {

        "Dashboard": ("v",),

        "Agenda": ("v","i","e"),
        "Pacientes": ("v","i","e"),
        "Orçamentos": ("v","i","e"),

        "Financeiro": ("v",),
        "Contas a Receber": ("v","i","e"),

        "Fornecedores": ("v",),
        "Produtos": ("v",),
        "Compras": ("v","i"),
        "Estoque": ("v",),

        "Relatórios": ("v",),
    },

    # =====================================================
    # AUXILIAR DE SAÚDE BUCAL
    # =====================================================

    "Auxiliar de Saúde Bucal": {

        "Dashboard": ("v",),

        "Agenda": ("v",),
        "Pacientes": ("v",),
        "Tratamentos": ("v",),
        "Estoque": ("v",),
        "Produtos": ("v",),
    },

    # =====================================================
    # CONTABILIDADE
    # =====================================================

    "Contabilidade": {

        "Dashboard": ("v",),

        "Financeiro": ("v","i","e","p"),
        "Livro Caixa": ("v","i","e","p"),
        "Contas a Receber": ("v","i","e","p"),
        "Contas a Pagar": ("v","i","e","p"),
        "Fluxo de Caixa": ("v","i","e","p"),
        "DRE": ("v","p"),
        "Fechamento Mensal": ("v","p"),

        "Relatórios": ("v","p"),
    },

    # =====================================================
    # MARKETING
    # =====================================================

    "Marketing": {

        "Dashboard": ("v",),
        "Relatórios": ("v","p"),
    },

    # =====================================================
    # AUDITORIA
    # =====================================================

    "Auditoria": {

        "Dashboard": ("v",),

        "Agenda": ("v",),
        "Pacientes": ("v",),
        "Anamnese": ("v",),
        "Odontograma": ("v",),
        "Tratamentos": ("v",),
        "Orçamentos": ("v",),

        "Financeiro": ("v",),
        "Livro Caixa": ("v",),
        "Contas a Receber": ("v",),
        "Contas a Pagar": ("v",),
        "Fluxo de Caixa": ("v",),
        "DRE": ("v",),
        "Fechamento Mensal": ("v",),

        "Fornecedores": ("v",),
        "Produtos": ("v",),
        "Compras": ("v",),
        "Estoque": ("v",),

        "Relatórios": ("v",),
        "Auditoria": ("v",),

        "Usuários": ("v",),
        "Perfis": ("v",),
        "Clínica": ("v",),
    },
}

# =====================================================
# APLICAR PERMISSÕES PADRÃO
# =====================================================

def aplicar_permissoes_padrao(perfil):

    permissoes = PERMISSOES_PADRAO.get(perfil.nome)

    if not permissoes:
        return

    for nome_modulo, acoes in permissoes.items():

        try:
            modulo = Modulo.objects.get(
                nome=nome_modulo,
                ativo=True
            )

        except Modulo.DoesNotExist:
            continue

        permissao, _ = Permissao.objects.get_or_create(
            perfil=perfil,
            modulo=modulo
        )

        permissao.visualizar = "v" in acoes
        permissao.inserir = "i" in acoes
        permissao.editar = "e" in acoes
        permissao.excluir = "x" in acoes
        permissao.exportar = "p" in acoes

        permissao.save()