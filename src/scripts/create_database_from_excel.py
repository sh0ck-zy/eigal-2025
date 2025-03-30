#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para criar um banco de dados com os dados completos do Excel
"""

import os
import sqlite3
import pandas as pd
from pathlib import Path

def main():
    # Caminho para o arquivo Excel
    excel_path = os.path.join('dados', 'quantidades_detalhado.xlsx')
    
    # Verificar se o arquivo existe
    if not os.path.exists(excel_path):
        alt_path = os.path.join('..', 'dados', 'quantidades_detalhado.xlsx')
        print(f"Arquivo não encontrado. Tentando caminho alternativo: {alt_path}")
        if os.path.exists(alt_path):
            excel_path = alt_path
        else:
            print("Arquivo Excel não encontrado!")
            return
    
    print(f"Carregando dados do Excel: {excel_path}")
    
    # Novo banco de dados
    db_path = 'waste_calculation_complete.db'
    
    # Excluir banco de dados existente se necessário
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Banco de dados existente removido: {db_path}")
    
    # Criar nova conexão com banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Criar tabela para os dados completos
    cursor.execute('''
    CREATE TABLE quantities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        print_type VARCHAR(10) NOT NULL,
        run_length INTEGER NOT NULL,
        waste_sheets INTEGER NOT NULL,
        date DATE,
        client_code VARCHAR(10),
        job_number VARCHAR(20),
        paper_format VARCHAR(10),
        paper_gsm INTEGER,
        machine VARCHAR(30),
        adjustment VARCHAR(20),
        is_special_case BOOLEAN DEFAULT 0
    )
    ''')
    
    # Também criar a tabela de tipos de impressão
    cursor.execute('''
    CREATE TABLE print_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(10) NOT NULL UNIQUE,
        description VARCHAR(100),
        front_colors INTEGER,
        back_colors INTEGER
    )
    ''')
    
    # Ler o arquivo Excel - usar a planilha de dados completos
    df = pd.read_excel(excel_path, sheet_name='Dados Completos')
    
    print(f"Total de registros a serem importados: {len(df)}")
    
    # Inserir dados na tabela
    # Para inserções em massa, é mais eficiente usar pandas
    # Mas vamos usar o sqlite diretamente para mais controle
    
    # Preparar os tipos de impressão para a tabela de tipos
    print_types = []
    for pt in df['print_type'].unique():
        parts = pt.split('/')
        front = int(parts[0])
        back = int(parts[1])
        
        description = f"{front} cor"
        if front > 1:
            description += "es"
        if back > 0:
            description += f" + {back} cor"
            if back > 1:
                description += "es"
            description += " no verso"
        else:
            description += " somente frente"
        
        print_types.append((pt, description, front, back))
    
    cursor.executemany(
        "INSERT INTO print_types (name, description, front_colors, back_colors) VALUES (?, ?, ?, ?)",
        print_types
    )
    
    # Inserir registros na tabela principal
    # Dividir em lotes para performance
    batch_size = 1000
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        
        # Preparar os valores a serem inseridos
        values = []
        for _, row in batch.iterrows():
            values.append((
                row['print_type'], 
                row['run_length'], 
                row['waste_sheets'],
                row['date'],
                row['client_code'],
                row['job_number'],
                row['paper_format'],
                row['paper_gsm'],
                row['machine'],
                None,  # adjustment
                False  # is_special_case
            ))
        
        cursor.executemany(
            '''INSERT INTO quantities 
               (print_type, run_length, waste_sheets, date, client_code, job_number, 
               paper_format, paper_gsm, machine, adjustment, is_special_case) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            values
        )
        
        print(f"Inseridos {min(i+batch_size, len(df))} de {len(df)} registros...")
    
    # Criar índices para melhorar performance de consultas
    cursor.execute('CREATE INDEX idx_print_type_run ON quantities (print_type, run_length)')
    cursor.execute('CREATE INDEX idx_date ON quantities (date)')
    cursor.execute('CREATE INDEX idx_client ON quantities (client_code)')
    
    # Commit e encerrar
    conn.commit()
    conn.close()
    
    print(f"Banco de dados criado com sucesso: {db_path}")
    print(f"Total de tipos de impressão inseridos: {len(print_types)}")
    print(f"Total de registros inseridos: {len(df)}")

if __name__ == "__main__":
    main() 