#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para criar um arquivo Excel de exemplo com dados fictícios
para demonstrar como seriam milhares de registros de impressão.
"""

import os
import random
import pandas as pd
import numpy as np
from datetime import datetime

def main():
    # Definir os parâmetros para gerar os dados
    print_types = ['1/0', '1/1', '2/0', '2/2', '4/0', '4/4', '5/0', '5/5']
    run_lengths = [500, 1000, 2000, 3000, 5000, 10000]
    
    # Gerar um conjunto maior e mais variado de dados com base em parâmetros reais
    # Vamos gerar 10.000 registros aleatórios
    num_records = 10000
    
    # Criar listas para os dados
    records = []
    
    # Gerar combinações básicas (como no exemplo original)
    base_records = []
    for pt in print_types:
        for rl in run_lengths:
            # Simular o desperdício de folhas com base no tipo de impressão e tiragem
            # Fórmula fictícia: waste = base_waste * coeficiente do tipo + fator de tiragem
            pt_coefficient = 1.0 + (float(pt.split('/')[0]) * 0.1)
            base_waste = int(5 + (rl / 500) * 2)
            waste = int(base_waste * pt_coefficient)
            
            base_records.append({
                'print_type': pt,
                'run_length': rl,
                'waste_sheets': waste
            })
    
    # Adicionar os registros base (estes são os 48 registros do original)
    records.extend(base_records)
    
    # Gerar registros adicionais com mais variações
    for _ in range(num_records - len(base_records)):
        # Gerar tipos de impressão mais variados (2/1, 3/0, 3/1, 3/2, etc.)
        frente = random.randint(1, 6)
        verso = random.randint(0, frente)
        pt = f"{frente}/{verso}"
        
        # Gerar tiragens mais variadas
        rl = random.choice([
            random.randint(100, 499),  # Tiragens menores
            random.choice(run_lengths),  # Tiragens padrão
            random.randint(10001, 50000)  # Tiragens maiores
        ])
        
        # Gerar desperdício com alguma variação
        pt_coefficient = 1.0 + (frente * 0.1) + (verso * 0.05)
        base_waste = int(5 + (rl / 450) * 1.5)
        # Adicionar alguma variação aleatória (+/- 20%)
        variation = random.uniform(0.8, 1.2)
        waste = max(1, int(base_waste * pt_coefficient * variation))
        
        records.append({
            'print_type': pt,
            'run_length': rl,
            'waste_sheets': waste
        })
    
    # Adicionar outras colunas para tornar mais realista
    for record in records:
        # Data aleatória nos últimos 2 anos
        days_ago = random.randint(1, 730)
        record['date'] = (datetime.now() - pd.Timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Código do cliente
        record['client_code'] = f"CLI{random.randint(1000, 9999)}"
        
        # Número do trabalho
        record['job_number'] = f"JOB-{random.randint(10000, 99999)}"
        
        # Formato do papel
        formats = ['A4', 'A3', 'SRA3', '70x100', '50x70']
        record['paper_format'] = random.choice(formats)
        
        # Gramatura do papel
        gsm_options = [80, 90, 115, 135, 150, 170, 250, 300, 350]
        record['paper_gsm'] = random.choice(gsm_options)
        
        # Máquina de impressão
        machines = ['Heidelberg SM52', 'Heidelberg CD74', 'Komori GL540', 'KBA Rapida 106', 'Roland 700']
        record['machine'] = random.choice(machines)
    
    # Criar DataFrame
    df = pd.DataFrame(records)
    
    # Ordenar por data, tipo de impressão e tiragem
    df = df.sort_values(['date', 'print_type', 'run_length'])
    
    # Criar diretório se não existir
    os.makedirs('dados', exist_ok=True)
    
    # Salvar arquivo
    output_file = os.path.join('dados', 'quantidades_detalhado.xlsx')
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    
    # Salvar na planilha principal
    df.to_excel(writer, sheet_name='Dados Completos', index=False)
    
    # Criar uma segunda planilha com estatísticas
    # Agrupar por tipo de impressão e tiragem para ver médias de desperdício
    stats = df.groupby(['print_type', 'run_length']).agg({
        'waste_sheets': ['count', 'mean', 'std', 'min', 'max'],
        'client_code': 'nunique'
    }).reset_index()
    
    stats.columns = ['print_type', 'run_length', 'count', 'waste_avg', 'waste_std', 'waste_min', 'waste_max', 'clients']
    stats.to_excel(writer, sheet_name='Estatísticas', index=False)
    
    # Criar uma terceira planilha apenas com os dados originais
    original_df = pd.DataFrame(base_records)
    original_df.to_excel(writer, sheet_name='Dados Originais', index=False)
    
    # Finalizar
    writer.close()
    
    print(f"Arquivo Excel criado com sucesso: {output_file}")
    print(f"Total de registros: {len(df)}")
    print(f"Tipos de impressão únicos: {df['print_type'].nunique()}")
    print(f"Tiragens únicas: {df['run_length'].nunique()}")

if __name__ == "__main__":
    main() 