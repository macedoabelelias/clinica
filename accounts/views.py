import os

from django.conf import settings

from django.http import HttpResponse

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
from reportlab.lib.styles import getSampleStyleSheet

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
    ConfiguracaoClinica
)

from .forms import (
    ProcedimentoForm,
    ItemOrcamentoForm,
    ConvenioForm
)

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
            )

        )

        return redirect('pacientes')

    # =========================================
    # LISTAGEM
    # =========================================

    pacientes = Paciente.objects.all().order_by('-id')

    convenios = Convenio.objects.filter(
        ativo=True
    ).order_by('nome')

    context = {

        'pacientes': pacientes,
        'convenios': convenios

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

    return render(

        request,

        'accounts/perfil.html',

        {

            'paciente': paciente

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

            foto=request.FILES.get('foto'),

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
# ODONTOGRAMA
# =========================================

@login_required(login_url='/')
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

    return render(

        request,

        'accounts/odontograma.html',

        context

    )

# =========================================
# PROCEDIMENTO GERAL
# =========================================

@login_required(login_url='/')
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
            'queixa_principal'
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
            'alergias'
        )

        anamnese.fumante = 'fumante' in request.POST
        anamnese.gravida = 'gravida' in request.POST

        anamnese.historico_medico = request.POST.get(
            'historico_medico'
        )

        # =========================================
        # MEDICAMENTOS
        # =========================================

        anamnese.usa_medicamento = 'usa_medicamento' in request.POST

        anamnese.medicamentos = request.POST.get(
            'medicamentos'
        )

        anamnese.antibioticos = request.POST.get(
            'antibioticos'
        )

        anamnese.antiinflamatorios = request.POST.get(
            'antiinflamatorios'
        )

        anamnese.analgesicos = request.POST.get(
            'analgesicos'
        )

        # =========================================
        # CIRURGIAS
        # =========================================

        anamnese.cirurgia = 'cirurgia' in request.POST

        anamnese.cirurgias = request.POST.get(
            'cirurgias'
        )

        anamnese.hospitalizado = 'hospitalizado' in request.POST

        anamnese.hospitalizacao = request.POST.get(
            'hospitalizacao'
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
            'experiencia_odontologica'
        )

        anamnese.abandono_tratamento = (
            'abandono_tratamento' in request.POST
        )

        anamnese.medo_dentista = (
            'medo_dentista' in request.POST
        )

        anamnese.anestesia_reacao = request.POST.get(
            'anestesia_reacao'
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
            'frequencia_escovacao'
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
            'tipo_alimentacao'
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

        anamnese.retraido = 'retraido' in request.POST
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
            'observacoes'
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

        # RESUMO CLÍNICO

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

    elementos.append(Spacer(1, 8))

    # Linha abaixo do título

    elementos.append(
        HRFlowable(
            width="100%",
            thickness=1.2,
            color=colors.HexColor('#1e40af')
        )
    )

    elementos.append(Spacer(1, 12))

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

    if hasattr(paciente, 'cpf'):

        elementos.append(
            Paragraph(
                f'<b>CPF:</b> {paciente.cpf}',
                styles['Normal']
            )
        )

    telefone = paciente.telefone or 'Não informado'
    whatsapp = paciente.whatsapp or 'Não informado'
    email = paciente.email or 'Não informado'

    elementos.append(
        Paragraph(
            f'<b>Telefone:</b> {telefone}',
            styles['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f'<b>WhatsApp:</b> {whatsapp}',
            styles['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f'<b>E-mail:</b> {email}',
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
    # ASSINATURAS
    # =========================================

    elementos.append(Spacer(1, 50))

    elementos.append(
        Paragraph(
            '________________________________________________________',
            styles['Normal']
        )
    )

    elementos.append(
        Paragraph(
            'Cirurgião-Dentista Responsável',
            styles['Normal']
        )
    )

    elementos.append(Spacer(1, 40))

    elementos.append(
        Paragraph(
            '________________________________________________________',
            styles['Normal']
        )
    )

    elementos.append(
        Paragraph(
            'Paciente / Responsável Legal',
            styles['Normal']
        )
    )

    # =========================================
    # RODAPÉ
    # =========================================

    elementos.append(Spacer(1, 30))

    elementos.append(
        Paragraph(
            '''
            <para align="center">
            Documento gerado automaticamente pelo
            <b>AM Systems Odontologia</b>
            </para>
            ''',
            styles['Italic']
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

        print(template_id)

        conteudo = request.POST.get(
            'conteudo'
        )

        if template_id:

            template = TemplateDocumento.objects.get(
                id=template_id
            )

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

            

        documento = DocumentoClinico.objects.create(

            paciente=paciente,

            titulo=request.POST.get(
                'titulo'
            ),

            conteudo=conteudo

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