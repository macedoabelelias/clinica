from django.db import models

from datetime import date


# =========================================
# PACIENTES
# =========================================

class Paciente(models.Model):

    # =========================================
    # DADOS PESSOAIS
    # =========================================

    foto = models.ImageField(
        upload_to='pacientes/',
        blank=True,
        null=True
    )

    nome = models.CharField(
        max_length=200
    )

    cpf = models.CharField(
        max_length=14,
        blank=True,
        null=True
    )

    rg = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    nascimento = models.DateField(
        blank=True,
        null=True
    )

    genero = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    estado_civil = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    profissao = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # =========================================
    # CONTATO
    # =========================================

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    # =========================================
    # ENDEREÇO
    # =========================================

    cep = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    endereco = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    numero = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    complemento = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    bairro = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    cidade = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    estado = models.CharField(
        max_length=2,
        blank=True,
        null=True
    )

    # =========================================
    # CLÍNICO
    # =========================================

    convenio = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    carteirinha = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    alergias = models.TextField(
        blank=True,
        null=True
    )

    medicamentos = models.TextField(
        blank=True,
        null=True
    )

    observacoes = models.TextField(
        blank=True,
        null=True
    )

    # =========================================
    # RESPONSÁVEL
    # =========================================

    responsavel = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    cpf_responsavel = models.CharField(
        max_length=14,
        blank=True,
        null=True
    )

    telefone_responsavel = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # =========================================
    # CONTROLE
    # =========================================

    ativo = models.BooleanField(
        default=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    # =========================================
    # IDADE AUTOMÁTICA
    # =========================================

    @property
    def idade(self):

        if self.nascimento:

            hoje = date.today()

            return (

                hoje.year
                - self.nascimento.year
                - (
                    (
                        hoje.month,
                        hoje.day
                    ) < (
                        self.nascimento.month,
                        self.nascimento.day
                    )
                )

            )

        return None

    # =========================================
    # STATUS
    # =========================================

    @property
    def status(self):

        return 'Ativo' if self.ativo else 'Inativo'

    # =========================================
    # STRING
    # =========================================

    def __str__(self):

        return self.nome
    

class Anamnese(models.Model):

    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE
    )

    # =========================================
    # QUEIXA PRINCIPAL
    # =========================================

    queixa_principal = models.TextField(
        blank=True
    )

    # =========================================
    # HISTÓRIA MÉDICA
    # =========================================

    hipertenso = models.BooleanField(
        default=False
    )

    diabetico = models.BooleanField(
        default=False
    )

    cardiopatia = models.BooleanField(
        default=False
    )

    asma = models.BooleanField(
        default=False
    )

    bronquite = models.BooleanField(
        default=False
    )

    anemia = models.BooleanField(
        default=False
    )

    hepatite = models.BooleanField(
        default=False
    )

    rinite = models.BooleanField(
        default=False
    )

    sinusite = models.BooleanField(
        default=False
    )

    problema_renal = models.BooleanField(
        default=False
    )

    sangramento_excessivo = models.BooleanField(
        default=False
    )    

    alergico = models.BooleanField(
        default=False
    )

    alergias = models.TextField(
        blank=True
    )

    fumante = models.BooleanField(
        default=False
    )

    gravida = models.BooleanField(
        default=False
    )

    historico_medico = models.TextField(
        blank=True
    )

    # =========================================
    # MEDICAMENTOS
    # =========================================

    usa_medicamento = models.BooleanField(
        default=False
    )

    medicamentos = models.TextField(
        blank=True
    )

    antibioticos = models.TextField(
        blank=True
    )

    antiinflamatorios = models.TextField(
        blank=True
    )

    analgesicos = models.TextField(
        blank=True
    )

    # =========================================
    # CIRURGIAS / HOSPITALIZAÇÃO
    # =========================================

    cirurgia = models.BooleanField(
        default=False
    )

    cirurgias = models.TextField(
        blank=True
    )

    hospitalizado = models.BooleanField(
        default=False
    )

    hospitalizacao = models.TextField(
        blank=True
    )

    transfusao_sangue = models.BooleanField(
        default=False
    )

    # =========================================
    # HISTÓRIA ODONTOLÓGICA
    # =========================================

    primeira_consulta = models.BooleanField(
        default=False
    )

    ultima_consulta = models.DateField(
        null=True,
        blank=True
    )

    experiencia_odontologica = models.TextField(
        blank=True
    )

    abandono_tratamento = models.BooleanField(
        default=False
    )

    medo_dentista = models.BooleanField(
        default=False
    )

    anestesia_reacao = models.TextField(
        blank=True
    )

    sangramento_gengival = models.BooleanField(
        default=False
    )

    sensibilidade = models.BooleanField(
        default=False
    )

    dor_mastigar = models.BooleanField(
        default=False
    )

    # =========================================
    # HIGIENE ORAL
    # =========================================

    frequencia_escovacao = models.CharField(
        max_length=100,
        blank=True
    )

    usa_fio_dental = models.BooleanField(
        default=False
    )

    usa_enxaguante = models.BooleanField(
        default=False
    )

    escova_lingua = models.BooleanField(
        default=False
    )

    # =========================================
    # HÁBITOS
    # =========================================

    bruxismo = models.BooleanField(
        default=False
    )

    ronco = models.BooleanField(
        default=False
    )

    respiracao_bucal = models.BooleanField(
        default=False
    )

    roer_unhas = models.BooleanField(
        default=False
    )

    morde_objetos = models.BooleanField(
        default=False
    )

    chupeta = models.BooleanField(
        default=False
    )

    succao_dedo = models.BooleanField(
        default=False
    )

    baba_travesseiro = models.BooleanField(
        default=False
    )

    dorme_boca_aberta = models.BooleanField(
        default=False
    )

    morde_labios = models.BooleanField(
        default=False
    )

    # =========================================
    # HÁBITOS ALIMENTARES
    # =========================================

    belisca_refeicoes = models.BooleanField(
        default=False
    )

    alimentacao_cariogenica = models.BooleanField(
        default=False
    )

    tipo_alimentacao = models.CharField(
        max_length=100,
        blank=True
    )

    # =========================================
    # PERFIL COMPORTAMENTAL
    # =========================================

    ansioso = models.BooleanField(
        default=False
    )

    agitado = models.BooleanField(
        default=False
    )

    calmo = models.BooleanField(
        default=False
    )

    comunicativo = models.BooleanField(
        default=False
    )

    retraido = models.BooleanField(
        default=False
    )
    introvertido = models.BooleanField(
        default=False
    )

    extrovertido = models.BooleanField(
        default=False
    )

    # =========================================
    # OBSERVAÇÕES
    # =========================================

    observacoes = models.TextField(
        blank=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f'Anamnese - {self.paciente.nome}'
    
# =========================================
# PROCEDIMENTOS
# =========================================

class Procedimento(models.Model):

    # =========================================
    # CATEGORIAS
    # =========================================

    CATEGORIAS = [

        ('dentistica', 'Dentística'),
        ('endodontia', 'Endodontia'),
        ('periodontia', 'Periodontia'),
        ('cirurgia', 'Cirurgia'),
        ('protese', 'Prótese'),
        ('implantodontia', 'Implantodontia'),
        ('ortodontia', 'Ortodontia'),
        ('geral', 'Geral')

    ]

    # =========================================
    # TIPOS
    # =========================================

    TIPOS = [

        ('dente', 'Por Dente'),
        ('hemiarcada', 'Hemi-Arcada'),
        ('geral', 'Geral'),
        ('cirurgia', 'Cirurgia')

    ]

    # =========================================
    # POSIÇÕES
    # =========================================

    POSICOES = [

        ('coroa', 'Coroa'),
        ('raiz', 'Raiz'),
        ('oclusal', 'Oclusal'),
        ('vestibular', 'Vestibular'),
        ('lingual', 'Lingual'),
        ('centro', 'Centro')

    ]

    # =========================================
    # NOME
    # =========================================

    nome = models.CharField(

        max_length=255

    )

    # =========================================
    # CATEGORIA
    # =========================================

    categoria = models.CharField(

        max_length=100,

        choices=CATEGORIAS,

        default='geral'

    )

    # =========================================
    # TIPO
    # =========================================

    tipo = models.CharField(

        max_length=50,

        choices=TIPOS,

        default='dente'

    )

    # =========================================
    # COR
    # =========================================

    cor = models.CharField(

        max_length=20,

        default='#2563eb'

    )

    # =========================================
    # ÍCONE
    # =========================================

    icone = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )

    # =========================================
    # POSIÇÃO DO ÍCONE
    # =========================================

    posicao_icone = models.CharField(

        max_length=30,

        choices=POSICOES,

        default='centro'

    )

    # =========================================
    # STATUS
    # =========================================

    ativo = models.BooleanField(

        default=True

    )

    # =========================================
    # ORDEM
    # =========================================

    ordem = models.IntegerField(

        default=0

    )

    # =========================================
    # DATA
    # =========================================

    criado_em = models.DateTimeField(

        auto_now_add=True

    )

    # =========================================
    # STRING
    # =========================================

    def __str__(self):

        return self.nome

