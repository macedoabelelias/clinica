import os

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

from django.conf import settings
print(settings.BASE_DIR)

from .models import (

    Convenio,
    EvolucaoClinica,
    Paciente,
    Anamnese,
    Procedimento,
    Orcamento,
    ItemOrcamento

)

from .forms import (

    ProcedimentoForm,
    OrcamentoForm,
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

        'accounts/editar_paciente.html',

        context

    )

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

        procedimento_id = request.POST.get(

            'procedimento'

        )

        procedimento = Procedimento.objects.get(

            id=procedimento_id

        )

        EvolucaoClinica.objects.create(

            paciente=paciente,

            dente=request.POST.get('dente'),

            procedimento=procedimento,

            descricao=request.POST.get('descricao')

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
    # PROCEDIMENTOS
    # =========================================

    procedimentos = Procedimento.objects.all().order_by(

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
        # PROCEDIMENTOS
        # =========================================

        'procedimentos': procedimentos

    }

    return render(

        request,

        'accounts/odontograma.html',

        context

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

def ficha_clinica(request, id):

    paciente = Paciente.objects.get(id=id)

    evolucoes = EvolucaoClinica.objects.filter(

        paciente=paciente

    ).order_by('-criado_em')

    if request.method == 'POST':

        EvolucaoClinica.objects.create(

            paciente=paciente,

            dente=request.POST.get('dente'),

            procedimento=request.POST.get('procedimento'),

            descricao=request.POST.get('descricao'),

            materiais=request.POST.get('materiais'),

            anestesia=request.POST.get('anestesia'),

            retorno=request.POST.get('retorno') or None

        )

        return redirect(

            'ficha_clinica',
            id=paciente.id

        )

    context = {

        'paciente': paciente,
        'evolucoes': evolucoes

    }

    return render(

        request,
        'accounts/ficha_clinica.html',
        context

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

    pasta_icones = os.path.join(

        settings.BASE_DIR,
        'static',
        'img',
        'procedimentos',
        'mini'

    )

    icones = []

    if os.path.exists(pasta_icones):

        icones = sorted([

            arquivo

            for arquivo in os.listdir(pasta_icones)

            if arquivo.lower().endswith((
                '.png',
                '.svg',
                '.webp',
                '.jpg',
                '.jpeg'
            ))

        ])

    print(pasta_icones)
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
    icones = []

    if os.path.exists(pasta_icones):

        icones = os.listdir(pasta_icones)

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

        item_form = ItemOrcamentoForm(

            request.POST

        )

        if item_form.is_valid():

            item = item_form.save(

                commit=False

            )

            item.orcamento = orcamento

            item.save()

            return redirect(

                'orcamento',

                id=paciente.id

            )

    else:

        item_form = ItemOrcamentoForm()

    context = {

        'paciente': paciente,

        'orcamento': orcamento,

        'item_form': item_form

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