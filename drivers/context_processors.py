from django.conf import settings
from .models import Motorista


def stats_context(request):
    """Adiciona estatísticas globais ao contexto"""
    return {
        'global_total_motoristas': Motorista.objects.count(),
        'global_motoristas_ativos': Motorista.objects.filter(status='ATIVO').count(),
        'app_name': settings.MOTORISTA_POWER_CONFIG['APP_NAME'],
        'app_version': settings.MOTORISTA_POWER_CONFIG['VERSION'],
    }


def mobile_context(request):
    """Detecta se é dispositivo mobile"""
    user_agent = getattr(request, 'user_agent', None)

    return {
        'is_mobile': user_agent.is_mobile if user_agent else False,
        'is_tablet': user_agent.is_tablet if user_agent else False,
        'is_touch_capable': user_agent.is_touch_capable if user_agent else False,
    }