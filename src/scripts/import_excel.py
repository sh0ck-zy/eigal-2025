import os
import sys
import pandas as pd
from sqlalchemy.orm import Session

# Adicionar diretório raiz ao path para importar os módulos corretamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, Base, engine
from app.models.quantities import Quantity, PrintType

def import_from_excel(excel_path):
    """
    Importa dados de uma planilha Excel para o banco de dados.
    
    A planilha deve ter as seguintes colunas:
    - print_type: Tipo de impressão (ex: 4/0, 4/4)
    - run_length: Comprimento da tiragem
    - waste_sheets: Quantidade de folhas desperdiçadas
    """
    try:
        # Verificar se o arquivo existe
        if not os.path.exists(excel_path):
            print(f"Erro: Arquivo '{excel_path}' não encontrado.")
            return False
        
        # Ler a planilha Excel
        print(f"Lendo dados do arquivo: {excel_path}")
        df = pd.read_excel(excel_path)
        
        # Verificar colunas necessárias
        required_columns = ['print_type', 'run_length', 'waste_sheets']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Erro: Colunas obrigatórias não encontradas: {', '.join(missing_columns)}")
            print(f"Colunas disponíveis: {', '.join(df.columns)}")
            return False
        
        # Abrir sessão do banco de dados
        db = SessionLocal()
        
        try:
            # Apagar registros existentes (opcional)
            print("Limpando registros existentes...")
            db.query(Quantity).delete()
            db.query(PrintType).delete()
            
            # Conjunto para armazenar tipos de impressão únicos
            print_types = set()
            
            # Processar cada linha da planilha
            print("Importando dados para o banco...")
            for _, row in df.iterrows():
                print_type = str(row['print_type']).strip()
                run_length = int(row['run_length'])
                waste_sheets = int(row['waste_sheets'])
                
                # Adicionar tipo de impressão único
                print_types.add(print_type)
                
                # Criar registro de quantidade
                quantity = Quantity(
                    print_type=print_type,
                    run_length=run_length,
                    waste_sheets=waste_sheets
                )
                db.add(quantity)
            
            # Criar registros de tipos de impressão únicos
            for pt in print_types:
                print_type = PrintType(name=pt)
                db.add(print_type)
            
            # Confirmar transação
            db.commit()
            print(f"Importação concluída! {len(df)} registros de quantidades e {len(print_types)} tipos de impressão importados.")
            return True
        
        except Exception as e:
            db.rollback()
            print(f"Erro durante a importação: {str(e)}")
            return False
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"Erro ao processar o arquivo Excel: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python import_excel.py <caminho_para_excel>")
        print("Exemplo: python import_excel.py ../dados/quantidades.xlsx")
        sys.exit(1)
    
    excel_path = sys.argv[1]
    success = import_from_excel(excel_path)
    
    if success:
        print("Importação concluída com sucesso!")
    else:
        print("Importação falhou. Verifique os erros acima.")
        sys.exit(1) 