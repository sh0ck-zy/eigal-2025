#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script simples para ler e exibir o arquivo Excel de quantidades
"""

import pandas as pd
import os
from pathlib import Path

def main():
    # Caminho para o arquivo Excel
    excel_path = os.path.join('dados', 'quantidades_exemplo.xlsx')
    
    print(f"Tentando ler o arquivo: {excel_path}")
    
    # Verificar se o arquivo existe
    if not os.path.exists(excel_path):
        alt_path = os.path.join('..', 'dados', 'quantidades_exemplo.xlsx')
        print(f"Arquivo não encontrado. Tentando caminho alternativo: {alt_path}")
        if os.path.exists(alt_path):
            excel_path = alt_path
        else:
            print("Arquivo Excel não encontrado!")
            return
    
    # Ler o arquivo Excel
    try:
        # Ler todas as abas do arquivo Excel
        xl = pd.ExcelFile(excel_path)
        print(f"Abas disponíveis no arquivo: {xl.sheet_names}")
        
        # Ler cada aba
        for sheet_name in xl.sheet_names:
            print(f"\n=== Conteúdo da aba '{sheet_name}' ===")
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            # Exibir informações sobre o DataFrame
            print(f"Forma: {df.shape} (linhas, colunas)")
            print(f"Colunas: {list(df.columns)}")
            
            # Exibir as primeiras linhas
            print("\nPrimeiras 5 linhas:")
            print(df.head())
            
            # Verificar valores únicos para cada coluna
            print("\nValores únicos por coluna:")
            for col in df.columns:
                unique_values = df[col].unique()
                if len(unique_values) <= 10:  # Mostrar somente se houver poucos valores únicos
                    print(f"  {col}: {sorted(unique_values)}")
                else:
                    print(f"  {col}: {len(unique_values)} valores únicos")
    
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {str(e)}")

if __name__ == "__main__":
    main() 