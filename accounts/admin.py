from django.contrib import admin

from .models import Paciente

from .models import Convenio


admin.site.register(Paciente)

admin.site.register(Convenio)

from .models import (
    TemplateDocumento,
    DocumentoClinico
)

admin.site.register(TemplateDocumento)
admin.site.register(DocumentoClinico)

from .models import ConfiguracaoClinica

admin.site.register(
    ConfiguracaoClinica
)
