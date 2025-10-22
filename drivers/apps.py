from django.apps import AppConfig


class DriversConfig(AppConfig):
    # Campo padrão para chaves primárias (recomendado pelo Django)
    default_auto_field = 'django.db.models.BigAutoField'

    # Nome do aplicativo
    name = 'drivers'

    # Nome que aparecerá no Admin (opcional, mas profissional)
    verbose_name = 'Cadastro de Motoristas'