# C:\APPY\MotoristaPower\drivers\validators\cpf_validators.py
# NENHUMA LINHA DE IMPORTAÇÃO DEVE SER COLOCADA AQUI ALÉM DESTAS ABAIXO.

import re
from django.core.exceptions import ValidationError
from rest_framework.serializers import ValidationError as DRFValidationError


def clean_cpf_numbers(cpf: str) -> str:
    """Remove caracteres não numéricos do CPF."""
    # Garante que, se o CPF for None, retorne uma string vazia para o re.sub funcionar
    return re.sub(r'\D', '', cpf or '')


def calc_cpf_digit(nums):
    """Calcula um dígito verificador do CPF."""
    # O range gera os pesos (10 a 2 ou 11 a 2)
    s = sum(int(n) * w for n, w in zip(nums, range(len(nums) + 1, 1, -1)))
    r = (s * 10) % 11
    return r if r < 10 else 0


def validate_cpf(value, is_drf_validation=False):
    """
    Valida a estrutura e os dígitos verificadores do CPF.
    Aceita um valor opcional para usar ValidationError do DRF.
    """
    cpf = clean_cpf_numbers(value)
    # Define a classe de erro a ser usada (Django padrão ou DRF)
    ErrorClass = DRFValidationError if is_drf_validation else ValidationError

    if len(cpf) != 11:
        raise ErrorClass('CPF deve ter 11 dígitos.')

    # 1. Checagem de CPFs com todos os dígitos iguais (ex: 111.111.111-11)
    if cpf == cpf[0] * 11:
        raise ErrorClass('CPF inválido: Dígitos sequenciais não são permitidos.')

    # 2. Cálculo do primeiro dígito verificador (usando os primeiros 9 dígitos)
    first_expected = calc_cpf_digit(cpf[:9])

    # 3. Cálculo do segundo dígito verificador (usando os 9 + o primeiro verificado)
    second_expected = calc_cpf_digit(cpf[:9] + str(first_expected))

    # 4. Comparação
    if int(cpf[9]) != first_expected or int(cpf[10]) != second_expected:
        raise ErrorClass('CPF inválido: Dígitos verificadores incorretos.')

    # ✅ Se passou, retorna o valor original (com pontuações, se houver)
    return value