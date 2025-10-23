from django.contrib import admin
from .models import Motorista


@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = [
        'nome_completo', 'cpf_formatado', 'idade', 'cidade', 'estado',
        'cnh_categoria', 'status', 'created_at'
    ]
    list_filter = ['status', 'estado', 'cnh_categoria', 'created_at']
    search_fields = ['nome_completo', 'cpf', 'cnh_numero', 'cidade']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Dados Pessoais', {
            'fields': [
                'nome_completo', 'cpf', 'data_nascimento', 'email', 'telefone'
            ]
        }),
        ('Endereço', {
            'fields': [
                'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado'
            ]
        }),
        ('Documentação CNH', {
            'fields': [
                'cnh_numero', 'cnh_categoria', 'cnh_validade', 'cnh_emissao'
            ]
        }),
        ('Status e Informações', {
            'fields': [
                'status', 'salario', 'observacoes'
            ]
        }),
        ('Metadados', {
            'fields': [
                'created_at', 'updated_at'
            ],
            'classes': ['collapse']
        }),
    ]

    def cpf_formatado(self, obj):
        return obj.cpf_formatado

    cpf_formatado.short_description = 'CPF'