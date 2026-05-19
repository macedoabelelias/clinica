from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .models import Paciente


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

    return render(

        request,

        'accounts/pacientes.html',

        {

            'pacientes': pacientes

        }

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

        # DADOS

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

    return render(

        request,

        'accounts/editar_paciente.html',

        {

            'paciente': paciente

        }

    )

# =========================================
# ODONTOGRAMA
# =========================================

@login_required
def odontograma(request, id):

    paciente = get_object_or_404(Paciente, id=id)

    context = {

        'paciente': paciente,

        # PERMANENTES
        'superiores': [
            '18','17','16','15','14','13','12','11',
            '21','22','23','24','25','26','27','28'
        ],

        'inferiores': [
            '48','47','46','45','44','43','42','41',
            '31','32','33','34','35','36','37','38'
        ],

        # DECÍDUOS
        'dec_superiores': [
            '55','54','53','52','51',
            '61','62','63','64','65'
        ],

        'dec_inferiores': [
            '85','84','83','82','81',
            '71','72','73','74','75'
        ],

    }

    return render(
        request,
        'accounts/odontograma.html',
        context
    )