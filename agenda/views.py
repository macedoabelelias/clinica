from django.shortcuts import render

from .models import Agendamento

from django.shortcuts import (
    render,
    redirect
)

from .forms import AgendamentoForm

# =========================================
# AGENDA
# =========================================

def agenda_view(request):

    agendamentos = Agendamento.objects.all().order_by(
        'data',
        'hora_inicio'
    )

    context = {
        'agendamentos': agendamentos
    }

    return render(
        request,
        'agenda/agenda.html',
        context
    )

# =========================================
# NOVO AGENDAMENTO
# =========================================

def novo_agendamento(request):

    form = AgendamentoForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect(
            'agenda'
        )

    context = {

        'form': form

    }

    return render(

        request,

        'agenda/agendamento_form.html',

        context

    )