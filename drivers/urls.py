from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    # URL PRINCIPAL DO APP: /drivers/ (Redireciona para o Dashboard)
    path('', views.DashboardView.as_view(), name='index'),

    # Dashboard (Classe View) - Acessado em /drivers/dashboard/
    # PROTEGIDO: Requer LoginRequiredMixin
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # Cadastro de motoristas - Acessado em /drivers/cadastro/
    # PÚBLICO: NÃO requer login, permitindo que usuários anônimos se cadastrem.
    path('cadastro/', views.cadastro_motorista, name='motorista_create'),

    # Lista de motoristas (Classe View) - Acessado em /drivers/motoristas/
    # PROTEGIDO: Requer LoginRequiredMixin
    path('motoristas/', views.MotoristaListView.as_view(), name='motorista_list'),

    # Editar motorista (Classe View)
    # PROTEGIDO: Requer LoginRequiredMixin e UserPassesTestMixin (Admin OU Próprio Motorista)
    path('editar/<int:pk>/', views.MotoristaUpdateView.as_view(), name='motorista_update'),

    # Excluir motorista (Classe View)
    # PROTEGIDO: Requer LoginRequiredMixin e UserPassesTestMixin (APENAS Admin)
    path('excluir/<int:pk>/', views.MotoristaDeleteView.as_view(), name='motorista_delete'),

    # Relatórios (Funções)
    # PROTEGIDO: Requer @login_required e verificação is_staff (APENAS Admin)
    path('relatorios/', views.relatorio_estatisticas, name='relatorios'),
    path('relatorios/excel/', views.relatorio_excel, name='relatorio_excel'),
    path('relatorios/pdf/', views.relatorio_pdf, name='relatorio_pdf'),
    path('relatorios/estatisticas-excel/', views.relatorio_estatisticas_excel, name='relatorio_estatisticas_excel'),
]
