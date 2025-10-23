from django.db import models
from django.core.validators import RegexValidator
from datetime import date
from django.contrib.auth.models import User # NOVO: Importa o modelo de Usuário do Django


class Motorista(models.Model):
    CATEGORIA_CNH_CHOICES = [
        ('A', 'A - Moto'),
        ('B', 'B - Carro'),
        ('C', 'C - Caminhão'),
        ('D', 'D - Ônibus'),
        ('E', 'E - Reboque'),
    ]

    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
        ('FERIAS', 'Férias'),
        ('AFASTADO', 'Afastado'),
    ]

    ESTADO_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    ]

    # 🔑 NOVO CAMPO: Vínculo com o usuário do Django que criou/é o dono do cadastro
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,  # Permite que cadastros antigos (ou criados pelo Admin) não tenham usuário
        blank=True,
        verbose_name='Usuário Associado'
    )

    # Dados Pessoais
    nome_completo = models.CharField(max_length=100, verbose_name='Nome Completo')
    cpf = models.CharField(
        max_length=14,  # Mantido 14 (máscara)
        unique=True,
        verbose_name='CPF',
        validators=[
            RegexValidator(regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message='CPF deve estar no formato: 000.000.000-00')]
    )
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    email = models.EmailField(verbose_name='E-mail')
    telefone = models.CharField(
        max_length=15,
        verbose_name='Telefone',
        validators=[RegexValidator(regex=r'^\(\d{2}\)\s?\d{4,5}-\d{4}$',
                                   message='Telefone deve estar no formato: (00) 00000-0000')]
    )

    # Endereço
    cep = models.CharField(max_length=9, verbose_name='CEP', default='')
    endereco = models.CharField(max_length=200, verbose_name='Endereço')
    numero = models.CharField(max_length=10, verbose_name='Número')
    complemento = models.CharField(max_length=100, verbose_name='Complemento', blank=True)
    bairro = models.CharField(max_length=100, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, verbose_name='Estado')

    # Documentação CNH
    cnh_numero = models.CharField(max_length=11, unique=True, verbose_name='Número da CNH')
    cnh_categoria = models.CharField(max_length=2, choices=CATEGORIA_CNH_CHOICES, verbose_name='Categoria CNH')
    cnh_validade = models.DateField(verbose_name='Validade da CNH')
    cnh_emissao = models.DateField(verbose_name='Data de Emissão')

    # NOVO CAMPO DE FOTO
    foto = models.ImageField(upload_to='motorista_fotos/', null=True, blank=True, verbose_name='Foto')

    # Status e controle
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATIVO', verbose_name='Status')
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Salário')
    observacoes = models.TextField(blank=True, verbose_name='Observações')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Atualização')

    class Meta:
        verbose_name = 'Motorista'
        verbose_name_plural = 'Motoristas'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

    @property
    def idade(self):
        if not self.data_nascimento:
            return None
        today = date.today()
        return today.year - self.data_nascimento.year - (
                (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    @property
    def cpf_formatado(self):
        # Manteve a lógica robusta para CPFs com ou sem máscara
        cpf = self.cpf.replace('.', '').replace('-', '')
        if cpf and len(cpf) == 11:
            return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        return self.cpf or ''

    def cnh_proxima_vencer(self):
        if not self.cnh_validade:
            return False
        today = date.today()
        days_until_expiry = (self.cnh_validade - today).days
        return 0 <= days_until_expiry <= 30