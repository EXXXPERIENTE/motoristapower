"""
URL configuration for drivers app.
"""

from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    # 🏠 Dashboard (agora acessível por /dashboard/)
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # 👥 Gerenciamento de Motoristas
    path('motoristas/', views.MotoristaListView.as_view(), name='motorista_list'),
    path('cadastro/', views.cadastro_motorista_view, name='cadastro_motorista'),
    path('editar/<int:pk>/', views.MotoristaUpdateView.as_view(), name='motorista_update'),
    path('excluir/<int:pk>/', views.MotoristaDeleteView.as_view(), name='motorista_delete'),

    # 📊 Relatórios
    path('relatorios/', views.relatorio_estatisticas, name='relatorio_estatisticas'),
    path('relatorios/excel/', views.relatorio_excel, name='relatorio_excel'),
    path('relatorios/pdf/', views.relatorio_pdf, name='relatorio_pdf'),
    path('relatorios/estatisticas-excel/', views.relatorio_estatisticas_excel, name='relatorio_estatisticas_excel'),
]

print("✅ URLs do app Drivers configuradas:")
print("   🏠 Dashboard: /dashboard/")
print("   👥 Lista: /motoristas/")
print("   ➕ Cadastro: /cadastro/")
print("   ✏️ Editar: /editar/<id>/")
print("   🗑️ Excluir: /excluir/<id>/")
print("   📊 Relatórios: /relatorios/")