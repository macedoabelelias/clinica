from datetime import date, datetime, timedelta
import json

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.http import JsonResponse
from django.urls import reverse

from .models import Agendamento
from .forms import AgendamentoForm

from accounts.models import Paciente

# =========================================
# AGENDA
# =========================================

def agenda_view(request):

    data_str = request.GET.get('data')

    if data_str:
        data_agenda = datetime.strptime(
            data_str,
            '%Y-%m-%d'
        ).date()
    else:
        data_agenda = date.today()

    agendamentos = Agendamento.objects.filter(
        data=data_agenda
    ).order_by(
        'hora_inicio'
    )

    context = {

        'agendamentos': agendamentos,
        'data_agenda': data_agenda,

        'total_agendado': agendamentos.filter(
            status='agendado'
        ).count(),

        'total_confirmado': agendamentos.filter(
            status='confirmado'
        ).count(),

        'total_atendimento': agendamentos.filter(
            status='atendimento'
        ).count(),

        'total_finalizado': agendamentos.filter(
            status='finalizado'
        ).count(),

    }

    return render(
        request,
        'agenda/calendario.html'
    )

# =========================================
# MOVER AGENDAMENTO
# =========================================

def mover_agendamento(request):

    if request.method == 'POST':

        dados = json.loads(
            request.body
        )

        agendamento = get_object_or_404(
            Agendamento,
            id=dados['agendamento_id']
        )

        agendamento.data = dados['nova_data']

        agendamento.save()

        return JsonResponse({

            'sucesso': True

        })

    return JsonResponse({

        'sucesso': False

    })

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


# =========================================
# NOVO AGENDAMENTO PELO PACIENTE
# =========================================

def novo_agendamento_paciente(request, paciente_id):

    paciente = get_object_or_404(
        Paciente,
        id=paciente_id
    )

    if request.method == 'POST':

        form = AgendamentoForm(
            request.POST
        )

        if form.is_valid():

            agendamento = form.save(
                commit=False
            )

            agendamento.paciente = paciente

            agendamento.save()

            return redirect(
                'agenda'
            )

        else:

            print(form.errors)

    else:

        form = AgendamentoForm(
            initial={
                'paciente': paciente
            }
        )

        # form.fields['paciente'].disabled = True

    return render(

        request,

        'agenda/agendamento_form.html',

        {
            'form': form,
            'paciente': paciente,
        }

    )

# =========================================
# INICIAR ATENDIMENTO
# =========================================

def iniciar_atendimento(request, agendamento_id):

    agendamento = get_object_or_404(
        Agendamento,
        id=agendamento_id
    )

    agendamento.status = 'atendimento'

    agendamento.save()

    return redirect(
        'perfil_paciente',
        id=agendamento.paciente.id
    )

# =========================================
# EDITAR AGENDAMENTO
# =========================================

def editar_agendamento(request, id):

    agendamento = get_object_or_404(
        Agendamento,
        id=id
    )

    form = AgendamentoForm(
        request.POST or None,
        instance=agendamento
    )

    if form.is_valid():

        form.save()

        return redirect(
            'agenda'
        )

    return render(

        request,

        'agenda/agendamento_form.html',

        {

            'form': form,
            'agendamento': agendamento,

        }

    )

# =========================================
# FINALIZAR ATENDIMENTO
# =========================================

def finalizar_atendimento(request, agendamento_id):

    agendamento = get_object_or_404(
        Agendamento,
        id=agendamento_id
    )

    agendamento.status = 'finalizado'

    agendamento.save()

    return redirect(
        'agenda'
    )


# =========================================
# EVENTOS FULLCALENDAR
# =========================================

def eventos_agenda(request):

    eventos = []

    for agendamento in Agendamento.objects.all():

        cor = '#0d6efd'

        if agendamento.status == 'confirmado':
            cor = '#198754'

        elif agendamento.status == 'atendimento':
            cor = '#fd7e14'

        elif agendamento.status == 'finalizado':
            cor = '#6c757d'

        elif agendamento.status == 'cancelado':
            cor = '#dc3545'

        elif agendamento.status == 'faltou':
            cor = '#991b1b'

        eventos.append({

            'id': agendamento.id,

            'title': (
                f'{agendamento.hora_inicio.strftime("%H:%M")} • '
                f'{agendamento.paciente.nome.split()[0]}'
            ),

            'start': str(
                agendamento.data
            ),

            'url': (
                f'/agenda/editar/{agendamento.id}/'
            ),

            'extendedProps': {

                'status': (
                    agendamento.get_status_display()
                ),

                'paciente': (
                    agendamento.paciente.nome
                ),

                'procedimento': (
                    agendamento.procedimento.nome
                    if agendamento.procedimento
                    else 'Não informado'
                ),

                'profissional': (
                    agendamento.profissional.nome
                ),

                'perfil_url': reverse(
                    'perfil_paciente',
                    args=[agendamento.paciente.id]
                ),

                'editar_url': reverse(
                    'editar_agendamento',
                    args=[agendamento.id]
                ),

                'confirmar_url': reverse(
                    'confirmar_agendamento',
                    args=[agendamento.id]
                ),

                'iniciar_url': reverse(
                    'iniciar_atendimento',
                    args=[agendamento.id]
                ),

                'finalizar_url': reverse(
                    'finalizar_atendimento',
                    args=[agendamento.id]
                ),

            },

            'backgroundColor': cor,

            'borderColor': cor,

        })

    return JsonResponse(
        eventos,
        safe=False
    )

# =========================================
# CONFIRMAR AGENDAMENTO
# =========================================

def confirmar_agendamento(request, agendamento_id):

    agendamento = get_object_or_404(
        Agendamento,
        id=agendamento_id
    )

    agendamento.status = 'confirmado'

    agendamento.save()

    return redirect(
        'agenda'
    )