# =========================================
# EVOLUÇÃO CLÍNICA
# =========================================

class EvolucaoClinica(models.Model):

    paciente = models.ForeignKey(

        Paciente,

        on_delete=models.CASCADE,

        related_name='evolucoes'

    )

    # =========================================
    # DENTE
    # =========================================

    dente = models.CharField(

        max_length=10,

        blank=True

    )

    # =========================================
    # PROCEDIMENTO
    # =========================================

    procedimento = models.ForeignKey(

        Procedimento,

        on_delete=models.SET_NULL,

        null=True,

        blank=True

    )

    # =========================================
    # DESCRIÇÃO
    # =========================================

    descricao = models.TextField(

        blank=True

    )

    # =========================================
    # MATERIAIS
    # =========================================

    materiais = models.TextField(

        blank=True

    )

    # =========================================
    # ANESTESIA
    # =========================================

    anestesia = models.CharField(

        max_length=255,

        blank=True

    )

    # =========================================
    # RETORNO
    # =========================================

    retorno = models.DateField(

        null=True,

        blank=True

    )

    # =========================================
    # DATA
    # =========================================

    criado_em = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        procedimento = (
            self.procedimento.nome
            if self.procedimento
            else 'Sem procedimento'
        )

        return f'{self.paciente.nome} - {procedimento}'
    
   