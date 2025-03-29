# scripts/init_db.py
import sys
import os

# Adiciona o diretório pai ao sys.path para permitir importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal, Base, engine
from app.models.quantities import Quantity, PrintType


def init_database():
    # Cria as tabelas
    Base.metadata.create_all(bind=engine)
    
    # Cria uma sessão
    db = SessionLocal()
    
    try:
        # Remove todos os registros existentes
        db.query(Quantity).delete()
        db.query(PrintType).delete()
        
        # Tipos de impressão
        print_types = ["4/0", "4/4", "2/2"]
        
        # Adicionar tipos de impressão
        for pt in print_types:
            db.add(PrintType(name=pt))
        
        # Dados de exemplo para inicialização
        example_quantities = [
            # Tipo 4/0
            Quantity(print_type="4/0", run_length=500, waste_sheets=30, adjustment=None, is_special_case=False),
            Quantity(print_type="4/0", run_length=1000, waste_sheets=50, adjustment=None, is_special_case=False),
            Quantity(print_type="4/0", run_length=2000, waste_sheets=80, adjustment=None, is_special_case=False),
            Quantity(print_type="4/0", run_length=5000, waste_sheets=150, adjustment=None, is_special_case=False),
            Quantity(print_type="4/0", run_length=10000, waste_sheets=250, adjustment=None, is_special_case=False),
            
            # Tipo 4/4
            Quantity(print_type="4/4", run_length=500, waste_sheets=40, adjustment=None, is_special_case=False),
            Quantity(print_type="4/4", run_length=1000, waste_sheets=70, adjustment=None, is_special_case=False),
            Quantity(print_type="4/4", run_length=2000, waste_sheets=100, adjustment=None, is_special_case=False),
            Quantity(print_type="4/4", run_length=5000, waste_sheets=180, adjustment=None, is_special_case=False),
            Quantity(print_type="4/4", run_length=10000, waste_sheets=300, adjustment=None, is_special_case=False),
            
            # Tipo 2/2
            Quantity(print_type="2/2", run_length=500, waste_sheets=25, adjustment="Ajustar chapas", is_special_case=True),
            Quantity(print_type="2/2", run_length=1000, waste_sheets=45, adjustment="Ajustar chapas", is_special_case=True),
            Quantity(print_type="2/2", run_length=2000, waste_sheets=70, adjustment=None, is_special_case=False),
            Quantity(print_type="2/2", run_length=5000, waste_sheets=120, adjustment=None, is_special_case=False),
            Quantity(print_type="2/2", run_length=10000, waste_sheets=200, adjustment=None, is_special_case=False),
        ]
        
        # Adiciona todos os registros
        db.add_all(example_quantities)
        db.commit()
        
        print(f"Banco de dados inicializado com {len(example_quantities)} registros.")
    
    except Exception as e:
        db.rollback()
        print(f"Erro ao inicializar banco de dados: {e}")
    
    finally:
        db.close()


if __name__ == "__main__":
    init_database() 