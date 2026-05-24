from django.contrib import admin

from .models import Paciente

from .models import Convenio


admin.site.register(Paciente)

admin.site.register(Convenio)
