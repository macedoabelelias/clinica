from django.db import models


# =========================================
# PROFISSIONAIS
# =========================================

class Profissional(models.Model):

    nome = models.CharField(
        max_length=200
    )

    especialidade = models.CharField(
        max_length=100,
        blank=True
    )

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    cor_agenda = models.CharField(
        max_length=20,
        default='#2563eb'
    )

    ativo = models.BooleanField(
        default=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ['nome']

        verbose_name = 'Profissional'

        verbose_name_plural = 'Profissionais'

    def __str__(self):

        return self.nome
from accounts.models import Paciente, Procedimento


# =========================================
# AGENDAMENTOS
# =========================================

class Agendamento(models.Model):

    STATUS_CHOICES = (

        ('agendado', 'Agendado'),
        ('confirmado', 'Confirmado'),
        ('atendimento', 'Em Atendimento'),
        ('finalizado', 'Finalizado'),
        ('faltou', 'Faltou'),
        ('cancelado', 'Cancelado'),

    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )

    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name='agendamentos'
    )

    procedimento = models.ForeignKey(
        Procedimento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    data = models.DateField()

    hora_inicio = models.TimeField()

    duracao = models.IntegerField(
        default=60,
        help_text='Duração em minutos'
    )

    observacoes = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='agendado'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            'data',
            'hora_inicio'
        ]

        verbose_name = 'Agendamento'

        verbose_name_plural = 'Agendamentos'

    def __str__(self):

        return (
            f'{self.paciente.nome} '
            f'- {self.data}'
        )
