from django.contrib import admin

from .models import (
    TemplateDocumento
)

from .models import PerfilUsuario

from .models import Produto

admin.site.register(Produto)

from .models import Tratamento


# =========================================
# TEMPLATE DOCUMENTOS
# =========================================

admin.site.register(
    TemplateDocumento
)


# =========================================
# PERFIL USUARIO ADMINISTRADOR
# =========================================

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):

    list_display = (

        'usuario',

        'tipo_usuario',

        'cro',

        'ativo',

        'somente_leitura'

    )

    list_filter = (

        'tipo_usuario',

        'ativo'

    )

    search_fields = (

        'usuario__username',

        'usuario__first_name',

        'usuario__last_name',

        'cro'

    )

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