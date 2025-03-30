#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para comparar dados do banco de dados com o Excel sem interação do usuário
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
    
    # Carregar dados do banco de dados
    print("Carregando dados do banco de dados...")
    db_df = pd.read_sql_query("SELECT print_type, run_length, waste_sheets FROM quantities", conn)
    print(f"Total de registros do banco de dados: {len(db_df)}")
    
    # Caminho para o arquivo Excel
    excel_path = os.path.join('dados', 'quantidades_exemplo.xlsx')
    
    # Verificar se o arquivo existe
    if not os.path.exists(excel_path):
        alt_path = os.path.join('..', 'dados', 'quantidades_exemplo.xlsx')
        print(f"Arquivo não encontrado. Tentando caminho alternativo: {alt_path}")
        if os.path.exists(alt_path):
            excel_path = alt_path
        else:
            print("Arquivo Excel não encontrado!")
            return
    
    print(f"Carregando dados do Excel: {excel_path}")
    try:
        # Ler o arquivo Excel - assumindo que está na primeira aba
        excel_df = pd.read_excel(excel_path)
        print(f"Total de registros do Excel: {len(excel_df)}")
        
        # Verificar colunas
        print(f"Colunas do banco de dados: {list(db_df.columns)}")
        print(f"Colunas do Excel: {list(excel_df.columns)}")
        
        # Verificar se as colunas existem no Excel
        required_columns = ['print_type', 'run_length', 'waste_sheets']
        if all(col in excel_df.columns for col in required_columns):
            print("✅ Todas as colunas necessárias estão presentes no Excel.")
            
            # Ordenar DataFrames para facilitar a comparação
            db_df_sorted = db_df.sort_values(by=['print_type', 'run_length']).reset_index(drop=True)
            excel_df_sorted = excel_df[required_columns].sort_values(by=['print_type', 'run_length']).reset_index(drop=True)
            
            # Comparação inicial - tamanho
            print("\nComparando registros:")
            print(f"Banco de dados: {len(db_df_sorted)} registros")
            print(f"Excel: {len(excel_df_sorted)} registros")
            
            if len(db_df_sorted) == len(excel_df_sorted):
                print("✅ Mesmo número de registros.")
                
                # Verificar se os DataFrames são idênticos
                if db_df_sorted.equals(excel_df_sorted):
                    print("\n✅ Os dados do banco de dados e do Excel são IDÊNTICOS!")
                else:
                    print("\n❌ Os dados do banco de dados e do Excel são DIFERENTES!")
                    
                    # Analisar coluna por coluna
                    for col in required_columns:
                        if db_df_sorted[col].equals(excel_df_sorted[col]):
                            print(f"✅ Coluna '{col}': Dados idênticos")
                        else:
                            print(f"❌ Coluna '{col}': Existem diferenças")
                            
                            # Contar diferenças
                            diff_mask = db_df_sorted[col] != excel_df_sorted[col]
                            diff_count = diff_mask.sum()
                            print(f"   {diff_count} diferenças encontradas ({diff_count/len(db_df_sorted)*100:.2f}%)")
                            
                            # Mostrar algumas diferenças (máximo 5)
                            diff_indices = diff_mask[diff_mask].index[:5]
                            if len(diff_indices) > 0:
                                print("   Exemplos de diferenças:")
                                for idx in diff_indices:
                                    print(f"   - Linha {idx}: BD={db_df_sorted.loc[idx, col]} vs Excel={excel_df_sorted.loc[idx, col]}")
            else:
                print("❌ Número diferente de registros!")
                
                # Encontrar registros extras/faltantes
                print("\nVerificando registros diferentes...")
                
                # Criar tuplas para comparação
                db_tuples = set([tuple(row) for row in db_df_sorted[required_columns].values])
                excel_tuples = set([tuple(row) for row in excel_df_sorted[required_columns].values])
                
                # Registros presentes no BD mas não no Excel
                only_in_db = db_tuples - excel_tuples
                if only_in_db:
                    print(f"\n❌ {len(only_in_db)} registros estão no banco de dados mas NÃO no Excel:")
                    only_in_db_df = pd.DataFrame([list(row) for row in only_in_db], columns=required_columns)
                    print(only_in_db_df.head(10))  # Mostrar apenas os primeiros 10
                
                # Registros presentes no Excel mas não no BD
                only_in_excel = excel_tuples - db_tuples
                if only_in_excel:
                    print(f"\n❌ {len(only_in_excel)} registros estão no Excel mas NÃO no banco de dados:")
                    only_in_excel_df = pd.DataFrame([list(row) for row in only_in_excel], columns=required_columns)
                    print(only_in_excel_df.head(10))  # Mostrar apenas os primeiros 10
        else:
            missing_cols = [col for col in required_columns if col not in excel_df.columns]
            print(f"❌ Colunas ausentes no Excel: {missing_cols}")
    except Exception as e:
        print(f"Erro ao processar o arquivo Excel: {str(e)}")
    
    # Fechar a conexão
    conn.close()

if __name__ == "__main__":
    main() 