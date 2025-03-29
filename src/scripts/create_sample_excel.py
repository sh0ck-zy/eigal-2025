import os
import pandas as pd
import numpy as np

def create_sample_excel(output_path):
    """
    Cria um arquivo Excel de exemplo com dados fictícios 
    de desperdício para diferentes tipos de impressão e tiragens.
    """
    # Definir tipos de impressão
    print_types = ['1/0', '1/1', '2/0', '2/2', '4/0', '4/4', '5/0', '5/5']
    
    # Definir tamanhos de tiragem
    run_lengths = [500, 1000, 2000, 3000, 5000, 10000]
    
    # Preparar dados
    data = []
    
    # Para cada tipo de impressão e tiragem, criar um registro
    for pt in print_types:
        for run in run_lengths:
            # Calcular desperdício fictício baseado no tipo e na tiragem
            # Lógica: tipos com mais cores têm mais desperdício
            base_waste = 20  # desperdício base
            
            # Fator por tipo (mais cores = mais desperdício)
            type_factor = 1.0
            if '1/' in pt:
                type_factor = 0.5
            elif '2/' in pt:
                type_factor = 0.75
            elif '4/' in pt:
                type_factor = 1.0
            elif '5/' in pt:
                type_factor = 1.2
            
            # Fator frente-e-verso (mais desperdício)
            verso_factor = 1.0
            if pt.endswith('/0'):  # apenas frente
                verso_factor = 1.0
            else:  # frente e verso
                verso_factor = 1.3
            
            # Fator de escala (tiragens maiores têm menor % de desperdício)
            scale_factor = np.sqrt(run / 1000)
            
            # Calcular desperdício final com alguma aleatoriedade
            waste = int(base_waste * type_factor * verso_factor * scale_factor * (0.9 + 0.2 * np.random.random()))
            
            # Adicionar registro
            data.append({
                'print_type': pt,
                'run_length': run,
                'waste_sheets': waste
            })
    
    # Criar DataFrame
    df = pd.DataFrame(data)
    
    # Salvar para Excel
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False)
    
    print(f"Arquivo de exemplo criado: {output_path}")
    print(f"Contém {len(data)} registros para {len(print_types)} tipos de impressão e {len(run_lengths)} tamanhos de tiragem.")

if __name__ == "__main__":
    output_path = os.path.join('dados', 'quantidades_exemplo.xlsx')
    create_sample_excel(output_path) 