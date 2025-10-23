"""
URL configuration for fleet project.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


# View para redirecionar para o dashboard (ou para o login, se não logado)
def redirect_to_dashboard_or_create(request):
    # Redireciona para o dashboard, que é a landing page após o login.
    return redirect('drivers:dashboard')

urlpatterns = [
    # 🔧 Admin Django
    path('admin/', admin.site.urls),

    # 🔑 AUTENTICAÇÃO: Inclui as URLs de login, logout e reset de senha.
    # ISSO CORRIGE O ERRO 404 DO /accounts/login/
    path('accounts/', include('django.contrib.auth.urls')),

    # 🚗 App Drivers (o namespace 'drivers' é definido no drivers/urls.py com app_name)
    path('drivers/', include('drivers.urls')),

    # 🏠 Página inicial (raiz) redireciona para o dashboard
    path('', redirect_to_dashboard_or_create, name='home'),
]

# 🔧 Configurações para desenvolvimento (Mídia e Estáticos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 🎯 Personalização do Admin
admin.site.site_header = '🚗 MotoristaPower - Administração'
admin.site.site_title = 'MotoristaPower Admin'
admin.site.index_title = 'Painel de Controle do Sistema'