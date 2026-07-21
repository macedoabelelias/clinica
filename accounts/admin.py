from django.contrib import admin

from .models import (
    Auditoria,
    PerfilUsuario,
    Produto,
    TemplateDocumento,
    Tratamento,
)


# =========================================
# PRODUTOS
# =========================================

admin.site.register(Produto)


# =========================================
# TEMPLATE DOCUMENTOS
# =========================================

admin.site.register(TemplateDocumento)


# =========================================
# PERFIL USUÁRIO
# =========================================

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):

    list_display = (

        "usuario",

        "tipo_usuario",

        "cro",

        "ativo",

        "somente_leitura",

    )

    list_filter = (

        "tipo_usuario",

        "ativo",

    )

    search_fields = (

        "usuario__username",

        "usuario__first_name",

        "usuario__last_name",

        "cro",

    )


# =========================================
# TRATAMENTOS
# =========================================

@admin.register(Tratamento)
class TratamentoAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "paciente",

        "titulo",

        "status",

        "data_inicio",

        "data_encerramento",

    )

    list_filter = (

        "status",

    )

    search_fields = (

        "paciente__nome",

        "titulo",

    )


# =========================================
# AUDITORIA
# =========================================

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):

    list_display = (

        "data_hora",

        "usuario",

        "modulo",

        "acao",

        "nivel",

    )

    list_filter = (

        "modulo",

        "acao",

        "nivel",

        "data_hora",

    )

    search_fields = (

        "usuario__username",

        "usuario__first_name",

        "usuario__last_name",

        "descricao",

        "modulo",

    )

    ordering = (

        "-data_hora",

    )

    readonly_fields = (

        "usuario",

        "modulo",

        "acao",

        "nivel",

        "descricao",

        "objeto_id",

        "ip",

        "data_hora",

    )

    def has_add_permission(self, request):

        return False

    def has_delete_permission(self, request, obj=None):

        return False