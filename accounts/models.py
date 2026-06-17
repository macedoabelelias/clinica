from django.db import models

from datetime import date

from django.contrib.auth.models import User


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
    # CONDIÇÕES MÉDICAS IMPORTANTES
    # =========================================

    anticoagulante = models.BooleanField(
        default=False
    )

    bisfosfonato = models.BooleanField(
        default=False
    )

    marcapasso = models.BooleanField(
        default=False
    )

    cancer = models.BooleanField(
        default=False
    )

    hipotireoidismo = models.BooleanField(
        default=False
    )

    hipertireoidismo = models.BooleanField(
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
        ('diagnostico', 'Diagnóstico'),
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
    # STATUS CLÍNICO
    # =========================================

    STATUS = [

        ('realizar', 'A Realizar'),
        ('andamento', 'Em Andamento'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado'),
        ('reavaliar', 'Reavaliar')

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
    # STATUS
    # =========================================

    status = models.CharField(

        max_length=30,

        choices=STATUS,

        default='realizar'

    )

    # =========================================
    # ÍCONE ANTIGO
    # =========================================

    icone = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )

    # =========================================
    # NOVO ARQUIVO DO ÍCONE
    # =========================================

    arquivo_icone = models.CharField(

        max_length=255,

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
    # VALOR PARTICULAR
    # =========================================

    valor_particular = models.DecimalField(

        max_digits=10,

        decimal_places=2,

        default=0

    )

    # =========================================
    # VALOR CONVÊNIO
    # =========================================

    valor_convenio = models.DecimalField(

        max_digits=10,

        decimal_places=2,

        default=0

    )

    # =========================================
    # TEMPO ESTIMADO
    # =========================================

    tempo_estimado = models.IntegerField(

        default=60,

        help_text='Tempo em minutos'

    )

    # =========================================
    # CUSTO CLÍNICO
    # =========================================

    custo_clinico = models.DecimalField(

        max_digits=10,

        decimal_places=2,

        default=0

    )

    # =========================================
    # ATIVO
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
    # META
    # =========================================

    class Meta:

        ordering = ['categoria', 'ordem', 'nome']

        verbose_name = 'Procedimento'

        verbose_name_plural = 'Procedimentos'

    # =========================================
    # STRING
    # =========================================

    def __str__(self):

        return self.nome



# =========================================
# EVOLUÇÃO CLÍNICA
# =========================================

class EvolucaoClinica(models.Model):

    STATUS_CHOICES = (

        ('existente', 'Existente'),
        ('planejado', 'Planejado'),
        ('andamento', 'Em Andamento'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado'),

    )

    paciente = models.ForeignKey(

        Paciente,

        on_delete=models.CASCADE,

        related_name='evolucoes'

    )

    dente = models.CharField(

        max_length=10,

        blank=True,

        null=True

    )

    face = models.CharField(

        max_length=20,

        blank=True,

        null=True

    )

    posicao_icone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=Procedimento.POSICOES
    )

    procedimento = models.ForeignKey(

        'Procedimento',

        on_delete=models.SET_NULL,

        null=True,

        blank=True

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='planejado'

    )

    descricao = models.TextField(

        blank=True,

        null=True

    )

    criado_em = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ['-criado_em']

    def __str__(self):

        procedimento = (
            self.procedimento.nome
            if self.procedimento
            else 'Sem procedimento'
        )

        return (
            f'{self.paciente.nome} - '
            f'{procedimento} - '
            f'{self.get_status_display()}'
        )

# =========================================
# PRONTUÁRIO CLÍNICO
# =========================================

class ProntuarioClinico(models.Model):

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='prontuarios'
    )

    titulo = models.CharField(
        max_length=200
    )

    anotacao = models.TextField()

    dente = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    procedimento = models.ForeignKey(
        Procedimento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    descricao = models.TextField(
        blank=True
    )

    materiais = models.TextField(
        blank=True
    )

    anestesia = models.CharField(
        max_length=255,
        blank=True
    )

    retorno = models.DateField(
        null=True,
        blank=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ['-criado_em']

        verbose_name = 'Prontuário Clínico'

        verbose_name_plural = 'Prontuários Clínicos'

    def __str__(self):

        if self.procedimento:

            return (
                f'{self.paciente.nome} - '
                f'{self.procedimento.nome}'
            )

        return (
            f'{self.paciente.nome} - '
            f'{self.titulo}'
        )

# =========================================
# ORÇAMENTO
# =========================================
class Orcamento(models.Model):

    # =========================================
    # PACIENTE
    # =========================================

    paciente = models.ForeignKey(

        Paciente,

        on_delete=models.CASCADE,

        related_name='orcamentos'

    )

    # =========================================
    # STATUS
    # =========================================

    STATUS_CHOICES = (

        ('rascunho', 'Rascunho'),
        ('aprovado', 'Aprovado'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='rascunho'

    )

    # =========================================
    # DESCONTO
    # =========================================

    desconto = models.DecimalField(

        max_digits=10,

        decimal_places=2,

        default=0

    )

    # =========================================
    # OBSERVAÇÕES
    # =========================================

    observacoes = models.TextField(

        blank=True,

        null=True

    )

    # =========================================
    # DATA CRIAÇÃO
    # =========================================

    criado_em = models.DateTimeField(

        auto_now_add=True

    )

    # =========================================
    # TOTAL
    # =========================================

    @property
    def total(self):

        total = sum(

            item.total

            for item in self.itens.all()

        )

        return total - self.desconto

    # =========================================
    # STRING
    # =========================================

    def __str__(self):

        return f'Orçamento #{self.id}' 

# =========================================
# CONFIGURAÇÃO DA CLÍNICA
# =========================================

class ConfiguracaoClinica(models.Model):

    nome_clinica = models.CharField(
        max_length=200
    )

    logo = models.ImageField(
        upload_to='clinica/',
        blank=True,
        null=True
    )

    cro = models.CharField(
        max_length=50,
        blank=True
    )

    cnpj = models.CharField(
        max_length=30,
        blank=True
    )

    telefone = models.CharField(
        max_length=30,
        blank=True
    )

    whatsapp = models.CharField(
        max_length=30,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    endereco = models.CharField(
        max_length=255,
        blank=True
    )

    numero = models.CharField(
        max_length=20,
        blank=True
    )

    bairro = models.CharField(
        max_length=100,
        blank=True
    )

    cidade = models.CharField(
        max_length=100,
        blank=True
    )

    estado = models.CharField(
        max_length=2,
        blank=True
    )

    cep = models.CharField(
        max_length=20,
        blank=True
    )

    observacoes_orcamento = models.TextField(
        blank=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        verbose_name = 'Configuração da Clínica'

        verbose_name_plural = (
            'Configurações da Clínica'
        )

    def __str__(self):

        return self.nome_clinica

# =========================================
# CONVÊNIOS
# =========================================

class Convenio(models.Model):

    nome = models.CharField(

        max_length=150

    )

    indice = models.DecimalField(

        max_digits=5,
        decimal_places=2,
        default=1.00

    )

    telefone = models.CharField(

        max_length=20,
        blank=True,
        null=True

    )

    observacoes = models.TextField(

        blank=True,
        null=True

    )

    ativo = models.BooleanField(

        default=True

    )

    criado_em = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return self.nome
  

# =========================================
# ITEM ORÇAMENTO
# =========================================

TIPO_LOCAL = (

    ('dente', 'Dente'),
    ('hemiarcada', 'Hemi Arcada'),
    ('geral', 'Geral'),

)


HEMI_CHOICES = (

    ('sup_dir', 'Superior Direita'),
    ('sup_esq', 'Superior Esquerda'),
    ('inf_dir', 'Inferior Direita'),
    ('inf_esq', 'Inferior Esquerda'),

)


class ItemOrcamento(models.Model):
    STATUS_CHOICES = (

        ('existente', 'Existente'),
        ('planejado', 'Planejado'),
        ('andamento', 'Em Andamento'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado'),

    )

  

    # =========================================
    # ORÇAMENTO
    # =========================================

    orcamento = models.ForeignKey(

        Orcamento,

        on_delete=models.CASCADE,

        related_name='itens'

    )


    # =========================================
    # PROCEDIMENTO
    # =========================================

    procedimento = models.ForeignKey(

        Procedimento,

        on_delete=models.SET_NULL,

        null=True

    )

    # =========================================
    # TIPO LOCAL
    # =========================================

    tipo_local = models.CharField(

        max_length=20,

        choices=TIPO_LOCAL,

        default='dente'

    )

    # =========================================
    # DENTE
    # =========================================

    dente = models.CharField(

        max_length=10,

        blank=True,

        null=True

    )

    # =========================================
    # FACE
    # =========================================

    face = models.CharField(

        max_length=10,

        blank=True,

        null=True

    )

    posicao_icone = models.CharField(

        max_length=20,

        blank=True,

        null=True,

        choices=Procedimento.POSICOES

    )

    # =========================================
    # HEMI ARCADA
    # =========================================

    hemi_arcada = models.CharField(

        max_length=20,

        choices=HEMI_CHOICES,

        blank=True,

        null=True

    )


    # =========================================
    # QUANTIDADE
    # =========================================

    quantidade = models.IntegerField(

        default=1

    )

    # =========================================
    # VALOR
    # =========================================

    valor_unitario = models.DecimalField(

        max_digits=10,

        decimal_places=2,

        default=0

    )

    # =========================================
    # STATUS
    # =========================================

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='planejado'

    )

    # =========================================
    # TOTAL
    # =========================================

    @property
    def total(self):

        return self.quantidade * self.valor_unitario

    # =========================================
    # STRING
    # =========================================

    def __str__(self):

        procedimento = (
            self.procedimento.nome
            if self.procedimento
            else 'Procedimento'
        )

        return f'{procedimento} - {self.orcamento.paciente.nome}'
    
# =========================================
# ANEXOS PACIENTE
# =========================================

class AnexoPaciente(models.Model):

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='anexos'
    )

    TIPO_CHOICES = (

        ('foto', 'Foto Clínica'),
        ('radiografia', 'Radiografia'),
        ('tomografia', 'Tomografia'),
        ('documento', 'Documento'),
        ('exame', 'Exame')

    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='documento'
    )

    descricao = models.CharField(
        max_length=200
    )

    arquivo = models.FileField(
        upload_to='anexos_pacientes/'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ['-criado_em']

    def __str__(self):

        return (
            f'{self.paciente.nome} - '
            f'{self.descricao}'
        )
    
# =========================================
# TEMPLATES DOCUMENTOS
# =========================================

class TemplateDocumento(models.Model):

    TIPO_CHOICES = (

        ('atestado', 'Atestado Odontológico'),
        ('declaracao', 'Declaração de Comparecimento'),
        ('receita', 'Receituário Simples'),
        ('controle_especial', 'Receituário Controle Especial'),
        ('exames', 'Solicitação de Exames'),
        ('encaminhamento', 'Encaminhamento'),
        ('relatorio', 'Relatório Odontológico'),
        ('alta', 'Termo de Alta'),
        ('consentimento', 'Termo de Consentimento'),
        ('contrato', 'Contrato'),
        ('livre', 'Documento Livre'),

    )

    nome = models.CharField(
        max_length=200
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES
    )

    conteudo = models.TextField()

    ativo = models.BooleanField(
        default=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.nome
    
# =========================================
# DOCUMENTOS CLÍNICOS
# =========================================

class DocumentoClinico(models.Model):

    STATUS = (

        ('rascunho', 'Rascunho'),
        ('finalizado', 'Finalizado'),

    )

    TIPOS = (

        ('atestado', 'Atestado Odontológico'),

        ('declaracao', 'Declaração de Comparecimento'),

        ('receita', 'Receituário Simples'),

        ('controle_especial', 'Receituário Controle Especial'),

        ('exames', 'Solicitação de Exames'),

        ('encaminhamento', 'Encaminhamento'),

        ('relatorio', 'Relatório Odontológico'),

        ('alta', 'Termo de Alta'),

        ('consentimento', 'Termo de Consentimento'),

        ('contrato', 'Contrato'),

        ('personalizado', 'Documento Personalizado'),

    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='documentos'
    )

    template = models.ForeignKey(
        TemplateDocumento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    titulo = models.CharField(
        max_length=255
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPOS,
        default='personalizado'
    )

    conteudo = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='rascunho'
    )

    pdf = models.FileField(
        upload_to='documentos/',
        blank=True,
        null=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ['-criado_em']

        verbose_name = 'Documento Clínico'

        verbose_name_plural = 'Documentos Clínicos'

    def __str__(self):

        return f'{self.titulo} - {self.paciente.nome}'
    
   
# =========================================
# MEDICAMENTOS
# =========================================

class Medicamento(models.Model):

    CATEGORIAS = (

        ('antibiotico', 'Antibiótico'),
        ('analgesico', 'Analgésico'),
        ('antiinflamatorio', 'Anti-inflamatório'),
        ('antisseptico', 'Antisséptico'),
        ('outro', 'Outro'),

    )

    nome = models.CharField(
        max_length=200
    )

    concentracao = models.CharField(
        max_length=100,
        blank=True
    )

    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIAS,
        default='outro'
    )

    ativo = models.BooleanField(
        default=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        if self.concentracao:

            return (
                f'{self.nome} '
                f'{self.concentracao}'
            )

        return self.nome


# =========================================
# RECEITAS
# =========================================

class Receita(models.Model):


    paciente = models.ForeignKey(

        Paciente,

        on_delete=models.CASCADE,

        related_name='receitas'

    )

    medicamento = models.CharField(

        max_length=300

    )

    titulo = models.CharField(

        max_length=200,

        default='Receituário'

    )

    quantidade = models.CharField(

        max_length=100

    )

    posologia = models.TextField()

    observacoes = models.TextField(

        blank=True,

        null=True

    )

    TIPO_RECEITA = (

        ('simples', 'Receituário Simples'),

        ('controle', 'Receita de Controle Especial'),

    )

    tipo_receita = models.CharField(

        max_length=20,

        choices=TIPO_RECEITA,

        default='simples'

    )

    status = models.CharField(

        max_length=20,

        default='ativo'

    )

    criado_em = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ['-criado_em']

    def __str__(self):

        return (
            f'{self.paciente.nome} - '
            f'{self.medicamento}'
        )
    

# =========================================
# MODELOS DE RECEITA
# =========================================

class ModeloReceita(models.Model):

    nome = models.CharField(
        max_length=200
    )

    medicamento = models.CharField(
        max_length=255
    )

    quantidade = models.CharField(
        max_length=100,
        blank=True
    )

    posologia = models.TextField()

    ativo = models.BooleanField(
        default=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        verbose_name = 'Modelo de Receita'

        verbose_name_plural = 'Modelos de Receita'

        ordering = ['nome']

    def __str__(self):

        return self.nome
    

# =========================================
# EXAMES
# =========================================

class Exame(models.Model):

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='exames'
    )

    nome = models.CharField(
        max_length=200
    )

    data_exame = models.DateField(
        blank=True,
        null=True
    )

    arquivo = models.FileField(
        upload_to='exames/',
        blank=True,
        null=True
    )

    observacoes = models.TextField(
        blank=True,
        null=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ['-criado_em']

        verbose_name = 'Exame'

        verbose_name_plural = 'Exames'

    def __str__(self):

        return (
            f'{self.paciente.nome} - '
            f'{self.nome}'
        )
    
# =========================================
# SOLICITAÇÃO DE EXAMES
# =========================================

class SolicitacaoExame(models.Model):

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='solicitacoes_exames'
    )

    titulo = models.CharField(
        max_length=200
    )

    exames_solicitados = models.TextField()

    observacoes = models.TextField(
        blank=True,
        null=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ['-criado_em']

        verbose_name = 'Solicitação de Exame'

        verbose_name_plural = 'Solicitações de Exames'

    def __str__(self):

        return (
            f'{self.paciente.nome} - '
            f'{self.titulo}'
        )

# =========================================
# PERFIL DE USUÁRIO
# =========================================

class PerfilUsuario(models.Model):

    ADMIN = 'admin'
    GESTOR = 'gestor'
    DENTISTA = 'dentista'
    SECRETARIA = 'secretaria'
    ACD = 'acd'
    CONTABILIDADE = 'contabilidade'
    MARKETING = 'marketing'
    AUDITORIA = 'auditoria'

    TIPOS_USUARIO = [

        (ADMIN, 'Administrador'),

        (GESTOR, 'Gestor'),

        (DENTISTA, 'Dentista'),

        (SECRETARIA, 'Secretária'),

        (ACD, 'Auxiliar de Saúde Bucal'),

        (CONTABILIDADE, 'Contabilidade'),

        (MARKETING, 'Marketing'),

        (AUDITORIA, 'Auditoria'),

    ]

    usuario = models.OneToOneField(

        User,

        on_delete=models.CASCADE,

        related_name='perfil'

    )

    tipo_usuario = models.CharField(

        max_length=30,

        choices=TIPOS_USUARIO,

        default=SECRETARIA

    )

    # Dados profissionais

    cro = models.CharField(

        max_length=20,

        blank=True,

        null=True

    )

    especialidade = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )

    telefone = models.CharField(

        max_length=20,

        blank=True,

        null=True

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

    data_nascimento = models.DateField(
        blank=True,
        null=True
    )

    sexo = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    foto = models.ImageField(
        upload_to='usuarios/fotos/',
        blank=True,
        null=True
    )

    assinatura = models.ImageField(
        upload_to='usuarios/assinaturas/',
        blank=True,
        null=True
    )

    cro_uf = models.CharField(
        max_length=2,
        blank=True,
        null=True
    )

    cep = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    logradouro = models.CharField(
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

    uf = models.CharField(
        max_length=2,
        blank=True,
        null=True
    )

    celular = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # Controle

    ativo = models.BooleanField(

        default=True

    )

    somente_leitura = models.BooleanField(

        default=False

    )

    criado_em = models.DateTimeField(

        auto_now_add=True

    )

    atualizado_em = models.DateTimeField(

        auto_now=True

    )

    def __str__(self):

        nome = self.usuario.get_full_name()

        if nome:

            return f'{nome} ({self.get_tipo_usuario_display()})'

        return f'{self.usuario.username} ({self.get_tipo_usuario_display()})'    

# =========================================
# FORNECEDORES
# =========================================

class Fornecedor(models.Model):

    nome = models.CharField(
        max_length=200
    )

    razao_social = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    cnpj = models.CharField(
        max_length=18,
        blank=True,
        null=True
    )

    contato = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    celular = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    # Endereço

    cep = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    logradouro = models.CharField(
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

    uf = models.CharField(
        max_length=2,
        blank=True,
        null=True
    )

    # Controle

    ativo = models.BooleanField(
        default=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.nome
