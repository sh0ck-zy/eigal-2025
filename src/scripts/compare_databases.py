#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para comparar os dois bancos de dados - o original e o completo
"""

import os
import sqlite3
import pandas as pd
from tabulate import tabulate

def main():
    # Caminhos para os bancos de dados
    db_original = 'waste_calculation.db'
    db_complete = 'waste_calculation_complete.db'
    
    # Verificar se os arquivos existem
    if not os.path.exists(db_original):
        print(f"Banco de dados original não encontrado: {db_original}")
        return
    
    if not os.path.exists(db_complete):
        print(f"Banco de dados completo não encontrado: {db_complete}")
        return
    
    print(f"Comparando os bancos de dados:\n- Original: {db_original}\n- Completo: {db_complete}")
    
    # Conectar aos bancos de dados
    conn_original = sqlite3.connect(db_original)
    conn_complete = sqlite3.connect(db_complete)
    
    # Obter informações sobre tabelas
    def get_tables(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in cursor.fetchall()]
    
    tables_original = get_tables(conn_original)
    tables_complete = get_tables(conn_complete)
    
    print("\n=== Tabelas Encontradas ===")
    print(f"Original: {', '.join(tables_original)}")
    print(f"Completo: {', '.join(tables_complete)}")
    
    # Comparar estrutura das tabelas comuns
    common_tables = [table for table in tables_original if table in tables_complete]
    print(f"\n=== Estrutura das Tabelas Comuns ({len(common_tables)}) ===")
    
    for table in common_tables:
        print(f"\nTabela: {table}")
        
        # Obter estrutura da tabela
        def get_table_schema(conn, table_name):
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name});")
            return cursor.fetchall()
        
        schema_original = get_table_schema(conn_original, table)
        schema_complete = get_table_schema(conn_complete, table)
        
        # Formatar como DataFrames para comparação mais fácil
        df_original = pd.DataFrame(schema_original, columns=['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk'])
        df_complete = pd.DataFrame(schema_complete, columns=['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk'])
        
        # Mostrar apenas nome e tipo para simplificar
        cols_original = df_original[['name', 'type']].sort_values('name')
        cols_complete = df_complete[['name', 'type']].sort_values('name')
        
        print("Original:")
        for _, row in cols_original.iterrows():
            print(f"  - {row['name']} ({row['type']})")
        
        print("\nCompleto:")
        for _, row in cols_complete.iterrows():
            print(f"  - {row['name']} ({row['type']})")
        
        # Verificar colunas adicionais ou removidas
        original_cols = set(cols_original['name'])
        complete_cols = set(cols_complete['name'])
        
        if original_cols - complete_cols:
            print(f"\nColunas em Original mas não em Completo: {', '.join(original_cols - complete_cols)}")
        
        if complete_cols - original_cols:
            print(f"\nColunas em Completo mas não em Original: {', '.join(complete_cols - original_cols)}")
    
    # Comparar contagem de registros
    print("\n=== Contagem de Registros ===")
    
    for table in common_tables:
        cursor_original = conn_original.cursor()
        cursor_complete = conn_complete.cursor()
        
        cursor_original.execute(f"SELECT COUNT(*) FROM {table};")
        count_original = cursor_original.fetchone()[0]
        
        cursor_complete.execute(f"SELECT COUNT(*) FROM {table};")
        count_complete = cursor_complete.fetchone()[0]
        
        print(f"Tabela {table}:")
        print(f"  - Original: {count_original:,} registros")
        print(f"  - Completo: {count_complete:,} registros")
        
        if table == 'quantities':
            # Verificar quantos tipos de impressão existem
            cursor_original.execute("SELECT COUNT(DISTINCT print_type) FROM quantities;")
            pt_count_original = cursor_original.fetchone()[0]
            
            cursor_complete.execute("SELECT COUNT(DISTINCT print_type) FROM quantities;")
            pt_count_complete = cursor_complete.fetchone()[0]
            
            print(f"\nTipos de impressão únicos:")
            print(f"  - Original: {pt_count_original}")
            print(f"  - Completo: {pt_count_complete}")
            
            # Verificar quantas tiragens diferentes existem
            cursor_original.execute("SELECT COUNT(DISTINCT run_length) FROM quantities;")
            rl_count_original = cursor_original.fetchone()[0]
            
            cursor_complete.execute("SELECT COUNT(DISTINCT run_length) FROM quantities;")
            rl_count_complete = cursor_complete.fetchone()[0]
            
            print(f"\nTiragens únicas:")
            print(f"  - Original: {rl_count_original}")
            print(f"  - Completo: {rl_count_complete}")
            
            # Comparar valores específicos
            print("\nComparando registros com mesmas combinações de tipo/tiragem:")
            
            # Pegar alguns exemplos do original
            cursor_original.execute("""
                SELECT print_type, run_length, waste_sheets 
                FROM quantities 
                ORDER BY print_type, run_length
                LIMIT 10;
            """)
            samples_original = cursor_original.fetchall()
            
            # Verificar os mesmos no completo
            comparison_data = []
            for pt, rl, ws_original in samples_original:
                cursor_complete.execute("""
                    SELECT waste_sheets FROM quantities 
                    WHERE print_type = ? AND run_length = ? 
                    LIMIT 1;
                """, (pt, rl))
                result = cursor_complete.fetchone()
                
                if result:
                    ws_complete = result[0]
                    match = ws_original == ws_complete
                    comparison_data.append([pt, rl, ws_original, ws_complete, match])
                else:
                    comparison_data.append([pt, rl, ws_original, "Não encontrado", False])
            
            # Exibir a comparação em formato tabular
            headers = ["Tipo", "Tiragem", "Desperdício (Original)", "Desperdício (Completo)", "Match"]
            print(tabulate(comparison_data, headers=headers, tablefmt="simple"))
    
    # Fechar conexões
    conn_original.close()
    conn_complete.close()

if __name__ == "__main__":
    main() 