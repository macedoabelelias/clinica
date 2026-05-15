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