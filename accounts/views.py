import os

from django.conf import settings

from django.http import (
    HttpResponse,
    JsonResponse
)

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.decorators import (
    login_required
)

from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    HRFlowable
)

from .models import (
    Convenio,
    EvolucaoClinica,
    ProntuarioClinico,
    DocumentoClinico,
    TemplateDocumento,
    Paciente,
    Anamnese,
    Procedimento,
    Orcamento,
    ItemOrcamento,
    AnexoPaciente,
    ConfiguracaoClinica,
    Medicamento,
    Receita,
    ModeloReceita,
    Exame,
    SolicitacaoExame,
    Fornecedor,
    Produto,
    Compra,
    ItemCompra,
    MovimentacaoEstoque,
    LoteProduto,
    ContaPagar
)

from .forms import (
    ProcedimentoForm,
    ItemOrcamentoForm,
    ConvenioForm
)

from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib import messages
from .models import PerfilUsuario
from .permissions import perfil_required
from django.contrib.auth import update_session_auth_hash
from .models import Compra, ItemCompra
from decimal import Decimal
from .models import Produto
from .models import Compra

# =========================================
# LOGIN
# =========================================

def login_view(request):

    erro = None

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(

            request,
            username=username,
            password=password

        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            erro = 'Usuário ou senha inválidos.'

    return render(

        request,

        'accounts/login.html',

        {

            'erro': erro

        }

    )


# =========================================
# DASHBOARD
# =========================================

@login_required(login_url='/')
def dashboard_view(request):

    return render(

        request,

        'accounts/dashboard.html'

    )

# =========================================
# PACIENTES
# =========================================

@login_required(login_url='/')
def pacientes_view(request):

    # =========================================
    # CADASTRAR PACIENTE
    # =========================================

    if request.method == 'POST':

        Paciente.objects.create(

            # FOTO
            foto=request.FILES.get('foto'),

            # DADOS PESSOAIS
            nome=request.POST.get('nome'),
            cpf=request.POST.get('cpf'),
            rg=request.POST.get('rg'),
            nascimento=request.POST.get('nascimento') or None,
            genero=request.POST.get('genero'),
            estado_civil=request.POST.get('estado_civil'),
            profissao=request.POST.get('profissao'),

            # CONTATO
            telefone=request.POST.get('telefone'),
            whatsapp=request.POST.get('whatsapp'),
            email=request.POST.get('email'),

            # ENDEREÇO
            cep=request.POST.get('cep'),
            endereco=request.POST.get('endereco'),
            numero=request.POST.get('numero'),
            complemento=request.POST.get('complemento'),
            bairro=request.POST.get('bairro'),
            cidade=request.POST.get('cidade'),
            estado=request.POST.get('estado'),

            # CLÍNICO
            convenio=request.POST.get('convenio'),
            carteirinha=request.POST.get('carteirinha'),
            alergias=request.POST.get('alergias'),
            medicamentos=request.POST.get('medicamentos'),
            observacoes=request.POST.get('observacoes'),

            # RESPONSÁVEL
            responsavel=request.POST.get('responsavel'),

            cpf_responsavel=request.POST.get(
                'cpf_responsavel'
            ),

            telefone_responsavel=request.POST.get(
                'telefone_responsavel'
            ),

            dentista_id=request.POST.get('dentista') or None,

        )

        return redirect('pacientes')

    # =========================================
    # LISTAGEM
    # =========================================

    perfil = request.user.perfil.tipo_usuario

    if perfil == 'dentista':

        pacientes = Paciente.objects.filter(
            dentista=request.user
        ).order_by('-id')

    else:

        pacientes = Paciente.objects.all().order_by('-id')

    convenios = Convenio.objects.filter(
        ativo=True
    ).order_by('nome')

    dentistas = User.objects.filter(
        perfil__tipo_usuario='dentista'
    ).order_by('first_name')

    context = {
        'pacientes': pacientes,
        'convenios': convenios,
        'dentistas': dentistas,
    }

    return render(

        request,

        'accounts/pacientes.html',

        context

    )

# =========================================
# PERFIL DO PACIENTE
# =========================================

@login_required(login_url='/')
def perfil_paciente(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    agendamentos = list(

        paciente.agendamentos.filter(
            status__in=[
                'agendado',
                'confirmado',
                'atendimento'
            ]
        ).order_by(
            '-data',
            '-hora_inicio'
        )[:4]

    )

    agendamentos.reverse()

    return render(

        request,

        'accounts/perfil.html',

        {

            'paciente': paciente,
            'agendamentos': agendamentos,

        }

    )
# =========================================
# LOGOUT
# =========================================

def logout_view(request):

    logout(request)

    return redirect('/')

# =========================================
# NOVO PACIENTE
# =========================================

@login_required(login_url='/')
def novo_paciente(request):

    if request.method == 'POST':

        paciente = Paciente.objects.create(

            dentista=request.user,

            foto=request.FILES.get('foto'),

            nome=request.POST.get('nome'),
            cpf=request.POST.get('cpf'),
            rg=request.POST.get('rg'),
            nascimento=request.POST.get('nascimento') or None,

            genero=request.POST.get('genero'),
            estado_civil=request.POST.get('estado_civil'),
            profissao=request.POST.get('profissao'),

            telefone=request.POST.get('telefone'),
            whatsapp=request.POST.get('whatsapp'),
            email=request.POST.get('email'),

            cep=request.POST.get('cep'),
            endereco=request.POST.get('endereco'),
            numero=request.POST.get('numero'),
            complemento=request.POST.get('complemento'),
            bairro=request.POST.get('bairro'),
            cidade=request.POST.get('cidade'),
            estado=request.POST.get('estado'),

            convenio=request.POST.get('convenio'),
            carteirinha=request.POST.get('carteirinha'),

            alergias=request.POST.get('alergias'),
            medicamentos=request.POST.get('medicamentos'),
            observacoes=request.POST.get('observacoes'),

            responsavel=request.POST.get('responsavel'),
            cpf_responsavel=request.POST.get('cpf_responsavel'),
            telefone_responsavel=request.POST.get(
                'telefone_responsavel'
            )

        )

        print(
            'PACIENTE CRIADO:',
            paciente.id
        )

        return redirect(
            'perfil_paciente',
            id=paciente.id
        )

    convenios = Convenio.objects.filter(
        ativo=True
    ).order_by('nome')

    return render(

        request,

        'accounts/paciente_form.html',

        {
            'convenios': convenios,
            'modo': 'novo'
        }

    )

# =========================================
# EDITAR PACIENTE
# =========================================

@login_required(login_url='/')
def editar_paciente(request, id):

    paciente = get_object_or_404(

        Paciente,

        id=id

    )

    if request.method == 'POST':

        # FOTO
        if request.FILES.get('foto'):

            paciente.foto = request.FILES.get(
                'foto'
            )

        # DADOS PESSOAIS
        paciente.nome = request.POST.get('nome')
        paciente.cpf = request.POST.get('cpf')
        paciente.rg = request.POST.get('rg')

        paciente.nascimento = (
            request.POST.get('nascimento')
            or None
        )

        paciente.genero = request.POST.get(
            'genero'
        )

        paciente.estado_civil = request.POST.get(
            'estado_civil'
        )

        paciente.profissao = request.POST.get(
            'profissao'
        )

        # CONTATO
        paciente.telefone = request.POST.get(
            'telefone'
        )

        paciente.whatsapp = request.POST.get(
            'whatsapp'
        )

        paciente.email = request.POST.get(
            'email'
        )

        # ENDEREÇO
        paciente.cep = request.POST.get('cep')

        paciente.endereco = request.POST.get(
            'endereco'
        )

        paciente.numero = request.POST.get(
            'numero'
        )

        paciente.complemento = request.POST.get(
            'complemento'
        )

        paciente.bairro = request.POST.get(
            'bairro'
        )

        paciente.cidade = request.POST.get(
            'cidade'
        )

        paciente.estado = request.POST.get(
            'estado'
        )

        # CLÍNICO
        paciente.convenio = request.POST.get(
            'convenio'
        )

        paciente.carteirinha = request.POST.get(
            'carteirinha'
        )

        paciente.alergias = request.POST.get(
            'alergias'
        )

        paciente.medicamentos = request.POST.get(
            'medicamentos'
        )

        paciente.observacoes = request.POST.get(
            'observacoes'
        )

        # RESPONSÁVEL
        paciente.responsavel = request.POST.get(
            'responsavel'
        )

        paciente.cpf_responsavel = request.POST.get(
            'cpf_responsavel'
        )

        paciente.telefone_responsavel = request.POST.get(
            'telefone_responsavel'
        )

        paciente.save()

        return redirect('pacientes')

    convenios = Convenio.objects.filter(
        ativo=True
    ).order_by('nome')

    context = {

        'paciente': paciente,
        'convenios': convenios

    }

    return render(

        request,

        'accounts/paciente_form.html',

        {

            'paciente': paciente,
            'convenios': convenios,
            'modo': 'editar'

        }

    )

# =========================================
# EXCLUIR PACIENTE
# =========================================

@login_required(login_url='/')
def excluir_paciente(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    paciente.delete()

    return redirect('pacientes')

# =========================================
# ALTERAR STATUS PACIENTE
# =========================================

@login_required(login_url='/')
def alterar_status_paciente(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    paciente.ativo = not paciente.ativo

    paciente.save()

    messages.success(
        request,
        'Status do paciente atualizado com sucesso.'
    )

    return redirect(
        'pacientes'
    )

# =========================================
# ODONTOGRAMA
# =========================================

@login_required(login_url='/')
@perfil_required(
    'admin',
    'dentista',
    'acd'
)
def odontograma(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    # =========================================
    # SALVAR EVOLUÇÃO
    # =========================================

    if request.method == 'POST':
        print(request.POST)

        procedimento = Procedimento.objects.get(
            id=request.POST.get('procedimento')
        )

        status = request.POST.get('status')

        dente = request.POST.get('dente')

        face = request.POST.get('face')

        descricao = request.POST.get('descricao')

        posicao_icone = request.POST.get(
            'posicao_icone'
        )

        print('POSICAO ESCOLHIDA:', posicao_icone)


        # =====================================
        # GARANTE ORÇAMENTO
        # =====================================

        orcamento, created = Orcamento.objects.get_or_create(
            paciente=paciente
        )

        # =====================================
        # DEFINE VALOR CONFORME CONVÊNIO
        # =====================================

        valor_unitario = procedimento.valor_particular

        if paciente.convenio:

            convenio = Convenio.objects.filter(
                nome=paciente.convenio
            ).first()

            if convenio:

                valor_unitario = (
                    procedimento.valor_particular
                    * (convenio.indice)
                )

        # =====================================
        # CRIA ITEM DO ORÇAMENTO
        # =====================================

        item = ItemOrcamento.objects.create(

            orcamento=orcamento,
            procedimento=procedimento,
            tipo_local='dente',
            dente=dente,
            face=face,
            posicao_icone=posicao_icone,
            valor_unitario=valor_unitario,
            status=status

        )

        
        # =====================================
        # REGISTRA EVOLUÇÃO CLÍNICA
        # =====================================

        EvolucaoClinica.objects.create(

            paciente=paciente,

            dente=dente,

            face=face,

            posicao_icone=posicao_icone,

            procedimento=procedimento,

            status=status,

            descricao=descricao or ''

        )

        return redirect(
            'odontograma',
            id=paciente.id
        )

    # =========================================
    # EVOLUÇÕES CLÍNICAS
    # =========================================

    evolucoes = EvolucaoClinica.objects.filter(
        paciente=paciente
    ).order_by('-criado_em')

    # =========================================
    # ITENS DO ORÇAMENTO
    # =========================================

    itens_orcamento = ItemOrcamento.objects.filter(
        orcamento__paciente=paciente
    )

    # =========================================
    # PROCEDIMENTOS
    # =========================================

    procedimentos = Procedimento.objects.all().order_by(
        'categoria',
        'nome'
    )

    procedimentos_gerais = Procedimento.objects.filter(
        tipo__in=['geral', 'hemiarcada']
    ).order_by(
        'categoria',
        'nome'
    )

    # =========================================
    # CONTEXT
    # =========================================

    context = {

        'paciente': paciente,

        # =========================================
        # DENTES PERMANENTES
        # =========================================

        'superiores': [

            '18','17','16','15','14','13','12','11',
            '21','22','23','24','25','26','27','28'

        ],

        'inferiores': [

            '48','47','46','45','44','43','42','41',
            '31','32','33','34','35','36','37','38'

        ],

        # =========================================
        # DENTES DECÍDUOS
        # =========================================

        'dec_superiores': [

            '55','54','53','52','51',
            '61','62','63','64','65'

        ],

        'dec_inferiores': [

            '85','84','83','82','81',
            '71','72','73','74','75'

        ],

        # =========================================
        # EVOLUÇÕES
        # =========================================

        'evolucoes': evolucoes,

        # =========================================
        # ITENS ORÇAMENTO
        # =========================================

        'itens_orcamento': itens_orcamento,

       # PROCEDIMENTOS

        'procedimentos': procedimentos,

        # PROCEDIMENTOS GERAIS

        'procedimentos_gerais': procedimentos_gerais,
        }
    
    for item in itens_orcamento:
        print(
            f'ITEM {item.id} | DENTE={item.dente} | POSICAO={item.posicao_icone}'
        )

    return render(

        request,

        'accounts/odontograma.html',

        context

    )

# =========================================
# PROCEDIMENTO GERAL
# =========================================

@login_required(login_url='/')
@perfil_required(
    'admin',
    'dentista',
    'acd'
)
def salvar_procedimento_geral(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    if request.method == 'POST':

        procedimento = get_object_or_404(
            Procedimento,
            id=request.POST.get('procedimento')
        )

        status = request.POST.get(
            'status'
        )

        descricao = request.POST.get(
            'descricao'
        )

        posicao_icone = request.POST.get(
            'posicao_icone'
        )

        # GARANTE ORÇAMENTO

        orcamento, created = Orcamento.objects.get_or_create(
            paciente=paciente
        )

        # =====================================
        # CALCULA VALOR CONFORME CONVÊNIO
        # =====================================

        valor_unitario = procedimento.valor_particular

        if paciente.convenio:

            convenio = Convenio.objects.filter(
                nome=paciente.convenio
            ).first()

            if convenio:

                valor_unitario = (
                    procedimento.valor_particular
                    * convenio.indice
                )

        # =====================================
        # CRIA ITEM NO ORÇAMENTO
        # =====================================

        ItemOrcamento.objects.create(

            orcamento=orcamento,

            procedimento=procedimento,

            tipo_local='geral',

            valor_unitario=valor_unitario,

            quantidade=1,

            status=status or 'planejado'

        )

        # CRIA EVOLUÇÃO

        EvolucaoClinica.objects.create(

            paciente=paciente,

            procedimento=procedimento,

            descricao=descricao

        )

    return redirect(
        'odontograma',
        id=paciente.id
    )

@login_required(login_url='/')
@perfil_required(
    'admin',
    'dentista',
    'acd',
    'secretaria'
)
def anamnese(request, id):

    paciente = Paciente.objects.get(id=id)

    anamnese, created = Anamnese.objects.get_or_create(
        paciente=paciente
    )

    if request.method == 'POST':

        # =========================================
        # QUEIXA PRINCIPAL
        # =========================================

        anamnese.queixa_principal = request.POST.get(
            'queixa_principal', ''
        )

        # =========================================
        # HISTÓRIA MÉDICA
        # =========================================

        anamnese.hipertenso = 'hipertenso' in request.POST
        anamnese.diabetico = 'diabetico' in request.POST
        anamnese.cardiopatia = 'cardiopatia' in request.POST
        anamnese.asma = 'asma' in request.POST
        anamnese.bronquite = 'bronquite' in request.POST
        anamnese.anemia = 'anemia' in request.POST
        anamnese.hepatite = 'hepatite' in request.POST

        anamnese.rinite = 'rinite' in request.POST
        anamnese.sinusite = 'sinusite' in request.POST

        anamnese.problema_renal = (
            'problema_renal' in request.POST
        )

        anamnese.sangramento_excessivo = (
            'sangramento_excessivo' in request.POST
        )

        anamnese.alergico = 'alergico' in request.POST

        anamnese.alergias = request.POST.get(
            'alergias', ''
        )

        anamnese.fumante = 'fumante' in request.POST
        anamnese.gravida = 'gravida' in request.POST

        anamnese.historico_medico = request.POST.get(
            'historico_medico', ''
        )

        # NOVOS CAMPOS

        if hasattr(anamnese, 'anticoagulante'):
            anamnese.anticoagulante = (
                'anticoagulante' in request.POST
            )

        if hasattr(anamnese, 'bisfosfonato'):
            anamnese.bisfosfonato = (
                'bisfosfonato' in request.POST
            )

        if hasattr(anamnese, 'marcapasso'):
            anamnese.marcapasso = (
                'marcapasso' in request.POST
            )

        if hasattr(anamnese, 'cancer'):
            anamnese.cancer = (
                'cancer' in request.POST
            )

        if hasattr(anamnese, 'hipotireoidismo'):
            anamnese.hipotireoidismo = (
                'hipotireoidismo' in request.POST
            )

        if hasattr(anamnese, 'hipertireoidismo'):
            anamnese.hipertireoidismo = (
                'hipertireoidismo' in request.POST
            )

        # =========================================
        # MEDICAMENTOS
        # =========================================

        anamnese.usa_medicamento = (
            'usa_medicamento' in request.POST
        )

        anamnese.medicamentos = request.POST.get(
            'medicamentos', ''
        )

        anamnese.antibioticos = request.POST.get(
            'antibioticos', ''
        )

        anamnese.antiinflamatorios = request.POST.get(
            'antiinflamatorios', ''
        )

        anamnese.analgesicos = request.POST.get(
            'analgesicos', ''
        )

        # =========================================
        # CIRURGIAS
        # =========================================

        anamnese.cirurgia = (
            'cirurgia' in request.POST
        )

        anamnese.cirurgias = request.POST.get(
            'cirurgias', ''
        )

        anamnese.hospitalizado = (
            'hospitalizado' in request.POST
        )

        anamnese.hospitalizacao = request.POST.get(
            'hospitalizacao', ''
        )

        anamnese.transfusao_sangue = (
            'transfusao_sangue' in request.POST
        )

        # =========================================
        # HISTÓRIA ODONTOLÓGICA
        # =========================================

        anamnese.primeira_consulta = (
            'primeira_consulta' in request.POST
        )

        anamnese.experiencia_odontologica = request.POST.get(
            'experiencia_odontologica', ''
        )

        anamnese.abandono_tratamento = (
            'abandono_tratamento' in request.POST
        )

        anamnese.medo_dentista = (
            'medo_dentista' in request.POST
        )

        anamnese.anestesia_reacao = request.POST.get(
            'anestesia_reacao', ''
        )

        anamnese.sangramento_gengival = (
            'sangramento_gengival' in request.POST
        )

        anamnese.sensibilidade = (
            'sensibilidade' in request.POST
        )

        anamnese.dor_mastigar = (
            'dor_mastigar' in request.POST
        )

        # =========================================
        # HIGIENE ORAL
        # =========================================

        anamnese.frequencia_escovacao = request.POST.get(
            'frequencia_escovacao', ''
        )

        anamnese.usa_fio_dental = (
            'usa_fio_dental' in request.POST
        )

        anamnese.usa_enxaguante = (
            'usa_enxaguante' in request.POST
        )

        anamnese.escova_lingua = (
            'escova_lingua' in request.POST
        )

        # =========================================
        # HÁBITOS
        # =========================================

        anamnese.bruxismo = 'bruxismo' in request.POST
        anamnese.ronco = 'ronco' in request.POST

        anamnese.respiracao_bucal = (
            'respiracao_bucal' in request.POST
        )

        anamnese.roer_unhas = (
            'roer_unhas' in request.POST
        )

        anamnese.morde_objetos = (
            'morde_objetos' in request.POST
        )

        anamnese.chupeta = 'chupeta' in request.POST

        anamnese.succao_dedo = (
            'succao_dedo' in request.POST
        )

        anamnese.baba_travesseiro = (
            'baba_travesseiro' in request.POST
        )

        anamnese.dorme_boca_aberta = (
            'dorme_boca_aberta' in request.POST
        )

        anamnese.morde_labios = (
            'morde_labios' in request.POST
        )

        # =========================================
        # HÁBITOS ALIMENTARES
        # =========================================

        anamnese.belisca_refeicoes = (
            'belisca_refeicoes' in request.POST
        )

        anamnese.alimentacao_cariogenica = (
            'alimentacao_cariogenica' in request.POST
        )

        anamnese.tipo_alimentacao = request.POST.get(
            'tipo_alimentacao', ''
        )

        # =========================================
        # PERFIL COMPORTAMENTAL
        # =========================================

        anamnese.ansioso = 'ansioso' in request.POST
        anamnese.agitado = 'agitado' in request.POST
        anamnese.calmo = 'calmo' in request.POST

        anamnese.comunicativo = (
            'comunicativo' in request.POST
        )

        anamnese.retraido = (
            'retraido' in request.POST
        )

        anamnese.introvertido = (
            'introvertido' in request.POST
        )

        anamnese.extrovertido = (
            'extrovertido' in request.POST
        )

        # =========================================
        # OBSERVAÇÕES
        # =========================================

        anamnese.observacoes = request.POST.get(
            'observacoes', ''
        )

        anamnese.save()

    context = {

        'paciente': paciente,
        'anamnese': anamnese

    }

    return render(

        request,
        'accounts/anamnese.html',
        context

    )

@login_required(login_url='/')
@perfil_required(
    'admin',
    'dentista'
)
def ficha_clinica(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    evolucoes = EvolucaoClinica.objects.filter(
        paciente=paciente
    ).order_by('-criado_em')

    prontuarios = ProntuarioClinico.objects.filter(
        paciente=paciente
    )

    documentos = DocumentoClinico.objects.filter(
        paciente=paciente
    )

    anexos = AnexoPaciente.objects.filter(
        paciente=paciente
    )

    receitas = Receita.objects.filter(
        paciente=paciente
    )

    exames = Exame.objects.filter(
        paciente=paciente
    )

    solicitacoes = SolicitacaoExame.objects.filter(
        paciente=paciente
    )

    # =========================================
    # RESUMO CLÍNICO
    # =========================================

    total_procedimentos = evolucoes.count()

    realizados = evolucoes.filter(
        status='realizado'
    ).count()

    planejados = evolucoes.filter(
        status='planejado'
    ).count()

    andamento = evolucoes.filter(
        status='andamento'
    ).count()

    ultima_evolucao = evolucoes.first()

    # =========================================
    # NOVO REGISTRO CLÍNICO
    # =========================================

    if request.method == 'POST':

        ProntuarioClinico.objects.create(

            paciente=paciente,

            titulo=request.POST.get(
                'titulo'
            ),

            anotacao=request.POST.get(
                'anotacao'
            )

        )

        return redirect(
            'ficha_clinica',
            id=paciente.id
        )

    context = {

        'paciente': paciente,

        'evolucoes': evolucoes,

        'prontuarios': prontuarios,

        'anexos': anexos,

        'documentos': documentos,

        'receitas': receitas,

        'exames': exames,

        'solicitacoes': solicitacoes,

        'total_procedimentos': total_procedimentos,

        'realizados': realizados,

        'planejados': planejados,

        'andamento': andamento,

        'ultima_evolucao': ultima_evolucao

    }

    return render(

        request,

        'accounts/ficha_clinica.html',

        context

    )

# =========================================
# UPLOAD ANEXO
# =========================================

@login_required(login_url='/')
@perfil_required(
    'admin',
    'dentista'
)
def upload_anexo(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    if request.method == 'POST':

        arquivo = request.FILES.get(
            'arquivo'
        )

        descricao = request.POST.get(
            'descricao'
        )

        if arquivo:

            AnexoPaciente.objects.create(

                paciente=paciente,

                descricao=descricao,

                arquivo=arquivo

            )

    return redirect(
        'ficha_clinica',
        id=paciente.id
    )

# =========================================
# PROCEDIMENTOS
# =========================================

@login_required(login_url='/')
@perfil_required(
    'admin'
)
def procedimentos(request):

    procedimentos = Procedimento.objects.all().order_by(
        'ordem',
        'nome'
    )

    # =========================================
    # ÍCONES DISPONÍVEIS
    # =========================================

    mini_path = os.path.join(

        settings.BASE_DIR,
        'static',
        'img',
        'procedimentos',
        'mini'

    )

    full_path = os.path.join(

        settings.BASE_DIR,
        'static',
        'img',
        'procedimentos',
        'full'

    )

    mini_icons = []
    full_icons = []

    # MINI

    if os.path.exists(mini_path):

        mini_icons = [

            arquivo

            for arquivo in os.listdir(mini_path)

            if arquivo.lower().endswith((

                '.png',
                '.svg',
                '.webp',
                '.jpg',
                '.jpeg'

            ))

        ]

    # FULL

    if os.path.exists(full_path):

        full_icons = [

            arquivo

            for arquivo in os.listdir(full_path)

            if arquivo.lower().endswith((

                '.png',
                '.svg',
                '.webp',
                '.jpg',
                '.jpeg'

            ))

        ]

    # REMOVE DUPLICADOS

    icones = sorted(

        list(

            set(
                mini_icons + full_icons
            )

        )

    )

    print(icones)

    # =========================================
    # FORMULÁRIO
    # =========================================

    form = ProcedimentoForm()

    # =========================================
    # SALVAR
    # =========================================

    if request.method == 'POST':

        form = ProcedimentoForm(request.POST)

        if form.is_valid():

            procedimento = form.save(commit=False)

            # VALOR CONVÊNIO AUTOMÁTICO

            if not procedimento.valor_convenio:

                procedimento.valor_convenio = 0

            procedimento.save()

            return redirect('procedimentos')

        else:

            print(form.errors)

    context = {

        'form': form,
        'procedimentos': procedimentos,
        'icones': icones

    }

    return render(

        request,

        'accounts/procedimentos.html',

        context

    )

# =========================================
# EDITAR PROCEDIMENTO
# =========================================

@login_required(login_url='/')
def editar_procedimento(request, id):

    procedimento = get_object_or_404(

        Procedimento,

        id=id

    )

    procedimentos = Procedimento.objects.all().order_by(
        'ordem',
        'nome'
    )

    pasta_icones = os.path.join(

        settings.BASE_DIR,
        'static',
        'img',
        'procedimentos',
        'mini'

    )
    # =========================================
    # ÍCONES DOS PROCEDIMENTOS
    # =========================================

    mini_path = os.path.join(

        settings.BASE_DIR,
        'static',
        'img',
        'procedimentos',
        'mini'

    )

    full_path = os.path.join(

        settings.BASE_DIR,
        'static',
        'img',
        'procedimentos',
        'full'

    )

    mini_icons = []
    full_icons = []

    # MINI
    if os.path.exists(mini_path):

        mini_icons = os.listdir(mini_path)

    # FULL
    if os.path.exists(full_path):

        full_icons = os.listdir(full_path)

    # REMOVE DUPLICADOS
    icones = sorted(

        list(

            set(
                mini_icons + full_icons
            )

        )

    )

    

    if request.method == 'POST':

        form = ProcedimentoForm(

            request.POST,

            instance=procedimento

        )

        if form.is_valid():

            form.save()

            return redirect('procedimentos')

    else:

        form = ProcedimentoForm(
            instance=procedimento
        )

    context = {

        'form': form,
        'procedimentos': procedimentos,
        'icones': icones,
        'editando': True

    }

    return render(

        request,

        'accounts/procedimentos.html',

        context

    )


# =========================================
# EXCLUIR PROCEDIMENTO
# =========================================

@login_required(login_url='/')
def excluir_procedimento(request, id):

    procedimento = get_object_or_404(

        Procedimento,

        id=id

    )

    procedimento.delete()

    return redirect('procedimentos')


# =========================================
# ORÇAMENTO
# =========================================

@login_required(login_url='/')
def orcamento(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    # =========================================
    # CRIA ORÇAMENTO
    # =========================================

    orcamento, created = Orcamento.objects.get_or_create(
        paciente=paciente
    )

    # =========================================
    # ADICIONAR ITEM
    # =========================================

    if request.method == 'POST':

        item_form = ItemOrcamentoForm(request.POST)

        if item_form.is_valid():

            item = item_form.save(commit=False)

            # ORÇAMENTO

            item.orcamento = orcamento

            # DENTE

            item.dente = request.POST.get('dente')

            # FACE

            item.face = request.POST.get('face')

            # STATUS

            item.status = 'planejado'

            # VALOR

            item.valor_unitario = item.procedimento.valor_particular

            # SALVAR

            item.save()

            return redirect(
                'orcamento',
                id=paciente.id
            )
    else:

        item_form = ItemOrcamentoForm()

    # =========================================
    # CONTEXT
    # =========================================

    context = {

        'paciente': paciente,
        'orcamento': orcamento,
        'item_form': item_form,

    }

    return render(
        request,
        'accounts/orcamento.html',
        context
    )


# =========================================
# CONVÊNIOS
# =========================================

@login_required(login_url='/')
def convenios(request):

    convenios = Convenio.objects.all().order_by('nome')

    form = ConvenioForm()

    if request.method == 'POST':

        form = ConvenioForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('convenios')

    context = {

        'form': form,
        'convenios': convenios

    }

    return render(

        request,
        'accounts/convenios.html',
        context

    )

# =========================================
# EDITAR CONVÊNIO
# =========================================

@login_required(login_url='/')
def editar_convenio(request, id):

    convenio = get_object_or_404(
        Convenio,
        id=id
    )

    if request.method == 'POST':

        form = ConvenioForm(
            request.POST,
            instance=convenio
        )

        if form.is_valid():

            form.save()

            return redirect('convenios')

    else:

        form = ConvenioForm(
            instance=convenio
        )

    convenios = Convenio.objects.all()

    return render(

        request,

        'accounts/convenios.html',

        {

            'form': form,
            'convenios': convenios

        }

    )


# =========================================
# EXCLUIR CONVÊNIO
# =========================================

@login_required(login_url='/')
def excluir_convenio(request, id):

    convenio = get_object_or_404(
        Convenio,
        id=id
    )

    convenio.delete()

    return redirect('convenios')

# =========================================
# EXCLUIR ITEM ORÇAMENTO
# =========================================

@login_required(login_url='/')
def excluir_item_orcamento(request, id):

    item = get_object_or_404(
        ItemOrcamento,
        id=id
    )

    paciente = item.orcamento.paciente

    # REMOVE DA TIMELINE

    EvolucaoClinica.objects.filter(

        paciente=paciente,

        procedimento=item.procedimento,

        dente=item.dente

    ).delete()

    # REMOVE DO ORÇAMENTO

    item.delete()

    return redirect(
        'orcamento',
        id=paciente.id
    )

# =========================================
# EDITAR ITEM ORÇAMENTO
# =========================================

@login_required(login_url='/')
def editar_item_orcamento(request, id):

    item = get_object_or_404(
        ItemOrcamento,
        id=id
    )

    if request.method == 'POST':

        item.procedimento_id = request.POST.get(
            'procedimento'
        )

        item.dente = request.POST.get(
            'dente'
        )

        item.face = request.POST.get(
            'face'
        )

        status = request.POST.get(
            'status',
            'planejado'
        )
        item.quantidade = request.POST.get(
            'quantidade'
        )

        procedimento = Procedimento.objects.get(
            id=item.procedimento_id
        )

        item.valor_unitario = procedimento.valor_particular

        item.save()

        return redirect(
            'orcamento',
            id=item.orcamento.paciente.id
        )

    procedimentos = Procedimento.objects.all()

    context = {

        'item': item,
        'procedimentos': procedimentos,

    }

    return render(

        request,

        'accounts/editar_item_orcamento.html',

        context

    )

# =========================================
# PDF ORÇAMENTO
# =========================================

@login_required(login_url='/')
def gerar_pdf_orcamento(request, id):

    orcamento = get_object_or_404(
        Orcamento,
        id=id
    )

    paciente = orcamento.paciente

    validade = (
        orcamento.criado_em.date()
        + timedelta(days=30)
    )

    config = ConfiguracaoClinica.objects.first()

    itens = orcamento.itens.all()

    evolucoes = EvolucaoClinica.objects.filter(
        paciente=paciente
    )

    # =========================================
    # ARCADAS PERMANENTES
    # =========================================

    superiores_permanentes = [
        '18','17','16','15','14','13','12','11',
        '21','22','23','24','25','26','27','28'
    ]

    inferiores_permanentes = [
        '48','47','46','45','44','43','42','41',
        '31','32','33','34','35','36','37','38'
    ]

    # =========================================
    # ARCADAS DECÍDUAS
    # =========================================

    superiores_deciduos = [
        '55','54','53','52','51',
        '61','62','63','64','65'
    ]

    inferiores_deciduos = [
        '85','84','83','82','81',
        '71','72','73','74','75'
    ]

    # =========================================
    # VERIFICA SE EXISTE DENTIÇÃO
    # =========================================

    PERMANENTES = (
        superiores_permanentes +
        inferiores_permanentes
    )

    DECIDUOS = (
        superiores_deciduos +
        inferiores_deciduos
    )

    tem_permanente = evolucoes.filter(
        dente__in=PERMANENTES
    ).exists()

    tem_deciduo = evolucoes.filter(
        dente__in=DECIDUOS
    ).exists()

    # =========================================
    # DENTES COM PROCEDIMENTO
    # =========================================

    dentes_com_procedimento = []

    for evolucao in evolucoes:

        if evolucao.dente:

            dentes_com_procedimento.append(
                str(evolucao.dente)
            )

    dentes_com_procedimento = list(
        set(dentes_com_procedimento)
    )

    # =========================================
    # CONTEXT
    # =========================================

    context = {

        'orcamento': orcamento,
        'paciente': paciente,
        'itens': itens,
        'evolucoes': evolucoes,
        'config': config,
        'validade': validade,
        'tem_permanente': tem_permanente,
        'tem_deciduo': tem_deciduo,

        'superiores_permanentes': superiores_permanentes,
        'inferiores_permanentes': inferiores_permanentes,

        'superiores_deciduos': superiores_deciduos,
        'inferiores_deciduos': inferiores_deciduos,
        'dentes_com_procedimento': dentes_com_procedimento,        
    }

    return render(
        request,
        'accounts/orcamento_pdf.html',
        context
    )

# =========================================
# ALTERAR STATUS PROCEDIMENTO
# =========================================

import json

from django.http import JsonResponse

@login_required(login_url='/')
def alterar_status_procedimento(request, id):

    item = get_object_or_404(

        ItemOrcamento,

        id=id

    )

    data = json.loads(request.body)

    novo_status = data['status']

    # =====================================
    # ATUALIZA STATUS
    # =====================================

    item.status = novo_status

    item.save()

    # =====================================
    # REGISTRA EVOLUÇÃO CLÍNICA
    # =====================================

    EvolucaoClinica.objects.create(

        paciente=item.orcamento.paciente,

        dente=item.dente,

        procedimento=item.procedimento,

        status=novo_status,

        descricao=''

    )
    return JsonResponse({

        'success': True

    })
# =========================================
# RODAPÉ PDF
# =========================================

def adicionar_rodape(canvas, doc):

    canvas.saveState()

    pagina = canvas.getPageNumber()

    canvas.setFont(
        "Helvetica",
        9
    )

    canvas.drawRightString(
        190 * mm,
        10 * mm,
        f"Página {pagina}"
    )

    canvas.restoreState()


# =========================================
# PDF PRONTUÁRIO
# =========================================
@login_required(login_url='/')
def imprimir_prontuario(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    prontuarios = ProntuarioClinico.objects.filter(
        paciente=paciente
    ).order_by('-criado_em')

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = f'inline; filename="prontuario_{paciente.id}.pdf"'

    doc = SimpleDocTemplate(
        response,
        topMargin=30,
        bottomMargin=30,
        leftMargin=40,
        rightMargin=40
    )

    styles = getSampleStyleSheet()

    elementos = []

    # =========================================
    # CONFIGURAÇÃO CLÍNICA
    # =========================================

    config = ConfiguracaoClinica.objects.first()

    # =========================================
    # LOGO
    # =========================================

    logo_path = os.path.join(
        settings.BASE_DIR,
        'static',
        'img',
        'logo.png'
    )

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=240,
            height=90
        )

    logo.hAlign = 'CENTER'

    elementos.append(logo)

    # Pequeno espaço após a logo
    elementos.append(Spacer(1, 8))

    # =========================================
    # NOME DA CLÍNICA
    # =========================================

    estilo_clinica = ParagraphStyle(
        'Clinica',
        parent=styles['Heading2'],
        fontSize=12,
        leading=14,
        alignment=1,  # Centralizado
        spaceAfter=10
    )

    if config and config.nome_clinica:

        elementos.append(
            Paragraph(
                f'''
                <para align="center">
                <b>{config.nome_clinica}</b>
                </para>
                ''',
                estilo_clinica
            )
        )

    # =========================================
    # TÍTULO
    # =========================================

    elementos.append(

        Paragraph(

            '''
            <para align="center">
            <b>PRONTUÁRIO CLÍNICO</b>
            </para>
            ''',

            styles['Title']

        )

    )

    elementos.append(
        Spacer(1, 10)
    )

    elementos.append(

        HRFlowable(
            width="100%",
            thickness=1.2,
            color=colors.HexColor('#1e40af')
        )

    )

    elementos.append(
        Spacer(1, 15)
    )

    # =========================================
    # CABEÇALHO
    # =========================================

    elementos.append(Spacer(1, 15))

    elementos.append(
        Paragraph(
            f'<b>Paciente:</b> {paciente.nome}',
            styles['Normal']
        )
    )

    if paciente.cpf:

        elementos.append(
            Paragraph(
                f'<b>CPF:</b> {paciente.cpf}',
                styles['Normal']
            )
        )

    telefone_paciente = (
        paciente.telefone or 'Não informado'
    )

    whatsapp_paciente = (
        paciente.whatsapp or 'Não informado'
    )

    email_paciente = (
        paciente.email or 'Não informado'
    )

    elementos.append(
        Paragraph(
            f'<b>Telefone:</b> {telefone_paciente}',
            styles['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f'<b>WhatsApp:</b> {whatsapp_paciente}',
            styles['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f'<b>E-mail:</b> {email_paciente}',
            styles['Normal']
        )
    )

    agora = timezone.localtime()

    elementos.append(
        Paragraph(
            f'<b>Data de emissão:</b> {agora.strftime("%d/%m/%Y %H:%M")}',
            styles['Normal']
        )
    )

    elementos.append(Spacer(1, 15))

    elementos.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.grey
        )
    )

    elementos.append(Spacer(1, 15))

    # =========================================
    # DADOS DA CLÍNICA
    # =========================================

    nome_clinica = (
        config.nome_clinica
        if config and config.nome_clinica
        else ''
    )

    telefone_clinica = (
        config.telefone
        if config and config.telefone
        else ''
    )

    whatsapp_clinica = (
        config.whatsapp
        if config and config.whatsapp
        else ''
    )

    email_clinica = (
        config.email
        if config and config.email
        else ''
    )

    # =========================================
    # REGISTROS
    # =========================================

    for item in prontuarios:

        elementos.append(
            Paragraph(
                f'<b>{item.titulo}</b>',
                styles['Heading2']
            )
        ) 

        data_local = timezone.localtime(
            item.criado_em
        )

        elementos.append(
            Paragraph(
                data_local.strftime(
                    '%d/%m/%Y %H:%M'
                ),
                styles['Italic']
            )
        )

        elementos.append(Spacer(1, 5))

        elementos.append(
            Paragraph(
                item.anotacao,
                styles['BodyText']
            )
        )

        elementos.append(Spacer(1, 10))

        elementos.append(
            HRFlowable(
                width="100%",
                thickness=0.5,
                color=colors.lightgrey
            )
        )

        elementos.append(Spacer(1, 10))
    # =========================================
    # ASSINATURA
    # =========================================

    elementos.append(Spacer(1, 15))

    elementos.append(
        Paragraph(
            '''
            <para align="center">
            _______________________________________
            <br/>
            Cirurgião-Dentista Responsável
            </para>
            ''',
            styles['Normal']
        )
    )

    # =========================================
    # RODAPÉ
    # =========================================

    elementos.append(Spacer(1, 20))

    elementos.append(
        HRFlowable(
            width="100%",
            thickness=0.8,
            color=colors.grey
        )
    )

    elementos.append(Spacer(1, 8))

    elementos.append(
        Paragraph(
            f'''
            <para align="center">
            <b>{nome_clinica}</b>
            </para>
            ''',
            styles['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f'''
            <para align="center">
            Tel: {telefone_clinica}
            &nbsp;&nbsp;&nbsp;
            WhatsApp: {whatsapp_clinica}
            </para>
            ''',
            styles['BodyText']
        )
    )

    elementos.append(
        Paragraph(
            f'''
            <para align="center">
            {email_clinica}
            </para>
            ''',
            styles['BodyText']
        )
    )

    # =========================================
    # GERAR PDF
    # =========================================

    doc.build(
        elementos,
        onFirstPage=adicionar_rodape,
        onLaterPages=adicionar_rodape
    )

    return response
# =========================================

@login_required(login_url='/')
def novo_documento(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    if request.method == 'POST':

        template_id = request.POST.get(
            'template'
        )

        conteudo = request.POST.get(
            'conteudo',
            ''
        )

        titulo = request.POST.get(
            'titulo',
            ''
        )

        tipo_documento = request.POST.get(
            'tipo',
            'personalizado'
        )

        # =========================================
        # TEMPLATE SELECIONADO
        # =========================================

        if template_id:

            template = get_object_or_404(
                TemplateDocumento,
                id=template_id
            )

            # usa o tipo do template
            tipo_documento = template.tipo

            # usa o conteúdo do template
            conteudo = template.conteudo

            conteudo = conteudo.replace(
                '{{ paciente_nome }}',
                paciente.nome or ''
            )

            conteudo = conteudo.replace(
                '{{ paciente_cpf }}',
                paciente.cpf or ''
            )

            conteudo = conteudo.replace(
                '{{ data_atual }}',
                timezone.now().strftime(
                    '%d/%m/%Y'
                )
            )

            conteudo = conteudo.replace(
                '{{ data_atendimento }}',
                timezone.now().strftime(
                    '%d/%m/%Y'
                )
            )

            if paciente.nascimento:

                conteudo = conteudo.replace(
                    '{{ paciente_nascimento }}',
                    paciente.nascimento.strftime(
                        '%d/%m/%Y'
                    )
                )

            else:

                conteudo = conteudo.replace(
                    '{{ paciente_nascimento }}',
                    ''
                )

            config = ConfiguracaoClinica.objects.first()

            conteudo = conteudo.replace(
                '{{ cro_clinica }}',
                config.cro if config and config.cro else ''
            )

            # se não informar título,
            # usa o nome do template
            if not titulo:
                titulo = template.nome

        documento = DocumentoClinico.objects.create(

            paciente=paciente,

            titulo=titulo,

            tipo=tipo_documento,

            conteudo=conteudo,

            status='rascunho'

        )

        return redirect(
            'editar_documento',
            documento.id
        )

    templates = TemplateDocumento.objects.filter(
        ativo=True
    ).order_by('nome')

    return render(

        request,

        'accounts/documento_form.html',

        {

            'paciente': paciente,

            'templates': templates

        }

    )

# ========================================

@login_required(login_url='/')
def editar_documento(request, id):

    documento = get_object_or_404(

        DocumentoClinico,

        id=id

    )

    if request.method == 'POST':

        documento.titulo = request.POST.get(
            'titulo'
        )

        documento.conteudo = request.POST.get(
            'conteudo'
        )

        documento.save()

        return redirect(

            'editar_documento',

            documento.id

        )

    return render(

        request,

        'accounts/documento_form.html',

        {

            'documento': documento,

            'paciente': documento.paciente

        }

    )

# =========================================
# EXCLUIR DOCUMENTO
# =========================================

@login_required(login_url='/')
def excluir_documento(request, id):

    documento = get_object_or_404(
        DocumentoClinico,
        id=id
    )

    paciente_id = documento.paciente.id

    documento.delete()

    return redirect(
        'ficha_clinica',
        paciente_id
    ) 

@login_required(login_url='/')
def imprimir_documento(request, id):

    documento = get_object_or_404(
        DocumentoClinico,
        id=id
    )

    paciente = documento.paciente

    config = ConfiguracaoClinica.objects.first()

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = f'inline; filename="documento_{documento.id}.pdf"'

    doc = SimpleDocTemplate(
        response,
        topMargin=30,
        bottomMargin=30,
        leftMargin=40,
        rightMargin=40
    )

    styles = getSampleStyleSheet()

    elementos = []

   # =========================================
    # LOGO
    # =========================================

    logo_path = os.path.join(
        settings.BASE_DIR,
        'static',
        'img',
        'logo.png'
    )

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=240,
            height=90
        )

        logo.hAlign = 'CENTER'

        elementos.append(logo)

        elementos.append(
            Spacer(1, 8)
        )

    # =========================================
    # NOME DA CLÍNICA
    # =========================================

    if config and config.nome_clinica:

        elementos.append(
            Paragraph(
                f'''
                <para align="center">
                <b>{config.nome_clinica}</b>
                </para>
                ''',
                styles['Heading2']
            )
        )

    # =========================================
    # TÍTULO
    # =========================================

    elementos.append(
        Paragraph(
            f'''
            <para align="center">
            <b>{documento.titulo.upper()}</b>
            </para>
            ''',
            styles['Title']
        )
    )

    elementos.append(Spacer(1, 10))

    elementos.append(
        HRFlowable(
            width="100%",
            thickness=1.2,
            color=colors.HexColor('#1e40af')
        )
    )

    elementos.append(Spacer(1, 15))

    # =========================================
    # PACIENTE
    # =========================================

    elementos.append(
        Paragraph(
            f'<b>Paciente:</b> {paciente.nome}',
            styles['Normal']
        )
    )

    if paciente.cpf:

        elementos.append(
            Paragraph(
                f'<b>CPF:</b> {paciente.cpf}',
                styles['Normal']
            )
        )

    elementos.append(Spacer(1, 15))

    # =========================================
    # CONTEÚDO
    # =========================================

    from reportlab.lib.styles import ParagraphStyle

    estilo_conteudo = ParagraphStyle(
        'ConteudoDocumento',
        parent=styles['BodyText'],
        fontSize=11,
        leading=20,
        alignment=4,  # Justificado
        spaceBefore=0,
        spaceAfter=12,
    )

    conteudo = documento.conteudo.replace(
        '\n',
        '<br/>'
    )

    elementos.append(
        Paragraph(
            conteudo,
            estilo_conteudo
        )
    )

    # =========================================
    # ASSINATURA
    # =========================================

    elementos.append(
        Spacer(1, 35)
    )

    elementos.append(
        Paragraph(
            '''
            <para align="center">
            ____________________________________
            <br/>
            Assinatura e Carimbo
            </para>
            ''',
            styles['Normal']
        )
    )
    # =========================================
    # DADOS DA CLÍNICA
    # =========================================

    nome_clinica = (
        config.nome_clinica
        if config and config.nome_clinica
        else ''
    )

    telefone_clinica = (
        config.telefone
        if config and config.telefone
        else ''
    )

    whatsapp_clinica = (
        config.whatsapp
        if config and config.whatsapp
        else ''
    )

    email_clinica = (
        config.email
        if config and config.email
        else ''
    )

    # =========================================
    # RODAPÉ
    # =========================================

    elementos.append(
        Spacer(1, 20)
    )

    elementos.append(
        HRFlowable(
            width="100%",
            thickness=0.8,
            color=colors.grey
        )
    )

    elementos.append(
        Spacer(1, 8)
    )

    if nome_clinica:

        elementos.append(
            Paragraph(
                f'''
                <para align="center">
                <b>{nome_clinica}</b>
                </para>
                ''',
                styles['Normal']
            )
        )

    if telefone_clinica or whatsapp_clinica:

        elementos.append(
            Paragraph(
                f'''
                <para align="center">
                Tel: {telefone_clinica}
                &nbsp;&nbsp;&nbsp;
                WhatsApp: {whatsapp_clinica}
                </para>
                ''',
                styles['BodyText']
            )
        )

    if email_clinica:

        elementos.append(
            Paragraph(
                f'''
                <para align="center">
                {email_clinica}
                </para>
                ''',
                styles['BodyText']
            )
        )

    doc.build(elementos)

    return response

# =========================================
# VISUALIZAR DOCUMENTO
# =========================================

@login_required(login_url='/')
def visualizar_documento(request, id):

    documento = get_object_or_404(
        DocumentoClinico,
        id=id
    )

    config = ConfiguracaoClinica.objects.first()

    return render(

        request,

        'accounts/visualizar_documento.html',

        {

            'documento': documento,
            'config': config

        }

    ) 

# =========================================
# CONFIGURAÇÃO DA CLÍNICA
# =========================================

@login_required(login_url='/')
def configuracao_clinica(request):

    config, created = (
        ConfiguracaoClinica.objects.get_or_create(
            id=1
        )
    )

    if request.method == 'POST':

        config.nome_clinica = request.POST.get(
            'nome_clinica'
        )

        config.cro = request.POST.get(
            'cro'
        )

        config.cnpj = request.POST.get(
            'cnpj'
        )

        config.telefone = request.POST.get(
            'telefone'
        )

        config.whatsapp = request.POST.get(
            'whatsapp'
        )

        config.email = request.POST.get(
            'email'
        )

        config.endereco = request.POST.get(
            'endereco'
        )

        config.numero = request.POST.get(
            'numero'
        )

        config.bairro = request.POST.get(
            'bairro'
        )

        config.cidade = request.POST.get(
            'cidade'
        )

        config.estado = request.POST.get(
            'estado'
        )

        config.cep = request.POST.get(
            'cep'
        )

        config.observacoes_orcamento = (
            request.POST.get(
                'observacoes_orcamento'
            )
        )

        if request.FILES.get('logo'):

            config.logo = request.FILES.get(
                'logo'
            )

        config.save()

        return redirect(
            'configuracao_clinica'
        )

    return render(

        request,

        'accounts/configuracao_clinica.html',

        {
            'config': config
        }

    ) 

# =========================================
# PDF ANAMNESE
# =========================================

@login_required(login_url='/')
def imprimir_anamnese(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    anamnese = get_object_or_404(
        Anamnese,
        paciente=paciente
    )

    resumo_clinico = gerar_resumo_clinico(
        anamnese
    )

    print(resumo_clinico)

    config = ConfiguracaoClinica.objects.first()    

    context = {

        'paciente': paciente,
        'anamnese': anamnese,
        'config': config,
        'resumo_clinico': resumo_clinico
    }

    return render(

        request,

        'accounts/anamnese_pdf.html',

        context

    ) 

# =========================================
# RESUMO CLÍNICO AUTOMÁTICO
# =========================================

def gerar_resumo_clinico(anamnese):

    resumo = []

    # =========================================
    # CONDIÇÕES SISTÊMICAS
    # =========================================

    if anamnese.hipertenso:
        resumo.append('Hipertenso')

    if anamnese.diabetico:
        resumo.append('Diabético')

    if anamnese.cardiopatia:
        resumo.append('Cardiopata')

    if anamnese.asma:
        resumo.append('Asma')

    if anamnese.bronquite:
        resumo.append('Bronquite')

    if anamnese.anemia:
        resumo.append('Anemia')

    if anamnese.hepatite:
        resumo.append('Hepatite')

    if anamnese.rinite:
        resumo.append('Rinite')

    if anamnese.sinusite:
        resumo.append('Sinusite')

    if anamnese.problema_renal:
        resumo.append('Problema renal')

    if anamnese.sangramento_excessivo:
        resumo.append('Sangramento excessivo')

    if hasattr(anamnese, 'anticoagulante') and anamnese.anticoagulante:
        resumo.append('Uso de anticoagulantes')

    if hasattr(anamnese, 'bisfosfonato') and anamnese.bisfosfonato:
        resumo.append('Uso de bisfosfonatos')

    if hasattr(anamnese, 'marcapasso') and anamnese.marcapasso:
        resumo.append('Portador de marcapasso')

    if hasattr(anamnese, 'cancer') and anamnese.cancer:
        resumo.append('Histórico de câncer')

    if hasattr(anamnese, 'hipotireoidismo') and anamnese.hipotireoidismo:
        resumo.append('Hipotireoidismo')

    if hasattr(anamnese, 'hipertireoidismo') and anamnese.hipertireoidismo:
        resumo.append('Hipertireoidismo')

    # =========================================
    # ALERGIAS E MEDICAMENTOS
    # =========================================

    if anamnese.alergias:
        resumo.append(
            f'Alergias: {anamnese.alergias}'
        )

    if anamnese.medicamentos:
        resumo.append(
            f'Medicamentos: {anamnese.medicamentos}'
        )

    # =========================================
    # CIRURGIAS
    # =========================================

    if anamnese.cirurgia:

        if anamnese.cirurgias:

            resumo.append(
                f'Cirurgias prévias: {anamnese.cirurgias}'
            )

        else:

            resumo.append(
                'Histórico cirúrgico positivo'
            )

    if anamnese.hospitalizado:

        if anamnese.hospitalizacao:

            resumo.append(
                f'Hospitalização: {anamnese.hospitalizacao}'
            )

        else:

            resumo.append(
                'Hospitalização prévia'
            )

    if anamnese.transfusao_sangue:
        resumo.append(
            'Histórico de transfusão sanguínea'
        )

    # =========================================
    # HISTÓRIA ODONTOLÓGICA
    # =========================================

    if anamnese.bruxismo:
        resumo.append('Bruxismo')

    if anamnese.sensibilidade:
        resumo.append('Sensibilidade dentária')

    if anamnese.sangramento_gengival:
        resumo.append('Sangramento gengival')

    if anamnese.dor_mastigar:
        resumo.append('Dor à mastigação')

    if anamnese.medo_dentista:
        resumo.append('Ansiedade odontológica')

    if anamnese.abandono_tratamento:
        resumo.append('Histórico de abandono de tratamento')

    # =========================================
    # HÁBITOS
    # =========================================

    if anamnese.fumante:
        resumo.append('Fumante')

    if anamnese.ronco:
        resumo.append('Ronco')

    if anamnese.respiracao_bucal:
        resumo.append('Respiração bucal')

    # =========================================
    # RESULTADO
    # =========================================

    if not resumo:

        return (
            'Nenhuma condição clínica relevante informada.'
        )

    return ' • '.join(resumo)

# =========================================
# MEDICAMENTOS
# =========================================

@login_required(login_url='/')
def medicamentos(request):

    medicamentos = Medicamento.objects.all().order_by(
        'nome'
    )

    return render(

        request,

        'accounts/medicamentos.html',

        {
            'medicamentos': medicamentos
        }

    )


@login_required(login_url='/')
def novo_medicamento(request):

    if request.method == 'POST':

        Medicamento.objects.create(

            nome=request.POST.get(
                'nome'
            ),

            concentracao=request.POST.get(
                'concentracao'
            ),

            categoria=request.POST.get(
                'categoria'
            )

        )

        return redirect(
            'medicamentos'
        )

    return render(

        request,

        'accounts/medicamento_form.html'

    )

# =========================================
# RECEITAS
# =========================================

@login_required(login_url='/')
@perfil_required(
    'admin',
    'dentista'
)
def receitas(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    receitas = Receita.objects.filter(
        paciente=paciente
    )

    return render(

        request,

        'accounts/receitas.html',

        {

            'paciente': paciente,
            'receitas': receitas

        }

    )


# =========================================
# NOVA RECEITA
# =========================================

@login_required(login_url='/')
def nova_receita(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    if request.method == 'POST':

        Receita.objects.create(

            paciente=paciente,

            medicamento=request.POST.get(
                'medicamento'
            ),

            quantidade=request.POST.get(
                'quantidade'
            ),

            posologia=request.POST.get(
                'posologia'
            ),

            observacoes=request.POST.get(
                'observacoes'
            ),

            tipo_receita=request.POST.get(
                'tipo_receita',
                'simples'
            )

        )

        return redirect(
            'receitas',
            id=paciente.id
        )

    return render(

        request,

        'accounts/receita_form.html',

        {

            'paciente': paciente,

            'modelos_receita': ModeloReceita.objects.filter(
                ativo=True
            ).order_by('nome')

        }

    )


# =========================================
# EDITAR RECEITA
# =========================================

@login_required(login_url='/')
def editar_receita(request, id):

    receita = get_object_or_404(
        Receita,
        id=id
    )

    if request.method == 'POST':

        receita.medicamento = request.POST.get(
            'medicamento'
        )

        receita.quantidade = request.POST.get(
            'quantidade'
        )

        receita.posologia = request.POST.get(
            'posologia'
        )

        receita.observacoes = request.POST.get(
            'observacoes'
        )

        receita.tipo_receita = request.POST.get(
            'tipo_receita',
            'simples'
        )

        receita.save()

        return redirect(
            'receitas',
            id=receita.paciente.id
        )

    return render(

        request,

        'accounts/receita_form.html',

        {

            'receita': receita,

            'paciente': receita.paciente

        }

    )


# =========================================
# EXCLUIR RECEITA
# =========================================

@login_required(login_url='/')
def excluir_receita(request, id):

    receita = get_object_or_404(
        Receita,
        id=id
    )

    paciente_id = receita.paciente.id

    receita.delete()

    return redirect(
        'receitas',
        id=paciente_id
    )

# =========================================
# PDF RECEITA
# =========================================

@login_required(login_url='/')
def imprimir_receita(request, id):

    receita = get_object_or_404(
        Receita,
        id=id
    )

    paciente = receita.paciente

    config = ConfiguracaoClinica.objects.first()

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = f'inline; filename="receita_{receita.id}.pdf"'

    doc = SimpleDocTemplate(
        response,
        topMargin=30,
        bottomMargin=30,
        leftMargin=40,
        rightMargin=40
    )

    styles = getSampleStyleSheet()

    elementos = []

    # =========================================
    # LOGO
    # =========================================

    logo_path = os.path.join(
        settings.BASE_DIR,
        'static',
        'img',
        'logo.png'
    )

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=240,
            height=90
        )

        logo.hAlign = 'CENTER'

        elementos.append(logo)

        elementos.append(
            Spacer(1, 8)
        )



    # =========================================
    # TÍTULO
    # =========================================

    titulo = (
        'RECEITA DE CONTROLE ESPECIAL'
        if receita.tipo_receita == 'controle'
        else 'RECEITUÁRIO'
    )

    elementos.append(

        Paragraph(

            f'''
            <para align="center">
            <b>{titulo}</b>
            </para>
            ''',

            styles['Title']

        )

    )

    elementos.append(
        Spacer(1, 10)
    )

    elementos.append(

        HRFlowable(
            width="100%",
            thickness=1.2,
            color=colors.HexColor('#1e40af')
        )

    )

    elementos.append(
        Spacer(1, 15)
    )

    # =========================================
    # PACIENTE
    # =========================================

    elementos.append(

        Paragraph(

            f'<b>Paciente:</b> {paciente.nome}',

            styles['Normal']

        )

    )

    if paciente.cpf:

        elementos.append(

            Paragraph(

                f'<b>CPF:</b> {paciente.cpf}',

                styles['Normal']

            )

        )

    elementos.append(
        Spacer(1, 15)
    )

    # =========================================
    # MEDICAMENTO
    # =========================================

    elementos.append(

        Paragraph(

            '<b>Medicamento:</b>',

            styles['Heading3']

        )

    )

    elementos.append(

        Paragraph(

            str(receita.medicamento),

            styles['BodyText']

        )

    )

    elementos.append(
        Spacer(1, 10)
    )

    # =========================================
    # QUANTIDADE
    # =========================================

    elementos.append(

        Paragraph(

            '<b>Quantidade:</b>',

            styles['Heading3']

        )

    )

    elementos.append(

        Paragraph(

            receita.quantidade,

            styles['BodyText']

        )

    )

    elementos.append(
        Spacer(1, 10)
    )

    # =========================================
    # POSOLOGIA
    # =========================================

    elementos.append(

        Paragraph(

            '<b>Posologia:</b>',

            styles['Heading3']

        )

    )

    elementos.append(

        Paragraph(

            receita.posologia,

            styles['BodyText']

        )

    )

    elementos.append(
        Spacer(1, 10)
    )

    # =========================================
    # OBSERVAÇÕES
    # =========================================

    if receita.observacoes:

        elementos.append(

            Paragraph(

                '<b>Observações:</b>',

                styles['Heading3']

            )

        )

        elementos.append(

            Paragraph(

                receita.observacoes,

                styles['BodyText']

            )

        )

        elementos.append(
            Spacer(1, 10)
        )

    

    # =========================================
    # ASSINATURA
    # =========================================

    elementos.append(
        Spacer(1, 25)
    )

    elementos.append(
        Paragraph(
            '''
            <para align="center">
            _______________________________________
            <br/>
            Cirurgião-Dentista Responsável
            </para>
            ''',
            styles['Normal']
        )
    )

    # =========================================
    # RODAPÉ
    # =========================================

    elementos.append(
        Spacer(1, 20)
    )

    elementos.append(
        HRFlowable(
            width="100%",
            thickness=0.8,
            color=colors.grey
        )
    )

    elementos.append(
        Spacer(1, 8)
    )

    if config and config.nome_clinica:

        elementos.append(
            Paragraph(
                f'''
                <para align="center">
                <b>{config.nome_clinica}</b>
                </para>
                ''',
                styles['Normal']
            )
        )

    if config and config.telefone:

        elementos.append(
            Paragraph(
                f'''
                <para align="center">
                Tel: {config.telefone}
                &nbsp;&nbsp;&nbsp;
                WhatsApp: {config.whatsapp}
                </para>
                ''',
                styles['BodyText']
            )
        )

    if config and config.endereco:

        elementos.append(
            Paragraph(
                f'''
                <para align="center">
                {config.endereco}
                </para>
                ''',
                styles['BodyText']
            )
        )

    if config and config.email:

        elementos.append(
            Paragraph(
                f'''
                <para align="center">
                {config.email}
                </para>
                ''',
                styles['BodyText']
            )
        )

    doc.build(elementos)

    return response

# =========================================
# MODELO DE RECEITA AJAX
# =========================================

@login_required(login_url='/')
def buscar_modelo_receita(request, id):

    modelo = get_object_or_404(
        ModeloReceita,
        id=id
    )

    return JsonResponse({

        'medicamento': modelo.medicamento,

        'quantidade': modelo.quantidade,

        'posologia': modelo.posologia,

    })

# =========================================
# MODELOS DE RECEITA
# =========================================

@login_required(login_url='/')
def modelos_receita(request):

    modelos = ModeloReceita.objects.all().order_by(
        'nome'
    )

    if request.method == 'POST':

        ModeloReceita.objects.create(

            nome=request.POST.get(
                'nome'
            ),

            medicamento=request.POST.get(
                'medicamento'
            ),

            quantidade=request.POST.get(
                'quantidade'
            ),

            posologia=request.POST.get(
                'posologia'
            ),

            ativo='ativo' in request.POST

        )

        return redirect(
            'modelos_receita'
        )

    return render(

        request,

        'accounts/modelos_receita.html',

        {

            'modelos': modelos

        }

    )

# =========================================
# EXCLUIR MODELO RECEITA
# =========================================

@login_required(login_url='/')
def excluir_modelo_receita(request, id):

    modelo = get_object_or_404(
        ModeloReceita,
        id=id
    )

    modelo.delete()

    return redirect(
        'modelos_receita'
    )

# =========================================
# EDITAR MODELO RECEITA
# =========================================

@login_required(login_url='/')
def editar_modelo_receita(request, id):

    modelo = get_object_or_404(
        ModeloReceita,
        id=id
    )

    if request.method == 'POST':

        modelo.nome = request.POST.get(
            'nome'
        )

        modelo.medicamento = request.POST.get(
            'medicamento'
        )

        modelo.quantidade = request.POST.get(
            'quantidade'
        )

        modelo.posologia = request.POST.get(
            'posologia'
        )

        modelo.ativo = (
            'ativo' in request.POST
        )

        modelo.save()

        return redirect(
            'modelos_receita'
        )

    return render(

        request,

        'accounts/modelo_receita_form.html',

        {

            'modelo': modelo

        }

    )

# =========================================
# EXAMES
# =========================================

@login_required(login_url='/')
def exames(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    exames = Exame.objects.filter(
        paciente=paciente
    ).order_by(
        '-criado_em'
    )

    return render(

        request,

        'accounts/exames.html',

        {

            'paciente': paciente,
            'exames': exames

        }

    )


# =========================================
# NOVO EXAME
# =========================================

@login_required(login_url='/')
def novo_exame(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    if request.method == 'POST':

        Exame.objects.create(

            paciente=paciente,

            nome=request.POST.get(
                'nome'
            ),

            data_exame=request.POST.get(
                'data_exame'
            ),

            observacoes=request.POST.get(
                'observacoes'
            ),

            arquivo=request.FILES.get(
                'arquivo'
            )

        )

        return redirect(
            'exames',
            paciente.id
        )

    return render(

        request,

        'accounts/novo_exame.html',

        {

            'paciente': paciente

        }

    )


# =========================================
# EXCLUIR EXAME
# =========================================

@login_required(login_url='/')
def excluir_exame(request, id):

    exame = get_object_or_404(
        Exame,
        id=id
    )

    paciente_id = exame.paciente.id

    if exame.arquivo:

        exame.arquivo.delete(
            save=False
        )

    exame.delete()

    return redirect(
        'exames',
        paciente_id
    )

# =========================================
# SOLICITAÇÕES DE EXAMES
# =========================================

@login_required(login_url='/')
@perfil_required(
    'admin',
    'dentista'
)
def solicitacoes_exames(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    solicitacoes = SolicitacaoExame.objects.filter(
        paciente=paciente
    )

    return render(

        request,

        'accounts/solicitacoes_exames.html',

        {

            'paciente': paciente,
            'solicitacoes': solicitacoes

        }

    )


# =========================================
# NOVA SOLICITAÇÃO DE EXAME
# =========================================

@login_required(login_url='/')
@perfil_required(
    'admin',
    'dentista'
)
def nova_solicitacao_exame(request, id):

    paciente = get_object_or_404(
        Paciente,
        id=id
    )

    if request.method == 'POST':

        SolicitacaoExame.objects.create(

            paciente=paciente,

            titulo=request.POST.get(
                'titulo'
            ),

            exames_solicitados=request.POST.get(
                'exames_solicitados'
            ),

            observacoes=request.POST.get(
                'observacoes'
            )

        )

        return redirect(
            'solicitacoes_exames',
            paciente.id
        )

    return render(

        request,

        'accounts/nova_solicitacao_exame.html',

        {

            'paciente': paciente

        }

    )


# =========================================
# EXCLUIR SOLICITAÇÃO
# =========================================

@login_required(login_url='/')
def excluir_solicitacao_exame(request, id):

    solicitacao = get_object_or_404(
        SolicitacaoExame,
        id=id
    )

    paciente_id = solicitacao.paciente.id

    solicitacao.delete()

    return redirect(
        'solicitacoes_exames',
        paciente_id
    )


# =========================================
# PDF SOLICITAÇÃO DE EXAME
# =========================================

@login_required(login_url='/')
def imprimir_solicitacao_exame(request, id):

    solicitacao = get_object_or_404(
        SolicitacaoExame,
        id=id
    )

    paciente = solicitacao.paciente

    config = ConfiguracaoClinica.objects.first()

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        f'inline; '
        f'filename="solicitacao_exame_{solicitacao.id}.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        topMargin=30,
        bottomMargin=30,
        leftMargin=40,
        rightMargin=40
    )

    styles = getSampleStyleSheet()

    elementos = []

    # =========================================
    # LOGO
    # =========================================

    logo_path = os.path.join(
        settings.BASE_DIR,
        'static',
        'img',
        'logo.png'
    )

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=240,
            height=90
        )

        logo.hAlign = 'CENTER'

        elementos.append(logo)

        elementos.append(
            Spacer(1, 8)
        )

    # =========================================
    # TÍTULO
    # =========================================

    elementos.append(

        Paragraph(

            '''
            <para align="center">
            <b>SOLICITAÇÃO DE EXAMES</b>
            </para>
            ''',

            styles['Title']

        )

    )

    elementos.append(
        Spacer(1, 10)
    )

    elementos.append(

        HRFlowable(
            width="100%",
            thickness=1.2,
            color=colors.HexColor('#1e40af')
        )

    )

    elementos.append(
        Spacer(1, 15)
    )

    # =========================================
    # PACIENTE
    # =========================================

    elementos.append(

        Paragraph(

            f'<b>Paciente:</b> {paciente.nome}',

            styles['Normal']

        )

    )

    if paciente.cpf:

        elementos.append(

            Paragraph(

                f'<b>CPF:</b> {paciente.cpf}',

                styles['Normal']

            )

        )

    elementos.append(
        Spacer(1, 15)
    )

    # =========================================
    # TÍTULO DA SOLICITAÇÃO
    # =========================================

    elementos.append(

        Paragraph(

            '<b>Título:</b>',

            styles['Heading3']

        )

    )

    elementos.append(

        Paragraph(

            solicitacao.titulo,

            styles['BodyText']

        )

    )

    elementos.append(
        Spacer(1, 10)
    )

    # =========================================
    # EXAMES SOLICITADOS
    # =========================================

    elementos.append(

        Paragraph(

            '<b>Exames Solicitados:</b>',

            styles['Heading3']

        )

    )

    elementos.append(

        Paragraph(

            solicitacao.exames_solicitados.replace(
                '\n',
                '<br/>'
            ),

            styles['BodyText']

        )

    )

    elementos.append(
        Spacer(1, 10)
    )

    # =========================================
    # OBSERVAÇÕES
    # =========================================

    if solicitacao.observacoes:

        elementos.append(

            Paragraph(

                '<b>Observações:</b>',

                styles['Heading3']

            )

        )

        elementos.append(

            Paragraph(

                solicitacao.observacoes.replace(
                    '\n',
                    '<br/>'
                ),

                styles['BodyText']

            )

        )

        elementos.append(
            Spacer(1, 10)
        )

    # =========================================
    # DATA
    # =========================================

    elementos.append(

        Paragraph(

            (
                f'Franca/SP, '
                f'{solicitacao.criado_em.strftime("%d/%m/%Y")}'
            ),

            styles['Normal']

        )

    )

    # =========================================
    # ASSINATURA
    # =========================================

    elementos.append(
        Spacer(1, 35)
    )

    elementos.append(

        Paragraph(

            '''
            <para align="center">
            _______________________________________
            <br/>
            Cirurgião-Dentista Responsável
            </para>
            ''',

            styles['Normal']

        )

    )

    # =========================================
    # RODAPÉ
    # =========================================

    elementos.append(
        Spacer(1, 20)
    )

    elementos.append(

        HRFlowable(
            width="100%",
            thickness=0.8,
            color=colors.grey
        )

    )

    elementos.append(
        Spacer(1, 8)
    )

    if config and config.nome_clinica:

        elementos.append(

            Paragraph(

                f'''
                <para align="center">
                <b>{config.nome_clinica}</b>
                </para>
                ''',

                styles['Normal']

            )

        )

    if config and config.telefone:

        elementos.append(

            Paragraph(

                f'''
                <para align="center">
                Tel: {config.telefone}
                &nbsp;&nbsp;&nbsp;
                WhatsApp: {config.whatsapp}
                </para>
                ''',

                styles['BodyText']

            )

        )

    if config and config.endereco:

        elementos.append(

            Paragraph(

                f'''
                <para align="center">
                {config.endereco}
                </para>
                ''',

                styles['BodyText']

            )

        )

    if config and config.email:

        elementos.append(

            Paragraph(

                f'''
                <para align="center">
                {config.email}
                </para>
                ''',

                styles['BodyText']

            )

        )

    doc.build(elementos)

    return response

# =========================================
# PERFIS
# =========================================

def usuario_admin(user):

    if not hasattr(user, 'perfil'):
        return False

    return user.perfil.tipo_usuario == 'admin'


def usuario_gestor(user):

    if not hasattr(user, 'perfil'):
        return False

    return user.perfil.tipo_usuario == 'gestor'


def usuario_dentista(user):

    if not hasattr(user, 'perfil'):
        return False

    return user.perfil.tipo_usuario == 'dentista'

def usuario_secretaria(user):

    if not hasattr(user, 'perfil'):
        return False

    return user.perfil.tipo_usuario == 'secretaria'


def usuario_acd(user):

    if not hasattr(user, 'perfil'):
        return False

    return user.perfil.tipo_usuario == 'acd'


def usuario_contabilidade(user):

    if not hasattr(user, 'perfil'):
        return False

    return user.perfil.tipo_usuario == 'contabilidade'


def usuario_marketing(user):

    if not hasattr(user, 'perfil'):
        return False

    return user.perfil.tipo_usuario == 'marketing'


def usuario_auditoria(user):

    if not hasattr(user, 'perfil'):
        return False

    return user.perfil.tipo_usuario == 'auditoria'

# =========================================
# USUÁRIOS
# =========================================

@login_required
@perfil_required(
    'admin',
    'gestor'
)
def usuarios(request):

    usuarios = User.objects.select_related(
        'perfil'
    ).order_by(
        'first_name',
        'username'
    )

    context = {
        'usuarios': usuarios
    }

    return render(
        request,
        'accounts/usuarios.html',
        context
    )

# =========================================
# NOVO USUÁRIO
# =========================================

@login_required
def novo_usuario(request):

    if request.method == 'POST':

        nome = request.POST.get('nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Já existe um usuário com esse login.'
            )

            return redirect('novo_usuario')

        usuario = User.objects.create_user(
            username=username,
            email=email,
            password=senha,
            first_name=nome
        )

        PerfilUsuario.objects.create(
            usuario=usuario,

            # Perfil
            tipo_usuario=request.POST.get('tipo_usuario'),

            # Dados pessoais
            foto=request.FILES.get('foto'),
            cpf=request.POST.get('cpf'),
            rg=request.POST.get('rg'),
            data_nascimento=request.POST.get('data_nascimento') or None,
            sexo=request.POST.get('sexo'),

            # Contato
            telefone=request.POST.get('telefone'),
            celular=request.POST.get('celular'),

            # Endereço
            cep=request.POST.get('cep'),
            logradouro=request.POST.get('logradouro'),
            numero=request.POST.get('numero'),
            complemento=request.POST.get('complemento'),
            bairro=request.POST.get('bairro'),
            cidade=request.POST.get('cidade'),
            uf=request.POST.get('uf'),

            # Dados profissionais
            cro=request.POST.get('cro'),
            cro_uf=request.POST.get('cro_uf'),
            especialidade=request.POST.get('especialidade'),
            assinatura=request.FILES.get('assinatura')
        )

        messages.success(
            request,
            'Usuário criado com sucesso.'
        )

        return redirect('usuarios')

    return render(
        request,
        'accounts/usuario_form.html'
    )

# =========================================
# EDITAR USUÁRIO
# =========================================

@login_required
def editar_usuario(request, id):

    usuario = User.objects.get(id=id)

    perfil = usuario.perfil

    if request.method == 'POST':

        usuario.first_name = request.POST.get('nome')

        usuario.username = request.POST.get('username')

        usuario.email = request.POST.get('email')

        usuario.save()

        perfil.tipo_usuario = request.POST.get(
            'tipo_usuario'
        )

        perfil.cro = request.POST.get('cro')

        perfil.especialidade = request.POST.get(
            'especialidade'
        )

        perfil.telefone = request.POST.get(
            'telefone'
        )

        perfil.save()

        messages.success(
            request,
            'Usuário atualizado com sucesso.'
        )

        return redirect('usuarios')

    context = {

        'usuario_obj': usuario,
        'perfil': perfil

    }

    return render(

        request,

        'accounts/usuario_form.html',

        context

    )

@login_required
def alterar_status_usuario(request, id):

    usuario = User.objects.get(id=id)

    if usuario.id == request.user.id:

        messages.warning(
            request,
            'Você não pode desativar seu próprio usuário.'
        )

        return redirect('usuarios')

    perfil = usuario.perfil

    perfil.ativo = not perfil.ativo

    perfil.save()

    messages.success(
        request,
        'Status atualizado com sucesso.'
    )

    return redirect('usuarios')

# =========================================
# MEU PERFIL
# =========================================

@login_required
def meu_perfil(request):

    usuario = request.user
    perfil = usuario.perfil

    if request.method == 'POST':

        # =====================================
        # USUÁRIO
        # =====================================

        usuario.first_name = request.POST.get('nome')
        usuario.email = request.POST.get('email')

        usuario.save()

        # =====================================
        # DADOS PESSOAIS
        # =====================================

        perfil.telefone = request.POST.get('telefone')
        perfil.celular = request.POST.get('celular')

        perfil.cpf = request.POST.get('cpf')
        perfil.rg = request.POST.get('rg')

        perfil.sexo = request.POST.get('sexo')

        data_nascimento = request.POST.get('data_nascimento')

        if data_nascimento:
            perfil.data_nascimento = data_nascimento

        # =====================================
        # ENDEREÇO
        # =====================================

        perfil.cep = request.POST.get('cep')
        perfil.logradouro = request.POST.get('logradouro')
        perfil.numero = request.POST.get('numero')
        perfil.complemento = request.POST.get('complemento')

        perfil.bairro = request.POST.get('bairro')
        perfil.cidade = request.POST.get('cidade')
        perfil.uf = request.POST.get('uf')

        # =====================================
        # DADOS PROFISSIONAIS
        # =====================================

        perfil.cro = request.POST.get('cro')
        perfil.cro_uf = request.POST.get('cro_uf')
        perfil.especialidade = request.POST.get('especialidade')

        # =====================================
        # FOTO
        # =====================================

        if request.FILES.get('foto'):

            perfil.foto = request.FILES.get('foto')

        # =====================================
        # ASSINATURA
        # =====================================

        if request.FILES.get('assinatura'):

            perfil.assinatura = request.FILES.get('assinatura')

        perfil.save()

        messages.success(
            request,
            'Perfil atualizado com sucesso.'
        )

        return redirect('meu_perfil')

    context = {

        'usuario_obj': usuario,
        'perfil': perfil

    }

    return render(

        request,

        'accounts/meu_perfil.html',

        context

    )

# =========================================
# ALTERAR SENHA
# =========================================

@login_required
def alterar_senha(request):

    if request.method == 'POST':

        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not request.user.check_password(senha_atual):

            messages.error(
                request,
                'Senha atual incorreta.'
            )

            return redirect('alterar_senha')

        if nova_senha != confirmar_senha:

            messages.error(
                request,
                'As senhas não conferem.'
            )

            return redirect('alterar_senha')

        request.user.set_password(nova_senha)
        request.user.save()

        update_session_auth_hash(
            request,
            request.user
        )

        messages.success(
            request,
            'Senha alterada com sucesso.'
        )

        return redirect('meu_perfil')

    return render(
        request,
        'accounts/alterar_senha.html'
    )

# =========================================
# ATIVAR USUÁRIO
# =========================================

@login_required
def ativar_usuario(request, id):

    usuario = User.objects.get(id=id)

    usuario.perfil.ativo = True

    usuario.perfil.save()

    return redirect('usuarios')


# =========================================
# DESATIVAR USUÁRIO
# =========================================

@login_required
def desativar_usuario(request, id):

    usuario = User.objects.get(id=id)

    usuario.perfil.ativo = False

    usuario.perfil.save()

    return redirect('usuarios')



# =========================================
# FORNECEDORES
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def fornecedores(request):

    fornecedores = Fornecedor.objects.order_by(
        'nome'
    )

    context = {
        'fornecedores': fornecedores
    }

    return render(
        request,
        'accounts/fornecedores.html',
        context
    )


# =========================================
# VALIDAÇÃO DO CNPJ
# =========================================

import re

def validar_cnpj(cnpj):

    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14:
        return False

    if cnpj == cnpj[0] * 14:
        return False

    peso1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    soma = sum(int(cnpj[i]) * peso1[i] for i in range(12))

    dig1 = 0 if soma % 11 < 2 else 11 - (soma % 11)

    if dig1 != int(cnpj[12]):
        return False

    peso2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
    soma = sum(int(cnpj[i]) * peso2[i] for i in range(13))

    dig2 = 0 if soma % 11 < 2 else 11 - (soma % 11)

    return dig2 == int(cnpj[13])

# =========================================
# NOVO FORNECEDOR
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def novo_fornecedor(request):

    if request.method == 'POST':

        nome = request.POST.get(
            'nome'
        )

        if not nome:

            messages.error(
                request,
                'Informe o nome do fornecedor.'
            )

            return render(
                request,
                'accounts/fornecedor_form.html'
            )

        cnpj = request.POST.get(
            'cnpj'
        )

        if cnpj:

            if not validar_cnpj(cnpj):

                messages.error(
                    request,
                    'CNPJ inválido.'
                )

                return render(
                    request,
                    'accounts/fornecedor_form.html'
                )

            if Fornecedor.objects.filter(
                cnpj=cnpj
            ).exists():

                messages.error(
                    request,
                    'Já existe um fornecedor com este CNPJ.'
                )

                return render(
                    request,
                    'accounts/fornecedor_form.html'
                )

        Fornecedor.objects.create(

            nome=nome,

            razao_social=request.POST.get(
                'razao_social'
            ),

            cnpj=cnpj,

            contato=request.POST.get(
                'contato'
            ),

            telefone=request.POST.get(
                'telefone'
            ),

            celular=request.POST.get(
                'celular'
            ),

            email=request.POST.get(
                'email'
            ),

            cep=request.POST.get(
                'cep'
            ),

            logradouro=request.POST.get(
                'logradouro'
            ),

            numero=request.POST.get(
                'numero'
            ),

            complemento=request.POST.get(
                'complemento'
            ),

            bairro=request.POST.get(
                'bairro'
            ),

            cidade=request.POST.get(
                'cidade'
            ),

            uf=request.POST.get(
                'uf'
            ),

            ativo=True

        )

        messages.success(
            request,
            'Fornecedor cadastrado com sucesso.'
        )

        return redirect(
            'fornecedores'
        )

    return render(
        request,
        'accounts/fornecedor_form.html'
    )

# =========================================
# EDITAR FORNECEDOR
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def editar_fornecedor(request, fornecedor_id):

    fornecedor = get_object_or_404(
        Fornecedor,
        id=fornecedor_id
    )

    if request.method == 'POST':

        cnpj = request.POST.get(
            'cnpj'
        )

        if cnpj:

            cnpj_limpo = re.sub(
                r'\D',
                '',
                cnpj
            )

            if not validar_cnpj(cnpj_limpo):

                messages.error(
                    request,
                    'CNPJ inválido.'
                )

                return render(
                    request,
                    'accounts/fornecedor_form.html',
                    {
                        'fornecedor': fornecedor
                    }
                )

            if Fornecedor.objects.filter(
                cnpj=cnpj
            ).exclude(
                id=fornecedor.id
            ).exists():

                messages.error(
                    request,
                    'Já existe outro fornecedor com este CNPJ.'
                )

                return render(
                    request,
                    'accounts/fornecedor_form.html',
                    {
                        'fornecedor': fornecedor
                    }
                )

        fornecedor.nome = request.POST.get(
            'nome'
        )

        fornecedor.razao_social = request.POST.get(
            'razao_social'
        )

        fornecedor.cnpj = cnpj

        fornecedor.nome = request.POST.get(
            'nome'
        )

        fornecedor.razao_social = request.POST.get(
            'razao_social'
        )

        fornecedor.cnpj = request.POST.get(
            'cnpj'
        )

        fornecedor.contato = request.POST.get(
            'contato'
        )

        fornecedor.telefone = request.POST.get(
            'telefone'
        )

        fornecedor.celular = request.POST.get(
            'celular'
        )

        fornecedor.email = request.POST.get(
            'email'
        )

        fornecedor.cep = request.POST.get(
            'cep'
        )

        fornecedor.logradouro = request.POST.get(
            'logradouro'
        )

        fornecedor.numero = request.POST.get(
            'numero'
        )

        fornecedor.complemento = request.POST.get(
            'complemento'
        )

        fornecedor.bairro = request.POST.get(
            'bairro'
        )

        fornecedor.cidade = request.POST.get(
            'cidade'
        )

        fornecedor.uf = request.POST.get(
            'uf'
        )

        fornecedor.save()

        messages.success(
            request,
            'Fornecedor atualizado com sucesso.'
        )

        return redirect(
            'fornecedores'
        )

    return render(
        request,
        'accounts/fornecedor_form.html',
        {
            'fornecedor': fornecedor
        }
    )

# =========================================
# ALTERAR STATUS DO FORNECEDOR
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def alterar_status_fornecedor(
    request,
    fornecedor_id
):

    fornecedor = get_object_or_404(
        Fornecedor,
        id=fornecedor_id
    )

    fornecedor.ativo = not fornecedor.ativo

    fornecedor.save()

    messages.success(
        request,
        'Status do fornecedor atualizado.'
    )

    return redirect(
        'fornecedores'
    )

# =========================================
# EXCLUIR FORNECEDOR
# =========================================


@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def excluir_fornecedor(
    request,
    fornecedor_id
):

    fornecedor = get_object_or_404(
        Fornecedor,
        id=fornecedor_id
    )

    fornecedor.delete()

    messages.success(
        request,
        'Fornecedor excluído com sucesso.'
    )

    return redirect(
        'fornecedores'
    )

# =========================================
# PRODUTOS
# =========================================

from django.db.models import F

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def produtos(request):

    produtos = Produto.objects.order_by(
        'nome'
    )

    produtos_baixos = Produto.objects.filter(
        ativo=True,
        estoque__lte=F('estoque_minimo')
    )

    context = {

        'produtos': produtos,

        'produtos_baixos': produtos_baixos,

        'total_produtos_baixos': produtos_baixos.count()

    }

    return render(

        request,

        'accounts/produtos.html',

        context

    )

# =========================================
# NOVO PRODUTO
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def novo_produto(request):

    if request.method == 'POST':

        nome = request.POST.get(
            'nome'
        )

        if not nome:

            messages.error(
                request,
                'Informe o nome do produto.'
            )

            return render(
                request,
                'accounts/produto_form.html'
            )

        Produto.objects.create(

            nome=nome,

            descricao=request.POST.get(
                'descricao'
            ),

            codigo=request.POST.get(
                'codigo'
            ),

            estoque=request.POST.get(
                'estoque'
            ) or 0,

            estoque_minimo=request.POST.get(
                'estoque_minimo'
            ) or 0,

            valor_compra=request.POST.get(
                'valor_compra'
            ) or 0,

            valor_venda=request.POST.get(
                'valor_venda'
            ) or 0,

            ativo=True

        )

        messages.success(
            request,
            'Produto cadastrado com sucesso.'
        )

        return redirect(
            'produtos'
        )

    return render(
        request,
        'accounts/produto_form.html'
    )

# =========================================
# EDITAR PRODUTO
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def editar_produto(
    request,
    produto_id
):

    produto = get_object_or_404(
        Produto,
        id=produto_id
    )

    if request.method == 'POST':

        produto.nome = request.POST.get(
            'nome'
        )

        produto.descricao = request.POST.get(
            'descricao'
        )

        produto.codigo = request.POST.get(
            'codigo'
        )

        produto.estoque = request.POST.get(
            'estoque'
        ) or 0

        produto.estoque_minimo = request.POST.get(
            'estoque_minimo'
        ) or 0

        produto.valor_compra = request.POST.get(
            'valor_compra'
        ) or 0

        produto.valor_venda = request.POST.get(
            'valor_venda'
        ) or 0

        produto.save()

        messages.success(
            request,
            'Produto atualizado com sucesso.'
        )

        return redirect(
            'produtos'
        )

    context = {
        'produto': produto
    }

    return render(
        request,
        'accounts/produto_form.html',
        context
    )

# =========================================
# STATUS PRODUTO
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def alterar_status_produto(
    request,
    produto_id
):

    produto = get_object_or_404(
        Produto,
        id=produto_id
    )

    produto.ativo = not produto.ativo

    produto.save()

    return redirect(
        'produtos'
    )

# =========================================
# EXCLUIR PRODUTO
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def excluir_produto(
    request,
    produto_id
):

    produto = get_object_or_404(
        Produto,
        id=produto_id
    )

    produto.delete()

    messages.success(
        request,
        'Produto excluído com sucesso.'
    )

    return redirect(
        'produtos'
    )

# =========================================
# COMPRAS
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def compras(request):

    compras = Compra.objects.select_related(
        'fornecedor'
    ).order_by('-id')

    context = {
        'compras': compras
    }

    return render(
        request,
        'accounts/compras.html',
        context
    )

# =========================================
# NOVA COMPRA
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def nova_compra(request):

    fornecedores = Fornecedor.objects.filter(
        ativo=True
    ).order_by('nome')

    produtos = Produto.objects.filter(
        ativo=True
    ).order_by('nome')

    if request.method == 'POST':

        fornecedor_id = request.POST.get(
            'fornecedor'
        )

        data_compra = request.POST.get(
            'data_compra'
        )

        numero_nf = request.POST.get(
            'numero_nf'
        )

        observacoes = request.POST.get(
            'observacoes'
        )

        arquivo_nf = request.FILES.get(
            'arquivo_nf'
        )

        compra = Compra.objects.create(

            fornecedor_id=fornecedor_id,

            data_compra=data_compra,

            numero_nf=numero_nf,

            observacoes=observacoes,

            arquivo_nf=arquivo_nf,

            valor_total=0

        )

        produtos_ids = request.POST.getlist(
            'produto[]'
        )

        quantidades = request.POST.getlist(
            'quantidade[]'
        )

        valores = request.POST.getlist(
            'valor_unitario[]'
        )

        total_compra = Decimal('0.00')

        for i in range(
            len(produtos_ids)
        ):

            produto = Produto.objects.get(
                id=produtos_ids[i]
            )

            quantidade = int(
                quantidades[i]
            )

            valor_unitario = Decimal(
                valores[i]
            )

            subtotal = (
                quantidade *
                valor_unitario
            )

            ItemCompra.objects.create(

                compra=compra,

                produto=produto,

                quantidade=quantidade,

                valor_unitario=valor_unitario,

                subtotal=subtotal

            )

            produto.estoque += quantidade

            produto.save()

            total_compra += subtotal

        compra.valor_total = total_compra

        compra.save()

        messages.success(

            request,

            'Compra cadastrada com sucesso.'

        )

        return redirect(
            'compras'
        )

    context = {

        'fornecedores': fornecedores,

        'produtos': produtos

    }

    return render(

        request,

        'accounts/compra_form.html',

        context

    )


# =========================================
# VISUALIZAR COMPRA
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def visualizar_compra(request, compra_id):

    compra = get_object_or_404(
        Compra,
        id=compra_id
    )

    itens = ItemCompra.objects.filter(
        compra=compra
    )

    context = {

        'compra': compra,
        'itens': itens

    }

    return render(

        request,

        'accounts/compra_visualizar.html',

        context

    )

# =========================================
# EDITAR COMPRA
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def editar_compra(request, compra_id):

    compra = get_object_or_404(
        Compra,
        id=compra_id
    )

    item = ItemCompra.objects.filter(
        compra=compra
    ).first()

    fornecedores = Fornecedor.objects.filter(
        ativo=True
    ).order_by('nome')

    produtos = Produto.objects.filter(
        ativo=True
    ).order_by('nome')

    if request.method == 'POST':

        fornecedor_id = request.POST.get(
            'fornecedor'
        )

        data_compra = request.POST.get(
            'data_compra'
        )

        numero_nf = request.POST.get(
            'numero_nf'
        )

        observacoes = request.POST.get(
            'observacoes'
        )

        produto_id = request.POST.get(
            'produto'
        )

        nova_quantidade = int(
            request.POST.get(
                'quantidade',
                0
            )
        )

        novo_valor = Decimal(
            request.POST.get(
                'valor_unitario',
                0
            )
        )

        if item:

            produto_antigo = item.produto

            produto_antigo.estoque -= (
                item.quantidade
            )

            if produto_antigo.estoque < 0:

                produto_antigo.estoque = 0

            produto_antigo.save()

        produto = Produto.objects.get(
            id=produto_id
        )

        subtotal = (
            nova_quantidade *
            novo_valor
        )

        produto.estoque += (
            nova_quantidade
        )

        produto.save()

        compra.fornecedor_id = (
            fornecedor_id
        )

        compra.data_compra = (
            data_compra
        )

        compra.numero_nf = (
            numero_nf
        )

        compra.observacoes = (
            observacoes
        )

        compra.valor_total = (
            subtotal
        )

        compra.save()

        if item:

            item.produto = produto

            item.quantidade = (
                nova_quantidade
            )

            item.valor_unitario = (
                novo_valor
            )

            item.subtotal = (
                subtotal
            )

            item.save()

        messages.success(

            request,

            'Compra atualizada com sucesso.'

        )

        return redirect(
            'compras'
        )

    context = {

        'compra': compra,

        'item': item,

        'fornecedores': fornecedores,

        'produtos': produtos

    }

    return render(

        request,

        'accounts/compra_editar.html',

        context

    )

# =========================================
# EXCLUIR COMPRA
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def excluir_compra(request, compra_id):

    compra = get_object_or_404(
        Compra,
        id=compra_id
    )

    itens = ItemCompra.objects.filter(
        compra=compra
    )

    for item in itens:

        produto = item.produto

        produto.estoque -= item.quantidade

        if produto.estoque < 0:

            produto.estoque = 0

        produto.save()

    compra.delete()

    messages.success(
        request,
        'Compra excluída com sucesso.'
    )

    return redirect(
        'compras'
    )

# =========================================
# ESTOQUE
# =========================================

from django.db.models import F
from decimal import Decimal

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def estoque(request):

    produtos = Produto.objects.filter(
        ativo=True
    ).order_by('nome')

    produtos_baixos = produtos.filter(
        estoque__lte=F('estoque_minimo')
    )

    valor_total_estoque = Decimal('0.00')

    for produto in produtos:

        produto.valor_estoque = (
            produto.estoque *
            produto.valor_compra
        )

        valor_total_estoque += (
            produto.valor_estoque
        )

    context = {

        'produtos': produtos,

        'produtos_baixos': produtos_baixos,

        'total_produtos': produtos.count(),

        'total_produtos_baixos': produtos_baixos.count(),

        'valor_total_estoque': valor_total_estoque

    }

    return render(

        request,

        'accounts/estoque.html',

        context

    )

# =========================================
# MOVIMENTAÇÕES DE ESTOQUE
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def movimentacoes_estoque(request):

    movimentacoes = (
        MovimentacaoEstoque.objects
        .select_related(
            'produto',
            'usuario'
        )
        .order_by(
            '-criado_em'
        )
    )

    produtos = Produto.objects.filter(
        ativo=True
    ).order_by(
        'nome'
    )

    produto_id = request.GET.get(
        'produto'
    )

    tipo = request.GET.get(
        'tipo'
    )

    data_inicial = request.GET.get(
        'data_inicial'
    )

    data_final = request.GET.get(
        'data_final'
    )

    if produto_id:

        movimentacoes = movimentacoes.filter(
            produto_id=produto_id
        )

    if tipo:

        movimentacoes = movimentacoes.filter(
            tipo=tipo
        )

    if data_inicial:

        movimentacoes = movimentacoes.filter(
            criado_em__date__gte=data_inicial
        )

    if data_final:

        movimentacoes = movimentacoes.filter(
            criado_em__date__lte=data_final
        )

    context = {

        'movimentacoes': movimentacoes,

        'produtos': produtos,

        'produto_id': produto_id,

        'tipo': tipo,

        'data_inicial': data_inicial,

        'data_final': data_final

    }

    return render(

        request,

        'accounts/movimentacoes_estoque.html',

        context

    )

# =========================================
# FUNÇÃO AUXILIAR
# =========================================

def registrar_movimentacao(
    produto,
    tipo,
    quantidade,
    usuario,
    observacao=''
):

    estoque_anterior = produto.estoque

    if tipo == 'SAIDA':

        if quantidade > produto.estoque:

            raise ValueError(
                'Estoque insuficiente.'
            )

        produto.estoque -= quantidade

    elif tipo in [

        'COMPRA',
        'ENTRADA'

    ]:

        produto.estoque += quantidade

    elif tipo == 'AJUSTE':

        produto.estoque = quantidade

    produto.save()

    MovimentacaoEstoque.objects.create(

        produto=produto,

        tipo=tipo,

        quantidade=quantidade,

        estoque_anterior=estoque_anterior,

        estoque_atual=produto.estoque,

        observacao=observacao,

        usuario=usuario

    )


# =========================================
# NOVA MOVIMENTAÇÃO DE ESTOQUE
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def nova_movimentacao_estoque(request):

    produtos = Produto.objects.filter(
        ativo=True
    ).order_by(
        'nome'
    )

    if request.method == 'POST':

        produto = get_object_or_404(
            Produto,
            id=request.POST.get('produto')
        )

        tipo = request.POST.get(
            'tipo'
        )

        quantidade = int(
            request.POST.get(
                'quantidade'
            ) or 0
        )

        observacao = request.POST.get(
            'observacao'
        )

        try:

            registrar_movimentacao(
                produto=produto,
                tipo=tipo,
                quantidade=quantidade,
                usuario=request.user,
                observacao=observacao
            )

            messages.success(
                request,
                'Movimentação registrada com sucesso.'
            )

            return redirect(
                'movimentacoes_estoque'
            )

        except ValueError as erro:

            messages.error(
                request,
                str(erro)
            )

    context = {

        'produtos': produtos

    }

    return render(

        request,

        'accounts/movimentacao_form.html',

        context

    )


# =========================================
# PRODUTOS CRÍTICOS
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def produtos_criticos(request):

    produtos = Produto.objects.filter(
        ativo=True,
        estoque__lte=F('estoque_minimo')
    ).order_by(
        'nome'
    )

    context = {

        'produtos': produtos,

        'total_produtos': produtos.count()

    }

    return render(

        request,

        'accounts/produtos_criticos.html',

        context

    )

# =========================================
# LOTES
# =========================================

from datetime import date, timedelta

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def lotes(request):

    lotes = LoteProduto.objects.select_related(
        'produto'
    ).order_by(
        'validade'
    )

    hoje = date.today()

    for lote in lotes:

        dias = (
            lote.validade - hoje
        ).days

        if dias < 0:

            lote.status_validade = 'VENCIDO'

        elif dias <= 30:

            lote.status_validade = '30_DIAS'

        elif dias <= 60:

            lote.status_validade = '60_DIAS'

        else:

            lote.status_validade = 'VALIDO'

    context = {

        'lotes': lotes,

        'total_lotes': lotes.count()

    }

    return render(

        request,

        'accounts/lotes.html',

        context

    )

# =========================================
# NOVO LOTE
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def novo_lote(request):

    produtos = Produto.objects.filter(
        ativo=True
    ).order_by(
        'nome'
    )

    if request.method == 'POST':

        LoteProduto.objects.create(

            produto_id=request.POST.get(
                'produto'
            ),

            lote=request.POST.get(
                'lote'
            ),

            quantidade=request.POST.get(
                'quantidade'
            ) or 0,

            validade=request.POST.get(
                'validade'
            )

        )

        messages.success(
            request,
            'Lote cadastrado com sucesso.'
        )

        return redirect(
            'lotes'
        )

    return render(

        request,

        'accounts/lote_form.html',

        {
            'produtos': produtos
        }

    )

# =========================================
# CONTAS A PAGAR
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def contas_pagar(request):

    hoje = timezone.now().date()

    # Atualiza contas vencidas automaticamente
    ContaPagar.objects.filter(
        status='PENDENTE',
        vencimento__lt=hoje
    ).update(
        status='VENCIDO'
    )

    contas = ContaPagar.objects.select_related(
        'fornecedor'
    ).order_by(
        'vencimento'
    )

    # Filtro por status
    status = request.GET.get(
        'status'
    )

    if status:

        contas = contas.filter(
            status=status
        )

    contas_pendentes = ContaPagar.objects.filter(
        status='PENDENTE'
    )

    contas_pagas = ContaPagar.objects.filter(
        status='PAGO'
    )

    contas_vencidas = ContaPagar.objects.filter(
        status='VENCIDO'
    )

    total_pendente = sum(
        conta.valor
        for conta in contas_pendentes
    )

    total_pago = sum(
        conta.valor
        for conta in contas_pagas
    )

    total_vencido = sum(
        conta.valor
        for conta in contas_vencidas
    )

    context = {

        'contas': contas,

        'status': status,

        'total_pendente': total_pendente,

        'total_pago': total_pago,

        'total_vencido': total_vencido,

        'quantidade_pendentes': contas_pendentes.count(),

        'quantidade_pagas': contas_pagas.count(),

        'quantidade_vencidas': contas_vencidas.count(),

    }

    return render(

        request,

        'accounts/contas_pagar.html',

        context

    )

# =========================================
# NOVA CONTA A PAGAR
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def nova_conta_pagar(request):

    fornecedores = Fornecedor.objects.filter(
        ativo=True
    ).order_by(
        'nome'
    )

    if request.method == 'POST':

        ContaPagar.objects.create(

            fornecedor_id=request.POST.get(
                'fornecedor'
            ),

            descricao=request.POST.get(
                'descricao'
            ),

            valor=request.POST.get(
                'valor'
            ),

            vencimento=request.POST.get(
                'vencimento'
            ),

            status='PENDENTE'

        )

        messages.success(
            request,
            'Conta cadastrada com sucesso.'
        )

        return redirect(
            'contas_pagar'
        )

    return render(

        request,

        'accounts/nova_conta_pagar.html',

        {

            'fornecedores': fornecedores

        }

    )

# =========================================
# PAGAR CONTA
# =========================================

@login_required
@perfil_required(
    'admin',
    'secretaria'
)
def pagar_conta(request, conta_id):

    conta = get_object_or_404(
        ContaPagar,
        id=conta_id
    )

    conta.status = 'PAGO'

    conta.data_pagamento = timezone.now().date()

    conta.save()

    messages.success(
        request,
        'Conta paga com sucesso.'
    )

    return redirect(
        'contas_pagar'
    )