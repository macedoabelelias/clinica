from django.contrib import admin

from .models import (
    TemplateDocumento
)

from .models import PerfilUsuario


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