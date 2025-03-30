#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para comparar os dados do banco de dados com arquivo Excel
"""

import os
import sys
import pandas as pd
import sqlite3
from pathlib import Path
import glob

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
    db_df = pd.read_sql_query("SELECT * FROM quantities", conn)
    print(f"Total de registros do banco de dados: {len(db_df)}")
    
    # Tentar encontrar arquivos Excel na pasta de dados
    excel_files = glob.glob(os.path.join("dados", "*.xlsx"))
    if not excel_files:
        excel_files = glob.glob(os.path.join("..", "dados", "*.xlsx"))
    
    if not excel_files:
        print("Nenhum arquivo Excel encontrado na pasta 'dados'")
        print("Por favor, especifique o caminho do arquivo Excel:")
        excel_path = input("> ")
    else:
        print("Arquivos Excel encontrados:")
        for i, file in enumerate(excel_files):
            print(f"{i+1}. {file}")
        
        if len(excel_files) == 1:
            excel_path = excel_files[0]
        else:
            print("Selecione o número do arquivo Excel para comparação:")
            selection = int(input("> "))
            excel_path = excel_files[selection-1]
    
    print(f"Carregando dados do Excel: {excel_path}")
    
    # Tentar carregar dados do Excel
    try:
        # Primeiro tentar encontrar a aba correta
        xl = pd.ExcelFile(excel_path)
        sheets = xl.sheet_names
        
        print("Abas disponíveis no Excel:")
        for i, sheet in enumerate(sheets):
            print(f"{i+1}. {sheet}")
        
        if len(sheets) == 1:
            sheet_name = sheets[0]
        else:
            print("Selecione o número da aba para comparação:")
            selection = int(input("> "))
            sheet_name = sheets[selection-1]
        
        print(f"Carregando aba '{sheet_name}'...")
        excel_df = pd.read_excel(excel_path, sheet_name=sheet_name)
        
        # Mostrar as primeiras linhas para verificar a estrutura
        print("\nPrimeiras linhas do Excel:")
        print(excel_df.head())
        
        # Pedir as colunas para mapeamento
        print("\nInforme os nomes das colunas do Excel que correspondem às colunas do banco de dados:")
        
        columns_mapping = {}
        db_columns = ['print_type', 'run_length', 'waste_sheets']
        
        for col in db_columns:
            print(f"Coluna do banco de dados: {col}")
            print("Colunas disponíveis no Excel:", ", ".join(excel_df.columns))
            excel_col = input(f"Informe o nome da coluna correspondente no Excel (ou deixe vazio para pular): ")
            if excel_col:
                columns_mapping[col] = excel_col
        
        # Comparar dados
        print("\nComparando dados...")
        
        # Verificar se todas as colunas necessárias foram mapeadas
        if set(db_columns).issubset(set(columns_mapping.keys())):
            # Mapear colunas do Excel para o formato do banco de dados
            excel_mapped = excel_df.rename(columns={v: k for k, v in columns_mapping.items()})
            
            # Selecionar apenas as colunas relevantes
            excel_compare = excel_mapped[db_columns].copy()
            db_compare = db_df[db_columns].copy()
            
            # Ordenar ambos os DataFrames para facilitar a comparação
            excel_compare = excel_compare.sort_values(by=['print_type', 'run_length']).reset_index(drop=True)
            db_compare = db_compare.sort_values(by=['print_type', 'run_length']).reset_index(drop=True)
            
            # Comparar registros
            print("\nRegistros no Excel:", len(excel_compare))
            print("Registros no banco de dados:", len(db_compare))
            
            # Verificar se os DataFrames têm o mesmo tamanho
            if len(excel_compare) == len(db_compare):
                # Verificar se os DataFrames são iguais
                if excel_compare.equals(db_compare):
                    print("\n✅ Os dados do Excel e do banco de dados são IDÊNTICOS!")
                else:
                    print("\n❌ Os dados do Excel e do banco de dados são DIFERENTES!")
                    
                    # Encontrar diferenças
                    diff = pd.concat([db_compare, excel_compare]).drop_duplicates(keep=False)
                    print("\nRegistros diferentes:")
                    print(diff)
                    
                    # Comparação mais detalhada, coluna por coluna
                    for col in db_columns:
                        equals = db_compare[col].equals(excel_compare[col])
                        print(f"Coluna '{col}': {'✅ IGUAL' if equals else '❌ DIFERENTE'}")
                        
                        if not equals:
                            # Encontrar índices onde os valores são diferentes
                            diff_idx = db_compare[col] != excel_compare[col]
                            diff_count = diff_idx.sum()
                            print(f"  Encontradas {diff_count} diferenças")
                            
                            if diff_count <= 10:  # Mostrar apenas primeiras 10 diferenças
                                for idx in diff_idx[diff_idx].index:
                                    print(f"  - Registro {idx}: DB={db_compare.loc[idx, col]} vs Excel={excel_compare.loc[idx, col]}")
            else:
                print("\n❌ Números de registros diferentes!")
                
                # Verificar registros extras/faltantes
                db_set = set(db_compare.apply(tuple, axis=1))
                excel_set = set(excel_compare.apply(tuple, axis=1))
                
                missing_in_excel = db_set - excel_set
                extra_in_excel = excel_set - db_set
                
                if missing_in_excel:
                    print(f"\nRegistros no banco de dados que NÃO estão no Excel ({len(missing_in_excel)}):")
                    missing_df = pd.DataFrame([list(row) for row in missing_in_excel], columns=db_columns)
                    print(missing_df)
                
                if extra_in_excel:
                    print(f"\nRegistros no Excel que NÃO estão no banco de dados ({len(extra_in_excel)}):")
                    extra_df = pd.DataFrame([list(row) for row in extra_in_excel], columns=db_columns)
                    print(extra_df)
        else:
            print("❌ Não foi possível mapear todas as colunas necessárias para comparação.")
    
    except Exception as e:
        print(f"Erro ao processar o arquivo Excel: {str(e)}")
    
    # Fechar a conexão
    conn.close()

if __name__ == "__main__":
    main() 