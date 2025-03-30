#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para comparar dados do arquivo CSV com o banco de dados
"""

import os
import sys
import pandas as pd
import sqlite3
from pathlib import Path
import numpy as np

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
    
    # Carregar dados do banco de dados
    print("Carregando dados do banco de dados...")
    db_df = pd.read_sql_query("SELECT print_type, run_length, waste_sheets FROM quantities", conn)
    print(f"Total de registros do banco de dados: {len(db_df)}")
    
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
        csv_df = pd.read_csv(csv_path)
        print(f"Total de registros do CSV: {len(csv_df)}")
        
        # Verificar colunas
        print(f"Colunas do banco de dados: {list(db_df.columns)}")
        print(f"Colunas do CSV: {list(csv_df.columns)}")
        
        # Verificar se as colunas existem no CSV
        required_columns = ['print_type', 'run_length', 'waste_sheets']
        if all(col in csv_df.columns for col in required_columns):
            print("✅ Todas as colunas necessárias estão presentes no CSV.")
            
            # Garantir que os tipos de dados estão corretos
            csv_df['run_length'] = csv_df['run_length'].astype(int)
            csv_df['waste_sheets'] = csv_df['waste_sheets'].astype(int)
            db_df['run_length'] = db_df['run_length'].astype(int)
            db_df['waste_sheets'] = db_df['waste_sheets'].astype(int)
            
            # Ordenar DataFrames para facilitar a comparação
            db_df_sorted = db_df.sort_values(by=['print_type', 'run_length']).reset_index(drop=True)
            csv_df_sorted = csv_df[required_columns].sort_values(by=['print_type', 'run_length']).reset_index(drop=True)
            
            # Comparação inicial - tamanho
            print("\nComparando registros:")
            print(f"Banco de dados: {len(db_df_sorted)} registros")
            print(f"CSV: {len(csv_df_sorted)} registros")
            
            if len(db_df_sorted) == len(csv_df_sorted):
                print("✅ Mesmo número de registros.")
                
                # Verificar se são idênticos - mostrando o DataFrame de diferenças
                diff_df = pd.DataFrame()
                identical = True
                
                for col in required_columns:
                    is_equal = db_df_sorted[col].equals(csv_df_sorted[col])
                    print(f"Coluna '{col}': {'✅ IGUAL' if is_equal else '❌ DIFERENTE'}")
                    
                    if not is_equal:
                        identical = False
                        diff_df[f'DB_{col}'] = db_df_sorted[col]
                        diff_df[f'CSV_{col}'] = csv_df_sorted[col]
                        diff_df[f'Diff_{col}'] = np.where(db_df_sorted[col] == csv_df_sorted[col], 
                                                         "", 
                                                         f"DB={db_df_sorted[col]} CSV={csv_df_sorted[col]}")
                
                if identical:
                    print("\n✅ Os dados do banco de dados e do CSV são IDÊNTICOS!")
                else:
                    print("\n❌ Os dados do banco de dados e do CSV são DIFERENTES!")
                    
                    # Exibir apenas as linhas com diferenças
                    has_diff = diff_df.filter(like='Diff_').apply(lambda x: x != "", axis=1).any(axis=1)
                    if has_diff.any():
                        print("\nLinhas com diferenças:")
                        print(diff_df.loc[has_diff])
                    else:
                        print("\nNenhuma diferença específica encontrada, pode ser um problema de tipo de dado.")
                        
                    # Analisar possíveis problemas de tipo de dado
                    print("\nTipos de dados nas colunas:")
                    print(f"Banco de dados: {db_df_sorted.dtypes}")
                    print(f"CSV: {csv_df_sorted.dtypes}")
                    
                    # Verificar valores nas primeiras linhas para comparação
                    print("\nAmostras das primeiras 5 linhas:")
                    sample_df = pd.DataFrame({
                        'DB_print_type': db_df_sorted['print_type'].head(),
                        'CSV_print_type': csv_df_sorted['print_type'].head(),
                        'DB_run_length': db_df_sorted['run_length'].head(),
                        'CSV_run_length': csv_df_sorted['run_length'].head(),
                        'DB_waste_sheets': db_df_sorted['waste_sheets'].head(),
                        'CSV_waste_sheets': csv_df_sorted['waste_sheets'].head()
                    })
                    print(sample_df)
            else:
                print("❌ Número diferente de registros!")
                
                # Encontrar registros extras/faltantes
                print("\nVerificando registros diferentes...")
                
                # Criar tuplas para comparação
                db_tuples = set([tuple(row) for row in db_df_sorted[required_columns].values])
                csv_tuples = set([tuple(row) for row in csv_df_sorted[required_columns].values])
                
                # Registros presentes no BD mas não no CSV
                only_in_db = db_tuples - csv_tuples
                if only_in_db:
                    print(f"\n❌ {len(only_in_db)} registros estão no banco de dados mas NÃO no CSV:")
                    only_in_db_df = pd.DataFrame([list(row) for row in only_in_db], columns=required_columns)
                    print(only_in_db_df.head(10))  # Mostrar apenas os primeiros 10
                
                # Registros presentes no CSV mas não no BD
                only_in_csv = csv_tuples - db_tuples
                if only_in_csv:
                    print(f"\n❌ {len(only_in_csv)} registros estão no CSV mas NÃO no banco de dados:")
                    only_in_csv_df = pd.DataFrame([list(row) for row in only_in_csv], columns=required_columns)
                    print(only_in_csv_df.head(10))  # Mostrar apenas os primeiros 10
        else:
            missing_cols = [col for col in required_columns if col not in csv_df.columns]
            print(f"❌ Colunas ausentes no CSV: {missing_cols}")
    except Exception as e:
        print(f"Erro ao processar o arquivo CSV: {str(e)}")
    
    # Fechar a conexão
    conn.close()

if __name__ == "__main__":
    main() 