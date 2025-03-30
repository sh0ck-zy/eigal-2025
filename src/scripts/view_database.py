#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para visualizar o banco de dados SQLite com pandas
"""

import os
import sys
import pandas as pd
import sqlite3
from pathlib import Path

# Ajustar o caminho de importação para poder importar módulos da aplicação
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config.settings import get_settings

def main():
    # Obter o caminho do arquivo de banco de dados
    settings = get_settings()
    db_path = settings.database_url.replace("sqlite:///", "")
    
    print(f"Conectando ao banco de dados: {db_path}")
    
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    
    # Listar todas as tabelas no banco de dados
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tabelas disponíveis no banco de dados:")
    for table in tables:
        print(f"- {table[0]}")
    
    # Exibir o conteúdo da tabela de quantidades
    print("\nConteúdo da tabela 'quantities':")
    df = pd.read_sql_query("SELECT * FROM quantities", conn)
    print(df)
    
    # Exibir estatísticas básicas
    print("\nEstatísticas da tabela 'quantities':")
    print(df.describe())
    
    # Agrupar por tipo de impressão para ver a distribuição
    print("\nDistribuição por tipo de impressão:")
    print(df.groupby('print_type').agg({
        'id': 'count',
        'run_length': ['min', 'max', 'mean'],
        'waste_sheets': ['min', 'max', 'mean']
    }))
    
    # Verificar a razão de desperdício (desperdício/tiragem)
    df['waste_ratio'] = df['waste_sheets'] / df['run_length']
    print("\nRazão de desperdício (waste_sheets/run_length):")
    print(df[['print_type', 'run_length', 'waste_sheets', 'waste_ratio']].sort_values('waste_ratio'))
    
    # Fechar a conexão
    conn.close()

if __name__ == "__main__":
    main() 