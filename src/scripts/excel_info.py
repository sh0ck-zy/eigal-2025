#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para mostrar informações do arquivo Excel de quantidades
"""

import os
import pandas as pd

def main():
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
        # Ler o arquivo Excel
        # Verificar se há várias planilhas
        excel = pd.ExcelFile(excel_path)
        print(f"Planilhas disponíveis: {excel.sheet_names}")
        
        total_rows = 0
        
        # Ler cada planilha e mostrar informações
        for sheet_name in excel.sheet_names:
            print(f"\n{'=' * 50}")
            print(f"Planilha: {sheet_name}")
            print(f"{'=' * 50}")
            
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            total_rows += len(df)
            
            print(f"Total de linhas: {len(df)}")
            print(f"Colunas: {list(df.columns)}")
            print("\nPrimeiras 5 linhas:")
            print(df.head())
            
            print("\nInformações sobre os dados:")
            print(df.info())
            
            # Verificar se existem as colunas que estamos procurando
            expected_columns = ['print_type', 'run_length', 'waste_sheets']
            missing_columns = [col for col in expected_columns if col not in df.columns]
            
            if missing_columns:
                print(f"\nColunas esperadas que não estão presentes: {missing_columns}")
                
                # Se não temos as colunas esperadas, vamos tentar identificar colunas similares
                print("\nColunas disponíveis que podem ser relevantes:")
                for col in df.columns:
                    print(f"  - {col}")
                    # Mostrar os primeiros valores únicos para cada coluna para ajudar na identificação
                    try:
                        unique_values = df[col].dropna().unique()[:5]
                        print(f"    Valores únicos (max 5): {unique_values}")
                    except:
                        print("    Não foi possível mostrar valores únicos")
            else:
                print("\nTodas as colunas esperadas estão presentes na planilha.")
                
                # Se as colunas esperadas estão presentes, mostrar estatísticas básicas
                print("\nEstatísticas básicas:")
                print(df[expected_columns].describe())
                
                # Mostrar quantos tipos de impressão diferentes existem
                print(f"\nTipos de impressão únicos ({len(df['print_type'].unique())}):")
                print(df['print_type'].value_counts().head(10))
                
                # Mostrar as tiragens disponíveis
                print(f"\nTiragens disponíveis ({len(df['run_length'].unique())}):")
                print(sorted(df['run_length'].unique()))
        
        print(f"\nTotal de linhas em todas as planilhas: {total_rows}")
        
    except Exception as e:
        print(f"Erro ao processar o arquivo Excel: {str(e)}")

if __name__ == "__main__":
    main() 