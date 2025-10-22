from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count, Q, Sum, Avg
from datetime import datetime
from django.http import HttpResponse
from django.contrib import messages
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
import threading

from .forms import MotoristaForm
from .models import Motorista


class MotoristaListView(ListView):
    model = Motorista
    template_name = 'drivers/motorista_list.html'
    context_object_name = 'motoristas'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtro por status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filtro por busca
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nome_completo__icontains=search) |
                Q(cpf__icontains=search) |
                Q(cnh_numero__icontains=search) |
                Q(cidade__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Estatísticas para o template
        context['total_motoristas'] = Motorista.objects.count()
        context['motoristas_ativos'] = Motorista.objects.filter(status='ATIVO').count()
        context['motoristas_inativos'] = Motorista.objects.filter(status='INATIVO').count()

        # Manter parâmetros de filtro na paginação
        context['current_status'] = self.request.GET.get('status', '')
        context['current_search'] = self.request.GET.get('search', '')

        return context


class MotoristaUpdateView(UpdateView):
    model = Motorista
    form_class = MotoristaForm
    template_name = 'drivers/motorista_form.html'
    success_url = reverse_lazy('drivers:motorista_list')

    def form_valid(self, form):
        messages.success(self.request, 'Motorista atualizado com sucesso!')
        return super().form_valid(form)


class MotoristaDeleteView(DeleteView):
    model = Motorista
    template_name = 'drivers/motorista_confirm_delete.html'
    success_url = reverse_lazy('drivers:motorista_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Motorista excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


def dashboard_view(request):
    # Estatísticas para o dashboard
    total_motoristas = Motorista.objects.count()
    motoristas_ativos = Motorista.objects.filter(status='ATIVO').count()
    motoristas_inativos = Motorista.objects.filter(status='INATIVO').count()

    # Estatísticas por estado
    estados_stats = Motorista.objects.values('estado').annotate(
        total=Count('id')
    ).order_by('-total')[:5]

    # Últimos cadastros
    ultimos_cadastros = Motorista.objects.all().order_by('-created_at')[:5]

    context = {
        'total_motoristas': total_motoristas,
        'motoristas_ativos': motoristas_ativos,
        'motoristas_inativos': motoristas_inativos,
        'estados_stats': estados_stats,
        'ultimos_cadastros': ultimos_cadastros,
    }
    return render(request, 'drivers/dashboard.html', context)


def cadastro_motorista_view(request):
    if request.method == 'POST':
        form = MotoristaForm(request.POST, request.FILES)
        if form.is_valid():
            motorista = form.save()

            # ✅ WHATSAPP REAL - VERSÃO CORRIGIDA
            nome_motorista = motorista.nome_completo or "Motorista Sem Nome"

            def enviar_notificacao():
                try:
                    from .services_whatsapp import enviar_whatsapp_real

                    print("")
                    print("🎯" * 60)
                    print("📱 SISTEMA MOTORISTAPOWER - INICIANDO WHATSAPP REAL")
                    print(f"👤 Motorista: {nome_motorista}")
                    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                    print("🎯" * 60)
                    print("")

                    if enviar_whatsapp_real(nome_motorista):
                        print("✅ ✅ ✅ WHATSAPP ENVIADO COM SUCESSO! ✅ ✅ ✅")
                    else:
                        print("⚠️ WhatsApp falhou - Tente novamente")

                except Exception as e:
                    print(f"❌ Erro no WhatsApp: {e}")

            # Executar em thread separada
            thread = threading.Thread(target=enviar_notificacao)
            thread.daemon = True
            thread.start()

            # Salvar em arquivo de log
            with open("cadastros_sucesso.log", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()} - CADASTRO: {nome_motorista}\n")

            messages.success(request, f"✅ Motorista {nome_motorista} cadastrado! WhatsApp sendo enviado... 📱")
            return redirect('drivers:motorista_list')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = MotoristaForm()

    context = {'form': form}
    return render(request, 'drivers/cadastro_motorista.html', context)


def relatorio_estatisticas(request):
    """Relatório de estatísticas dos motoristas"""
    total_motoristas = Motorista.objects.count()

    # Estatísticas por status
    status_stats = Motorista.objects.values('status').annotate(
        total=Count('id')
    ).order_by('-total')

    # Estatísticas por estado
    estado_stats = Motorista.objects.values('estado').annotate(
        total=Count('id')
    ).order_by('-total')

    # Estatísticas por categoria CNH
    categoria_stats = Motorista.objects.values('cnh_categoria').annotate(
        total=Count('id')
    ).order_by('-total')

    # Salários
    total_salarios = Motorista.objects.filter(salario__isnull=False).aggregate(
        total=Sum('salario')
    )['total'] or 0

    salario_medio = Motorista.objects.filter(salario__isnull=False).aggregate(
        medio=Avg('salario')
    )['medio'] or 0

    # Média de idade
    idade_media = None
    if total_motoristas > 0:
        idades = [motorista.idade for motorista in Motorista.objects.all() if motorista.data_nascimento]
        if idades:
            idade_media = sum(idades) / len(idades)

    context = {
        'total_motoristas': total_motoristas,
        'status_stats': status_stats,
        'estado_stats': estado_stats,
        'categoria_stats': categoria_stats,
        'total_salarios': total_salarios,
        'salario_medio': salario_medio,
        'idade_media': idade_media,
    }

    return render(request, 'drivers/relatorio_estatisticas.html', context)


def relatorio_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Relatório Motoristas"

    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    center_align = Alignment(horizontal='center', vertical='center')

    ws.merge_cells('A1:L1')
    ws['A1'] = "RELATÓRIO DE MOTORISTAS - MOTORISTAPOWER"
    ws['A1'].font = Font(bold=True, size=16, color="366092")
    ws['A1'].alignment = center_align

    ws.merge_cells('A2:L2')
    ws['A2'] = f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
    ws['A2'].alignment = center_align

    headers = ['ID', 'Nome', 'CPF', 'Data Nasc.', 'Idade', 'Telefone', 'Cidade/UF',
               'CNH', 'Categoria', 'Status', 'Salário', 'Data Cadastro']

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    motoristas = Motorista.objects.all().order_by('nome_completo')
    for row, motorista in enumerate(motoristas, 5):
        ws.cell(row=row, column=1, value=motorista.id)
        ws.cell(row=row, column=2, value=motorista.nome_completo or 'NÃO INFORMADO')
        ws.cell(row=row, column=3, value=motorista.cpf_formatado)
        ws.cell(row=row, column=4,
                value=motorista.data_nascimento.strftime('%d/%m/%Y') if motorista.data_nascimento else '')
        ws.cell(row=row, column=5, value=motorista.idade)
        ws.cell(row=row, column=6, value=motorista.telefone or '')
        ws.cell(row=row, column=7, value=f"{motorista.cidade or ''}/{motorista.estado or ''}")
        ws.cell(row=row, column=8, value=motorista.cnh_numero or '')
        ws.cell(row=row, column=9, value=motorista.cnh_categoria or '')
        ws.cell(row=row, column=10, value=motorista.get_status_display())
        ws.cell(row=row, column=11, value=float(motorista.salario) if motorista.salario else 0)
        ws.cell(row=row, column=12, value=motorista.created_at.strftime('%d/%m/%Y %H:%M'))

    column_widths = [8, 30, 15, 12, 8, 15, 15, 15, 10, 12, 12, 18]
    for col, width in enumerate(column_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = width

    ws.merge_cells(f'A{row + 2}:L{row + 2}')
    ws.cell(row=row + 2, column=1, value=f"TOTAL DE MOTORISTAS: {motoristas.count()}")
    ws.cell(row=row + 2, column=1).font = Font(bold=True, color="366092")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="relatorio_motoristas.xlsx"'

    wb.save(response)
    return response


def relatorio_pdf(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Center',
        alignment=1,
        fontSize=14,
        spaceAfter=30
    ))

    elements = []

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#366092'),
        alignment=1,
        spaceAfter=30
    )

    elements.append(Paragraph("RELATÓRIO DE MOTORISTAS", title_style))
    elements.append(Paragraph(f"<b>MotoristaPower</b> - Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
                              styles['Center']))
    elements.append(Spacer(1, 20))

    motoristas = Motorista.objects.all().order_by('nome_completo')

    if motoristas:
        data = [['ID', 'Nome', 'CPF', 'Idade', 'Cidade/UF', 'Status', 'CNH']]

        for motorista in motoristas:
            data.append([
                str(motorista.id),
                motorista.nome_completo or 'NÃO INFORMADO',
                motorista.cpf_formatado,
                str(motorista.idade),
                f"{motorista.cidade or ''}/{motorista.estado or ''}",
                motorista.get_status_display(),
                motorista.cnh_categoria or 'N/I'
            ])

        table = Table(data, colWidths=[0.5 * inch, 2 * inch, 1.2 * inch, 0.6 * inch, 1 * inch, 0.8 * inch, 0.6 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

        elements.append(Paragraph(f"<b>Total de Motoristas:</b> {motoristas.count()}", styles['Normal']))
        elements.append(Paragraph(f"<b>Ativos:</b> {motoristas.filter(status='ATIVO').count()}", styles['Normal']))
        elements.append(Paragraph(f"<b>Inativos:</b> {motoristas.filter(status='INATIVO').count()}", styles['Normal']))

    else:
        elements.append(Paragraph("Nenhum motorista cadastrado.", styles['Normal']))

    doc.build(elements)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_motoristas.pdf"'
    response.write(buffer.getvalue())
    buffer.close()

    return response


def relatorio_estatisticas_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Estatísticas"

    header_font = Font(bold=True, color="FFFFFF", size=14)
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    center_align = Alignment(horizontal='center', vertical='center')

    ws.merge_cells('A1:E1')
    ws['A1'] = "RELATÓRIO ESTATÍSTICO - MOTORISTAPOWER"
    ws['A1'].font = header_font
    ws['A1'].fill = header_fill
    ws['A1'].alignment = center_align

    ws.merge_cells('A2:E2')
    ws['A2'] = f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
    ws['A2'].alignment = center_align

    total_motoristas = Motorista.objects.count()
    ativos = Motorista.objects.filter(status='ATIVO').count()
    inativos = Motorista.objects.filter(status='INATIVO').count()
    total_salarios = Motorista.objects.filter(salario__isnull=False).aggregate(total=Sum('salario'))['total'] or 0

    ws['A4'] = "ESTATÍSTICAS GERAIS"
    ws['A4'].font = Font(bold=True, size=12)

    data_geral = [
        ['Total de Motoristas', total_motoristas],
        ['Motoristas Ativos', ativos],
        ['Motoristas Inativos', inativos],
        ['Folha de Pagamento Total', f'R$ {total_salarios:,.2f}'],
    ]

    for row, (label, value) in enumerate(data_geral, 5):
        ws.cell(row=row, column=1, value=label)
        ws.cell(row=row, column=2, value=value)
        ws.cell(row=row, column=1).font = Font(bold=True)

    ws['A10'] = "DISTRIBUIÇÃO POR ESTADO"
    ws['A10'].font = Font(bold=True, size=12)

    estados = Motorista.objects.values('estado').annotate(total=Count('id')).order_by('-total')
    for row, estado in enumerate(estados, 11):
        ws.cell(row=row, column=1, value=estado['estado'] or 'NÃO INFORMADO')
        ws.cell(row=row, column=2, value=estado['total'])

    ws['D10'] = "DISTRIBUIÇÃO POR CATEGORIA CNH"
    ws['D10'].font = Font(bold=True, size=12)

    categorias = Motorista.objects.values('cnh_categoria').annotate(total=Count('id')).order_by('-total')
    for row, categoria in enumerate(categorias, 11):
        ws.cell(row=row, column=4, value=categoria['cnh_categoria'] or 'NÃO INFORMADA')
        ws.cell(row=row, column=5, value=categoria['total'])

    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['D'].width = 25
    ws.column_dimensions['E'].width = 15

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="estatisticas_motoristas.xlsx"'

    wb.save(response)
    return response