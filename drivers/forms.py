from django import forms
from .models import Motorista
from datetime import date
import re


class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista
        # 'foto' agora existe no model e é incluído aqui.
        fields = [
            'nome_completo', 'cpf', 'data_nascimento', 'email', 'telefone',
            'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
            'cnh_numero', 'cnh_categoria', 'cnh_validade', 'cnh_emissao',
            'status', 'observacoes', 'foto',
        ]
        # 'salario' é explicitamente excluído do formulário,
        # garantindo que ele não apareça.
        exclude = ('salario',)

        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cnh_validade': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cnh_emissao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'nome_completo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nome completo do motorista'}),
            # maxlength 14 para o formato 000.000.000-00 (máscara)
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00', 'maxlength': 14}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, Avenida, etc.'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartamento, Bloco, etc.'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da cidade'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'cnh_numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número da CNH'}),
            'cnh_categoria': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    # Validação do CPF: Garante que o formato de 14 caracteres seja respeitado
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Verifica se o CPF está no formato 000.000.000-00 (14 caracteres)
            if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
                raise forms.ValidationError('CPF deve estar no formato: 000.000.000-00 (14 caracteres)')
            # Retorna o valor formatado (14 caracteres) para o banco de dados.
            return cpf
        return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone and not re.match(r'^\(\d{2}\)\s?\d{4,5}-\d{4}$', telefone):
            raise forms.ValidationError('Telefone deve estar no formato: (00) 00000-0000 ou (00) 0000-0000')
        return telefone

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento:
            hoje = date.today()
            idade = hoje.year - data_nascimento.year - (
                    (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

            if idade < 18:
                raise forms.ValidationError('Motorista deve ter pelo menos 18 anos.')

        return data_nascimento

    def clean_cnh_validade(self):
        cnh_validade = self.cleaned_data.get('cnh_validade')
        if cnh_validade:
            if cnh_validade < date.today():
                raise forms.ValidationError('A validade da CNH não pode ser uma data passada.')
        return cnh_validade

    def clean(self):
        cleaned_data = super().clean()
        cnh_emissao = cleaned_data.get('cnh_emissao')
        cnh_validade = cleaned_data.get('cnh_validade')

        if cnh_emissao and cnh_validade:
            if cnh_emissao >= cnh_validade:
                self.add_error('cnh_emissao', 'Data de emissão deve ser anterior à data de validade.')
                self.add_error('cnh_validade', 'Data de validade deve ser posterior à data de emissão.')

        return cleaned_data