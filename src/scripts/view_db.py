import sys
import os

# Adicionar diretório raiz ao path para importar os módulos corretamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, Base, engine
from app.models.quantities import Quantity, PrintType

def view_database():
    """
    Exibe o conteúdo do banco de dados (tipos de impressão e quantidades).
    """
    # Cria uma sessão
    db = SessionLocal()
    
    try:
        # Exibir tipos de impressão
        print("=== TIPOS DE IMPRESSÃO ===")
        print_types = db.query(PrintType).all()
        for pt in print_types:
            print(f"ID: {pt.id}, Nome: {pt.name}")
        
        print(f"\nTotal: {len(print_types)} tipos de impressão\n")
        
        # Exibir quantidades
        print("=== REGISTROS DE QUANTIDADES ===")
        quantities = db.query(Quantity).all()
        
        for q in quantities:
            special_mark = " [ESPECIAL]" if q.is_special_case else ""
            adjustment_text = f", Ajuste: {q.adjustment}" if q.adjustment else ""
            
            print(f"ID: {q.id}, Tipo: {q.print_type}, Tiragem: {q.run_length}, " +
                  f"Desperdício: {q.waste_sheets} folhas{adjustment_text}{special_mark}")
        
        print(f"\nTotal: {len(quantities)} registros de quantidade")
    
    except Exception as e:
        print(f"Erro ao consultar banco de dados: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    view_database() 