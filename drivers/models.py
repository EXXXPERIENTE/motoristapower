from django.db import models
from datetime import date
import os
from .validators import validar_cpf, formatar_cpf, validar_categoria_cnh  # ← ADICIONE O NOVO VALIDADOR


class Motorista(models.Model):
    foto = models.ImageField(
        'Foto do Motorista',
        upload_to='motoristas/fotos/',
        blank=True,
        null=True,
        help_text='Foto 3x4 do motorista'
    )

    nome_completo = models.CharField('Nome Completo', max_length=100)
    cpf = models.CharField('CPF', max_length=14, unique=True, validators=[validar_cpf])
    data_nascimento = models.DateField('Data de Nascimento')
    email = models.EmailField('E-mail', blank=True, null=True)
    telefone = models.CharField('Telefone', max_length=15, blank=True, null=True)

    cidade = models.CharField('Cidade', max_length=50, blank=True, null=True)
    estado = models.CharField('Estado', max_length=2, choices=[
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ], blank=True, null=True)

    cnh_numero = models.CharField('Número da CNH', max_length=20, blank=True, null=True)
    cnh_categoria = models.CharField(
        'Categoria CNH',
        max_length=5,
        choices=[('E', 'E')],  # ← SOMENTE CATEGORIA E
        blank=True,
        null=True,
        validators=[validar_categoria_cnh]  # ← ADICIONE O VALIDADOR
    )

    data_admissao = models.DateField('Data de Admissão', blank=True, null=True)
    salario = models.DecimalField('Salário', max_digits=10, decimal_places=2, blank=True, null=True)

    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('AFASTADO', 'Afastado'),
        ('FERIAS', 'Férias'),
        ('INATIVO', 'Inativo')
    ]
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='ATIVO')

    created_at = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)

    class Meta:
        verbose_name = 'Motorista'
        verbose_name_plural = 'Motoristas'
        ordering = ['-created_at']

    def __str__(self):
        return self.nome_completo

    @property
    def idade(self):
        if not self.data_nascimento:
            return None
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        if hoje.month < self.data_nascimento.month or (
                hoje.month == self.data_nascimento.month and hoje.day < self.data_nascimento.day
        ):
            idade -= 1
        return idade

    @property
    def cpf_formatado(self):
        return formatar_cpf(self.cpf)

    @property
    def tem_foto(self):
        return bool(self.foto)

    def get_status_display(self):
        """Retorna o display do status"""
        for status_code, status_name in self.STATUS_CHOICES:
            if status_code == self.status:
                return status_name
        return self.status

    def clean(self):
        """
        Validação no nível do modelo para CPF duplicado
        """
        from django.core.exceptions import ValidationError
        import re

        super().clean()

        # Verifica se já existe outro motorista com o mesmo CPF
        if self.cpf:
            cpf_limpo = re.sub(r'[^0-9]', '', self.cpf)
            motoristas_com_mesmo_cpf = Motorista.objects.filter(
                cpf__icontains=cpf_limpo
            ).exclude(pk=self.pk)

            if motoristas_com_mesmo_cpf.exists():
                raise ValidationError({
                    'cpf': 'Este CPF já está cadastrado no sistema.'
                })

    def save(self, *args, **kwargs):
        # Valida o modelo antes de salvar
        self.full_clean()

        # Formata o CPF antes de salvar
        if self.cpf:
            self.cpf = validar_cpf(self.cpf)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.foto:
            if os.path.isfile(self.foto.path):
                os.remove(self.foto.path)
        super().delete(*args, **kwargs)