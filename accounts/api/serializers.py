from rest_framework import serializers
from accounts.models import Usuario, Perfil

class PerfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perfil
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    
    perfil = PerfilSerializer(read_only=True)

    class Meta:
        model = Usuario
        
        exclude = [
            'password'
        ]

class CriarUsuarioSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = Usuario
        fields = [
            'nome',
            'email',
            'password',
            'matricula',
            'celular',
            'cpf',
            'perfil',
        ]


    def create(self, validated_data):

        senha = validated_data.pop('password')

        usuario = Usuario.objects.create_user(
            password=senha,
            **validated_data
        )

        return usuario

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )
