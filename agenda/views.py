from datetime import date, datetime, timedelta
import json

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.http import JsonResponse
from django.urls import reverse

from .models import Agendamento, Profissional
from .forms import AgendamentoForm

from accounts.models import Paciente

from urllib.parse import quote_plus

from django.views.decorators.http import require_POST

from accounts.models import (
    Paciente,
    Procedimento,
    Orcamento,
    ItemOrcamento
)

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

    # =========================================
    # PROFISSIONAL RESPONSÁVEL
    # =========================================

    profissional = None

    if paciente.dentista:

        nome_dentista = (
            paciente.dentista.get_full_name()
            or paciente.dentista.username
        )

        profissional = Profissional.objects.filter(
            nome__icontains=nome_dentista
        ).first()

    # =========================================
    # ORÇAMENTO APROVADO
    # =========================================

    orcamento = Orcamento.objects.filter(
        paciente=paciente,
        status='aprovado'
    ).order_by('-id').first()

    procedimentos_ids = []

    if orcamento:

        procedimentos_ids = ItemOrcamento.objects.filter(
            orcamento=orcamento
        ).values_list(
            'procedimento_id',
            flat=True
        )

    # =========================================
    # POST
    # =========================================

    if request.method == 'POST':

        form = AgendamentoForm(
            request.POST
        )

        if orcamento:

            form.fields['procedimento'].queryset = (
                Procedimento.objects.filter(
                    id__in=procedimentos_ids
                ).distinct()
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

    # =========================================
    # GET
    # =========================================

    else:

        form = AgendamentoForm(
            initial={
                'paciente': paciente,
                'profissional': profissional
            }
        )

        if orcamento:

            form.fields['procedimento'].queryset = (
                Procedimento.objects.filter(
                    id__in=procedimentos_ids
                ).distinct()
            )

        else:

            form.fields['procedimento'].queryset = (
                Procedimento.objects.none()
            )

    return render(

        request,

        'agenda/agendamento_form.html',

        {
            'form': form,
            'paciente': paciente,
            'orcamento': orcamento,
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

from urllib.parse import quote

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

    # =========================================
    # PROFISSIONAL RESPONSÁVEL
    # =========================================

    profissional = Profissional.objects.filter(
        nome=paciente.dentista.get_full_name()
    ).first()

    # =========================================
    # ORÇAMENTO APROVADO
    # =========================================

    orcamento = Orcamento.objects.filter(
        paciente=paciente,
        status='aprovado'
    ).order_by('-id').first()

    procedimentos_ids = []

    if orcamento:

        procedimentos_ids = ItemOrcamento.objects.filter(
            orcamento=orcamento
        ).values_list(
            'procedimento_id',
            flat=True
        )

    # =========================================
    # POST
    # =========================================

    if request.method == 'POST':

        form = AgendamentoForm(request.POST)

        if orcamento:

            form.fields['procedimento'].queryset = (
                Procedimento.objects.filter(
                    id__in=procedimentos_ids
                )
            )

        if form.is_valid():

            agendamento = form.save(
                commit=False
            )

            agendamento.paciente = paciente

            agendamento.save()

            return redirect('agenda')

        else:

            print(form.errors)

    # =========================================
    # GET
    # =========================================

    else:

        form = AgendamentoForm(
            initial={
                'paciente': paciente,
                'profissional': profissional,
            }
        )

        if orcamento:

            form.fields['procedimento'].queryset = (
                Procedimento.objects.filter(
                    id__in=procedimentos_ids
                )
            )

        else:

            form.fields['procedimento'].queryset = (
                Procedimento.objects.none()
            )

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
        print(
            f'ID={agendamento.id} | STATUS={agendamento.status}'
        )

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

        whatsapp_url = '#'

        telefone = (
            agendamento.paciente.whatsapp
            or agendamento.paciente.telefone
            or ''
        )

        if telefone:

            telefone_limpo = ''.join(
                filter(str.isdigit, telefone)
            )

            print(
                f'ID={agendamento.id} | STATUS={agendamento.status}'
            )

            if agendamento.status == 'agendado':

                mensagem = (
                    f'Olá {agendamento.paciente.nome}!\n\n'
                    f'Estamos entrando em contato para confirmar sua consulta.\n\n'
                    f'Data: {agendamento.data.strftime("%d/%m/%Y")}\n'
                    f'Horário: {agendamento.hora_inicio.strftime("%H:%M")}\n'
                    f'Procedimento: '
                    f'{agendamento.procedimento.nome if agendamento.procedimento else "Consulta"}\n\n'
                    f'Por favor, responda esta mensagem confirmando sua presença.'
                )

            elif agendamento.status == 'confirmado':

                mensagem = (
                    f'Olá {agendamento.paciente.nome}!\n\n'
                    f'Lembramos sua consulta.\n\n'
                    f'Data: {agendamento.data.strftime("%d/%m/%Y")}\n'
                    f'Horário: {agendamento.hora_inicio.strftime("%H:%M")}\n'
                    f'Procedimento: '
                    f'{agendamento.procedimento.nome if agendamento.procedimento else "Consulta"}\n\n'
                    f'Aguardamos você!'
                )

            elif agendamento.status == 'atendimento':

                mensagem = (
                    f'Olá {agendamento.paciente.nome}!\n\n'
                    f'Seu atendimento está em andamento.\n\n'
                    f'Caso necessite de alguma informação adicional, estamos à disposição.'
                )

            elif agendamento.status == 'finalizado':

                mensagem = (
                    f'Olá {agendamento.paciente.nome}!\n\n'
                    f'Esperamos que seu atendimento tenha sido excelente.\n\n'
                    f'Caso tenha qualquer dúvida, estamos à disposição.\n\n'
                    f'Obrigado pela confiança!'
                )

            elif agendamento.status == 'faltou':

                mensagem = (
                    f'Olá {agendamento.paciente.nome}!\n\n'
                    f'Notamos que você não compareceu à consulta agendada.\n\n'
                    f'Gostaria de remarcar seu atendimento?\n\n'
                    f'Estamos à disposição.'
                )

            elif agendamento.status == 'cancelado':

                mensagem = (
                    f'Olá {agendamento.paciente.nome}!\n\n'
                    f'Seu agendamento foi cancelado.\n\n'
                    f'Caso deseje, podemos encontrar uma nova data para atendimento.'
                )
            
            elif agendamento.status == 'reagendar':

                mensagem = (
                    f'Olá {agendamento.paciente.nome}!\n\n'
                    f'Gostaríamos de reagendar sua consulta.\n\n'
                    f'Entre em contato conosco para escolhermos um novo horário.'
                )

            else:

                mensagem = (
                    f'Olá {agendamento.paciente.nome}!\n\n'
                    f'Seu agendamento está registrado em nosso sistema.\n\n'
                    f'Data: {agendamento.data.strftime("%d/%m/%Y")}\n'
                    f'Horário: {agendamento.hora_inicio.strftime("%H:%M")}'
                )

            whatsapp_url = (
                'https://api.whatsapp.com/send?phone=55'
                + telefone_limpo
                + '&text='
                + quote_plus(mensagem)
            )

        print(whatsapp_url)   

        eventos.append({

            'id': agendamento.id,

            'title': (
                f'{agendamento.hora_inicio.strftime("%H:%M")} • '
                f'{agendamento.paciente.nome.split()[0]}'
            ),

            'start': str(agendamento.data),

            'url': f'/agenda/editar/{agendamento.id}/',

            'extendedProps': {

                'status': agendamento.get_status_display(),

                'paciente': agendamento.paciente.nome,

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

                'faltou_url': reverse(
                    'marcar_falta',
                    args=[agendamento.id]
                ),

                'cancelar_url': reverse(
                    'cancelar_agendamento',
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

                'whatsapp_url': whatsapp_url,

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


# =========================================
# FALTA
# =========================================

def marcar_falta(request, agendamento_id):

    agendamento = get_object_or_404(
        Agendamento,
        id=agendamento_id
    )

    agendamento.status = 'faltou'

    agendamento.save()

    return redirect(
        'agenda'
    )


# =========================================
# CANCELAR
# =========================================

def cancelar_agendamento(request, agendamento_id):

    agendamento = get_object_or_404(
        Agendamento,
        id=agendamento_id
    )

    agendamento.status = 'cancelado'

    agendamento.save()

    return redirect(
        'agenda'
    )

@require_POST
def alterar_status_ajax(request):

    dados = json.loads(request.body)

    agendamento = get_object_or_404(
        Agendamento,
        id=dados['agendamento_id']
    )

    agendamento.status = dados['status']

    agendamento.save()

    return JsonResponse({
    'sucesso': True,
    'status': agendamento.status
})