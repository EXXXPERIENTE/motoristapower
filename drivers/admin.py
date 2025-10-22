# drivers/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Motorista

@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = (
        'foto_miniatura',
        'nome_completo',
        'cpf_formatado',
        'idade',
        'cidade',
        'estado',
        'cnh_categoria',
        'status',
        'data_admissao'
    )
    list_filter = (
        'status', 'estado', 'cnh_categoria', 'data_admissao', 'created_at'
    )
    search_fields = ('nome_completo', 'cpf', 'email', 'cnh_numero')
    readonly_fields = ('created_at', 'updated_at', 'foto_preview', 'idade_display')
    fieldsets = (
        ('Foto', {
            'fields': ('foto', 'foto_preview')
        }),
        ('Dados Pessoais', {
            'fields': (
                'nome_completo', 'cpf', 'data_nascimento', 'idade_display', 'email', 'telefone'
            )
        }),
        ('Endereço', {
            'fields': (
                'cidade', 'estado'
            )
        }),
        ('Documentação', {
            'fields': (
                'cnh_numero', 'cnh_categoria'
            )
        }),
        ('Dados Profissionais', {
            'fields': (
                'data_admissao', 'salario', 'status'
            )
        }),
        ('Auditoria', {
            'fields': (
                'created_at', 'updated_at'
            )
        }),
    )

    def cpf_formatado(self, obj):
        return obj.cpf_formatado
    cpf_formatado.short_description = 'CPF'

    def idade_display(self, obj):
        return obj.idade
    idade_display.short_description = 'Idade'

    def foto_miniatura(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.foto.url
            )
        return "Sem foto"
    foto_miniatura.short_description = 'Foto'

    def foto_preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="150" height="150" style="border-radius: 8px; object-fit: cover;" />',
                obj.foto.url
            )
        return "Nenhuma foto cadastrada"
    foto_preview.short_description = 'Preview da Foto'