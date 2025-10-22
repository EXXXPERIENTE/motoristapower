# C:\APPY\MotoristaPower\drivers\serializers.py

# A importação agora aponta corretamente para o arquivo cpf_validators.py
from .validators.cpf_validators import validate_cpf
from rest_framework import serializers
from .models import Motorista


class MotoristaSerializer(serializers.ModelSerializer):
    # Aplica o validador à chave 'cpf'. Isso garante que o CPF será validado
    # usando a função validate_cpf sempre que um objeto for criado ou atualizado.
    cpf = serializers.CharField(validators=[validate_cpf])

    class Meta:
        # Define o modelo que este serializador vai manipular
        model = Motorista
        # Inclui todos os campos do modelo (nome, cpf, data_nascimento, created_at)
        fields = '__all__'
        # Se você quiser que o CPF seja somente leitura após a criação (recomendado),
        # adicione 'cpf' aqui:
        # read_only_fields = ('cpf',)