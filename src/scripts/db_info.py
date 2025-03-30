#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para mostrar informações do banco de dados SQLite
"""

import os
import sqlite3
from pathlib import Path

def main():
    # Tenta encontrar o arquivo do banco de dados
    db_path = 'waste_calculation.db'
    
    if not os.path.exists(db_path):
        alt_path = os.path.join('..', 'waste_calculation.db')
        print(f"Arquivo não encontrado. Tentando caminho alternativo: {alt_path}")
        if os.path.exists(alt_path):
            db_path = alt_path
        else:
            print("Arquivo do banco de dados não encontrado!")
            return
    
    print(f"Usando banco de dados: {db_path}")
    
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Listar todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"Tabelas encontradas no banco de dados ({len(tables)}):")
        for table in tables:
            table_name = table[0]
            print(f"\n{'=' * 50}")
            print(f"Tabela: {table_name}")
            print(f"{'=' * 50}")
            
            # Obter estrutura da tabela
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print("\nEstrutura da tabela:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"\nTotal de registros: {count}")
            
            # Mostrar amostra dos dados
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
            rows = cursor.fetchall()
            
            if rows:
                print("\nPrimeiros 5 registros:")
                for row in rows:
                    print(f"  {row}")
                
                # Se for a tabela de quantidades, mostrar mais informações
                if table_name.lower() == 'quantities':
                    # Verificar tipos de impressão
                    cursor.execute("SELECT DISTINCT print_type FROM quantities;")
                    print_types = cursor.fetchall()
                    print(f"\nTipos de impressão únicos ({len(print_types)}):")
                    for pt in print_types:
                        print(f"  - {pt[0]}")
                    
                    # Verificar tiragens
                    cursor.execute("SELECT DISTINCT run_length FROM quantities ORDER BY run_length;")
                    run_lengths = cursor.fetchall()
                    print(f"\nTiragens disponíveis ({len(run_lengths)}):")
                    print(f"  {[r[0] for r in run_lengths]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Erro ao processar o banco de dados: {str(e)}")

if __name__ == "__main__":
    main() 