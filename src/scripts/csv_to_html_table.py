#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para gerar uma tabela HTML a partir do arquivo CSV de quantidades
"""

import os
import pandas as pd
from pathlib import Path
import html

def main():
    # Caminho para o arquivo CSV
    csv_path = os.path.join('dados', 'quantidades.csv')
    
    # Verificar se o arquivo existe
    if not os.path.exists(csv_path):
        alt_path = os.path.join('..', 'dados', 'quantidades.csv')
        print(f"Arquivo não encontrado. Tentando caminho alternativo: {alt_path}")
        if os.path.exists(alt_path):
            csv_path = alt_path
        else:
            print("Arquivo CSV não encontrado!")
            return
    
    print(f"Carregando dados do CSV: {csv_path}")
    
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(csv_path)
        print(f"Total de registros do CSV: {len(df)}")
        
        # Ordenar por tipo de impressão e tiragem
        df = df.sort_values(by=['print_type', 'run_length'])
        
        # Criar um HTML com a tabela formatada
        html_output = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tabela de Quantidades</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .explanation {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }
        th, td {
            padding: 12px;
            text-align: center;
            border: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
            position: sticky;
            top: 0;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #ddd;
        }
        .print-type-header {
            background-color: #1976D2;
            color: white;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            font-size: 0.9em;
            color: #666;
        }
        @media print {
            .no-print {
                display: none;
            }
            table {
                page-break-inside: auto;
            }
            tr {
                page-break-inside: avoid;
                page-break-after: auto;
            }
            thead {
                display: table-header-group;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Tabela de Quantidades para Cálculo de Desperdício</h1>
        
        <div class="explanation">
            <h3>Como utilizar esta tabela:</h3>
            <p>Esta tabela apresenta os valores de desperdício esperados para cada combinação de tipo de impressão e tiragem.</p>
            <p>Para encontrar o desperdício esperado:</p>
            <ol>
                <li>Localize o tipo de impressão na primeira coluna (ex: 4/0, 4/4)</li>
                <li>Encontre a tiragem mais próxima na segunda coluna</li>
                <li>O valor na terceira coluna representa o desperdício esperado em folhas</li>
            </ol>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Tipo de Impressão</th>
                    <th>Tiragem</th>
                    <th>Desperdício (folhas)</th>
                </tr>
            </thead>
            <tbody>
"""
        
        current_print_type = None
        
        # Criar linhas da tabela
        for _, row in df.iterrows():
            print_type = html.escape(str(row['print_type']))
            run_length = int(row['run_length'])
            waste_sheets = int(row['waste_sheets'])
            
            # Adicionar cabeçalho para novo tipo de impressão
            if current_print_type != print_type:
                current_print_type = print_type
                html_output += f"""                <tr class="print-type-header">
                    <td colspan="3">Tipo: {current_print_type}</td>
                </tr>
"""
            
            html_output += f"""                <tr>
                    <td>{print_type}</td>
                    <td>{run_length:,}</td>
                    <td>{waste_sheets}</td>
                </tr>
"""
        
        # Fechar o HTML
        html_output += """            </tbody>
        </table>
        
        <div class="footer">
            <p>Tabela gerada a partir dos dados do sistema. Última atualização: <span id="date"></span></p>
        </div>
    </div>
    
    <script>
        document.getElementById('date').textContent = new Date().toLocaleDateString('pt-BR');
    </script>
</body>
</html>
"""
        
        # Salvar como arquivo HTML
        output_path = os.path.join('static', 'tabela_quantidades.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print(f"Tabela HTML gerada com sucesso: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"Erro ao processar o arquivo CSV: {str(e)}")

if __name__ == "__main__":
    main() 