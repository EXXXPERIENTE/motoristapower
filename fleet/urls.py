"""
URL configuration for fleet project.
REDIRECIONA DIRETO PARA O CADASTRO
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


# View para redirecionar para o cadastro
def redirect_to_cadastro(request):
    """
    Redireciona a página inicial direto para o cadastro de motoristas
    """
    return redirect('drivers:cadastro_motorista')


urlpatterns = [
    # 🔧 Admin Django
    path('admin/', admin.site.urls),

    # 🚗 Página inicial redireciona para cadastro
    path('', redirect_to_cadastro, name='home'),

    # 🚗 App Drivers
    path('', include('drivers.urls', namespace='drivers')),
]

# 🔧 Configurações para desenvolvimento
if settings.DEBUG:
    # Servir arquivos de mídia durante o desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Servir arquivos estáticos durante o desenvolvimento
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 🎯 Personalização do Admin
admin.site.site_header = '🚗 MotoristaPower - Administração'
admin.site.site_title = 'MotoristaPower Admin'
admin.site.index_title = 'Painel de Controle do Sistema'

print("✅ URLs configuradas - REDIRECIONANDO PARA CADASTRO")
print("   🏠 Página inicial → Cadastro de motoristas")
print("   🔧 Admin: /admin/")
print("   🚗 Drivers: /")
print("   📁 Mídia: /media/")