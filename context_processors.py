from .models import Motorista

def stats_context(request):
    """Adiciona estatísticas globais ao contexto"""
    if request.user.is_authenticated:
        return {
            'global_total_motoristas': Motorista.objects.count(),
        }
    return {}