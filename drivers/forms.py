from django import forms
from .models import Motorista
from datetime import date
import re
from .validators import validar_cpf, validar_categoria_cnh


class MotoristaForm(forms.ModelForm):
    # Campo CPF com validação customizada
    cpf = forms.CharField(
        max_length=14,
        validators=[validar_cpf],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00',
            'data-mask': '000.000.000-00'
        })
    )

    # Campos de data sem type='date' para permitir digitação manual
    data_nascimento = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'DD/MM/AAAA',
            'data-mask': '00/00/0000'
        })
    )

    data_admissao = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'DD/MM/AAAA',
            'data-mask': '00/00/0000'
        })
    )

    class Meta:
        model = Motorista
        fields = [
            'foto',
            'nome_completo', 'cpf', 'data_nascimento', 'email', 'telefone',
            'cidade', 'estado', 'cnh_numero', 'cnh_categoria',
            'data_admissao', 'salario', 'status'
        ]
        widgets = {
            'foto': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'nome_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'telefone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000', 'data-mask': '(00) 00000-0000'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'cnh_numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número da CNH'}),
            'cnh_categoria': forms.Select(attrs={'class': 'form-control'}),
            'salario': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': '0,00'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_completo': 'Nome Completo *',
            'cpf': 'CPF *',
            'data_nascimento': 'Data de Nascimento *',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'cnh_numero': 'Número da CNH',
            'cnh_categoria': 'Categoria da CNH *',
            'data_admissao': 'Data de Admissão',
            'salario': 'Salário (R$)',
            'status': 'Status',
            'foto': 'Foto do Motorista',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

        # Força a categoria E como única opção
        self.fields['cnh_categoria'].choices = [('', 'Selecione...'), ('E', 'E')]
        self.fields['cnh_categoria'].required = True

    def clean_cpf(self):
        """
        Valida se o CPF já está cadastrado
        """
        cpf = self.cleaned_data.get('cpf')

        if cpf:
            # Limpa o CPF
            cpf_limpo = re.sub(r'[^0-9]', '', cpf)

            # Verifica se já existe outro motorista com este CPF
            motoristas_com_mesmo_cpf = Motorista.objects.filter(cpf__icontains=cpf_limpo)

            # Se estiver editando, exclui o próprio registro da verificação
            if self.instance and self.instance.pk:
                motoristas_com_mesmo_cpf = motoristas_com_mesmo_cpf.exclude(pk=self.instance.pk)

            if motoristas_com_mesmo_cpf.exists():
                raise forms.ValidationError('Este CPF já está cadastrado no sistema.')

        return cpf

    def clean_cnh_categoria(self):
        """
        Valida se a categoria da CNH é E
        """
        categoria = self.cleaned_data.get('cnh_categoria')
        if categoria and categoria != 'E':
            raise forms.ValidationError('Somente categoria E é permitida.')
        return categoria

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento:
            # Converte string para date se necessário
            if isinstance(data_nascimento, str):
                try:
                    from datetime import datetime
                    data_nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y').date()
                except ValueError:
                    raise forms.ValidationError("Formato de data inválido. Use DD/MM/AAAA.")

            idade = (date.today() - data_nascimento).days // 365
            if idade < 18:
                raise forms.ValidationError("O motorista deve ter pelo menos 18 anos.")
            if idade > 100:
                raise forms.ValidationError("Idade inválida.")
        return data_nascimento

    def clean_data_admissao(self):
        data_admissao = self.cleaned_data.get('data_admissao')
        if data_admissao and isinstance(data_admissao, str):
            try:
                from datetime import datetime
                data_admissao = datetime.strptime(data_admissao, '%d/%m/%Y').date()
            except ValueError:
                raise forms.ValidationError("Formato de data inválido. Use DD/MM/AAAA.")
        return data_admissao

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto:
            if foto.size > 5 * 1024 * 1024:
                raise forms.ValidationError("A foto deve ter no máximo 5MB.")

            extensoes_validas = ['jpg', 'jpeg', 'png', 'gif']
            extensao = foto.name.split('.')[-1].lower()
            if extensao not in extensoes_validas:
                raise forms.ValidationError("Formato de arquivo inválido. Use JPG, JPEG, PNG ou GIF.")

        return foto

    def clean(self):
        cleaned_data = super().clean()
        data_nascimento = cleaned_data.get('data_nascimento')
        data_admissao = cleaned_data.get('data_admissao')

        # Valida se data de admissão é posterior à data de nascimento
        if data_nascimento and data_admissao:
            if data_admissao < data_nascimento:
                raise forms.ValidationError({
                    'data_admissao': "Data de admissão não pode ser anterior à data de nascimento."
                })

        return cleaned_data