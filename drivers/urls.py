from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    # ✅ PÚBLICO: Página inicial sem login
    path('', views.pagina_inicial, name='index'),

    # ✅ PÚBLICO: Cadastro sem login
    path('cadastro/', views.cadastro_motorista, name='motorista_create'),

    # ✅ PÚBLICO: Página de sucesso após cadastro
    path('sucesso/', views.pagina_sucesso, name='sucesso'),

    # 🔐 PRIVADO: Dashboard (precisa login)
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # 🔐 PRIVADO: Lista de motoristas (precisa login)
    path('motoristas/', views.MotoristaListView.as_view(), name='motorista_list'),

    # 🔐 PRIVADO: Editar (precisa login)
    path('editar/<int:pk>/', views.MotoristaUpdateView.as_view(), name='motorista_update'),

    # 🔐 PRIVADO: Excluir (só admin)
    path('excluir/<int:pk>/', views.MotoristaDeleteView.as_view(), name='motorista_delete'),

    # 🔐 PRIVADO: Relatórios (só admin)
    path('relatorios/', views.relatorio_estatisticas, name='relatorios'),
    path('relatorios/excel/', views.relatorio_excel, name='relatorio_excel'),
    path('relatorios/pdf/', views.relatorio_pdf, name='relatorio_pdf'),
    path('relatorios/estatisticas-excel/', views.relatorio_estatisticas_excel, name='relatorio_estatisticas_excel'),
]