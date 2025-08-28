import os
import sys
from datetime import datetime
from io import BytesIO
import threading
import time
from collections import defaultdict
import json

from flask import Flask, send_from_directory, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
CORS(app)

# Cache para armazenar os dados da planilha
excel_cache = {'data': None, 'last_modified': None}

def load_excel_data():
    """Carrega os dados da planilha Excel"""
    global excel_cache
    try:
        import pandas as pd
        file_path = os.path.join(os.path.dirname(__file__), 'PROCESSOSCLIENTES.xlsx')
        if os.path.exists(file_path):
            # Verificar se o arquivo foi modificado
            current_modified = os.path.getmtime(file_path)
            
            if excel_cache['last_modified'] != current_modified:
                print(f"Recarregando planilha... Última modificação: {datetime.fromtimestamp(current_modified)}")
                df = pd.read_excel(file_path, dtype={'CPF': str})
                # Tratar CPFs com e sem pontuação
                df['CPF'] = df['CPF'].astype(str).str.replace(r'[^0-9]', '', regex=True)
                # Remover linhas com CPF vazio ou inválido
                df = df[df['CPF'].str.len() == 11]
                excel_cache['data'] = df
                excel_cache['last_modified'] = current_modified
                
        return excel_cache['data']
    except Exception as e:
        print(f"Erro ao carregar planilha: {e}")
        return None

def monitor_excel_file():
    """Monitor contínuo do arquivo Excel para detectar mudanças"""
    while True:
        load_excel_data()
        time.sleep(30)  # Verificar a cada 30 segundos

# Iniciar o monitor em uma thread separada
monitor_thread = threading.Thread(target=monitor_excel_file, daemon=True)
monitor_thread.start()

@app.route('/search', methods=['POST'])
def search_data():
    cpf = request.json.get('cpf')
    if not cpf:
        return jsonify({'error': 'CPF não fornecido'}), 400

    try:
        import pandas as pd
        # Usar dados do cache
        df = load_excel_data()
        if df is None:
            return jsonify({'error': 'Erro ao carregar dados da planilha'}), 500
        
        cpf = ''.join(filter(str.isdigit, cpf))
        results = df[df['CPF'] == cpf]

        if not results.empty:
            # Agrupar todos os processos do mesmo CPF
            processes = []
            client_name = None
            client_cpf = None
            
            for _, row in results.iterrows():
                if client_name is None:
                    client_name = row.get('CLIENTE', '')
                    client_cpf = cpf
                
                # Formatar CPF para exibição
                formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
                
                process_data = {
                    'nome': client_name,
                    'cpf': formatted_cpf,
                    'acao': row.get('AÇÃO', ''),
                    'numero': str(row.get('N PROCESSO', '')) if pd.notna(row.get('N PROCESSO')) else 'Ainda será aberto'
                }
                processes.append(process_data)
            
            return jsonify({
                'nome': client_name,
                'cpf': formatted_cpf,
                'processos': processes
            })
        else:
            return jsonify({'error': 'CPF não encontrado'}), 404
    except Exception as e:
        print(f"Erro na busca: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/statistics', methods=['GET'])
def get_statistics():
    """Endpoint para obter estatísticas das ações"""
    try:
        import pandas as pd
        df = load_excel_data()
        if df is None:
            return jsonify({'error': 'Erro ao carregar dados da planilha'}), 500
        
        # Contar ações por tipo
        action_counts = df['AÇÃO'].value_counts().to_dict()
        
        # Calcular total
        total = sum(action_counts.values())
        
        # Calcular percentuais
        statistics = []
        for action, count in action_counts.items():
            if pd.notna(action) and action != '':
                percentage = (count / total) * 100 if total > 0 else 0
                statistics.append({
                    'action': action,
                    'count': count,
                    'percentage': round(percentage, 1)
                })
        
        # Ordenar por contagem (maior para menor)
        statistics.sort(key=lambda x: x['count'], reverse=True)
        
        return jsonify(statistics)
    except Exception as e:
        print(f"Erro ao obter estatísticas: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/reload-data', methods=['POST'])
def reload_data():
    """Endpoint para forçar o recarregamento dos dados"""
    try:
        load_excel_data()
        return jsonify({'message': 'Dados recarregados com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export-pdf', methods=['POST'])
def export_pdf():
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        data = request.json
        
        # Criar buffer para o PDF
        buffer = BytesIO()
        
        # Criar documento PDF
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
        story = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1e3a8a')
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            textColor=colors.HexColor('#1e3a8a')
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )
        
        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), 'LOGO.jpg')
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=3*inch, height=1.5*inch)
            logo.hAlign = 'CENTER'
            story.append(logo)
            story.append(Spacer(1, 20))
        
        # Título
        story.append(Paragraph("Consulta de Processos Jurídicos", title_style))
        story.append(Spacer(1, 20))
        
        # Dados do cliente
        story.append(Paragraph("Informações do Cliente", header_style))
        
        # Informações básicas do cliente
        client_data = [
            ['Nome:', data.get('nome', '')],
            ['CPF:', data.get('cpf', '')]
        ]
        
        client_table = Table(client_data, colWidths=[1.5*inch, 4.5*inch])
        client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1e3a8a')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        story.append(client_table)
        story.append(Spacer(1, 20))
        
        # Processos
        story.append(Paragraph("Processos", header_style))
        
        processes = data.get('processos', [])
        if processes:
            process_data = [['Ação', 'Número do Processo']]
            for process in processes:
                process_data.append([
                    process.get('acao', ''),
                    process.get('numero', '')
                ])
            
            process_table = Table(process_data, colWidths=[2*inch, 4*inch])
            process_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
            ]))
            story.append(process_table)
        
        story.append(Spacer(1, 40))
        
        # Data de geração
        data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M")
        story.append(Paragraph(f"Relatório gerado em: {data_geracao}", normal_style))
        
        story.append(Spacer(1, 40))
        
        # Rodapé com informações de contato
        story.append(Paragraph("Contato", header_style))
        
        contato_data = [
            ['Telefones:', '(79) 9.8150-9934 – Cálculos Jurídicos Daniely'],
            ['', '(79) 9.8833-9003 – Dr. Jeferson OAB 12.878'],
            ['Site:', 'https://jefersonsantos.godaddysites.com/'],
            ['Email:', 'escritoriojsantosadvocacia@gmail.com'],
            ['Endereços:', 'Rua Lagarto, 1034 – Centro, Aracaju/SE'],
            ['', 'Rua Cabo Resende, 112 – Barra dos Coqueiros/SE']
        ]
        
        contato_table = Table(contato_data, colWidths=[1.5*inch, 4.5*inch])
        contato_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#334155'))
        ]))
        story.append(contato_table)
        
        # Construir PDF
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'processos_{data.get("cpf", "cliente").replace(".", "").replace("-", "")}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    # Carregar dados iniciais
    load_excel_data()
    app.run(host='0.0.0.0', port=5001, debug=True)

