import re
from django.core.exceptions import ValidationError


def validate_cpf(value): # ALTERADO: DE 'validar_cpf' PARA 'validate_cpf'
    """
    Valida se o CPF é válido (função renomeada para DRF compatibility)
    """
    cpf = re.sub(r'[^0-9]', '', str(value))

    if len(cpf) != 11:
        raise ValidationError('CPF deve conter 11 dígitos.')

    # CORREÇÃO: Use re.match em vez de .test()
    if re.match(r'^(\d)\1+$', cpf):
        raise ValidationError('CPF inválido.')

    # Cálculo do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    if digito1 != int(cpf[9]):
        raise ValidationError('CPF inválido.')

    # Cálculo do segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    if digito2 != int(cpf[10]):
        raise ValidationError('CPF inválido.')

    return cpf


def formatar_cpf(cpf):
    """
    Formata o CPF para exibição: 000.000.000-00
    """
    cpf = re.sub(r'[^0-9]', '', str(cpf))
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf


def validar_categoria_cnh(value):
    """
    Valida se a categoria da CNH é E
    """
    if value and value != 'E':
        raise ValidationError('Somente categoria E é permitida.')
    return value