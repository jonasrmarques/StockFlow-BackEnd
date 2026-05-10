from django.db import models

# Classes base para autenticação customizada
from django.contrib.auth.models import (
    AbstractBaseUser, # fornece senha + autenticação
    PermissionsMixin # fornece grupos + superuser
)

# Importa o gerenciador customizado criado
from .managers import GerenciadorUsuario


# PERFIL DE ACESSO
class Perfil(models.Model):

    # Nome amigável do perfil
    # Ex: Administrador
    nome = models.CharField(max_length=200, unique=True)

    # Código técnico interno
    # Ex: admin
    codigo = models.CharField(max_length=100, unique=True)

    # Permissões específicas

    # Pode gerenciar usuários?
    pode_gerenciar_usuarios = models.BooleanField(default=False)
    # Pode movimentar estoque?
    pode_gerenciar_estoque = models.BooleanField(default=False)
    # Pode aprovar solicitações?
    pode_aprovar_solicitacoes = models.BooleanField(default=False)
    # Pode visualizar relatórios?
    pode_visualizar_relatorios = models.BooleanField(default=False)

    # Representação textual
    def __str__(self):
        return self.nome

# USUÁRIO CUSTOMIZADO
class Usuario(AbstractBaseUser, PermissionsMixin):
    # Nome completo do usuário
    nome = models.CharField(max_length=255, blank=True, null=True)

    # Email único
    # Será usado como login
    email = models.EmailField(unique=True)

    # Matrícula corporativa
    matricula = models.CharField(max_length=100, unique=True)

    celular = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True, unique=True)

    # Perfil vinculado ao usuário
    # Protege exclusão se estiver sendo usado
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    criado_em = models.DateField(auto_now_add=True)
    atualizado_em = models.DateField(auto_now_add=True)

    # Define qual gerenciador será usado
    objects = GerenciadorUsuario()

    # Campo principal de login
    USERNAME_FIELD = 'email'

    # Campos obrigatórios ao criar superuser
    REQUIRED_FIELD = [
        'nome',
        'matricula'
    ]

    def __str__(self):
        return self.email