from django.contrib.auth.base_user import BaseUserManager

# Gerenciador responsável por criar usuários e superusuários
class GerenciadorUsuario(BaseUserManager):

    # Método usado para criar usuários comuns
    def create_user(self, email, password=None, **extra_fields):
        # Valida se o email foi enviado
        if not email:
            raise ValueError('Email é obrigatório')

        # Normaliza o email
        email = self.normalize_email(email)

        # Cria a instância do usuário
        # extra_fields recebe os demais campos enviados
        usuario = self.model(
            email=email,
            **extra_fields
        )

        # Criptografa a senha
        # Nunca salva senha em texto puro
        usuario.set_password(password)


        # Salva no banco usando a conexão atual
        usuario.save(using=self._db)

        # Retorna o objeto criado
        return usuario

    # Método obrigatório para criar superusuários
    def create_superuser(self, email, password=None, **extra_fields):

        # Define acesso administrativo ao painel Django
        extra_fields.setdefault('is_staff', True)

        # Define permissões totais no sistema
        extra_fields.setdefault('is_superuser', True)

        # Reaproveita o método create_user
        return self.create_user(
            email,
            password,
            **extra_fields
        )