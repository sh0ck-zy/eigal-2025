# app/repositories/quantity_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.quantities import Quantity, PrintType


class QuantityRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def find_by_print_type_and_run(self, print_type: str, print_run: int) -> Optional[Quantity]:
        """
        Busca o registro de quantidade para o tipo de impressão e tiragem fornecidos.
        Encontra o registro com menor tiragem que seja maior ou igual à tiragem solicitada.
        """
        return self.db_session.query(Quantity)\
            .filter(Quantity.print_type == print_type)\
            .filter(Quantity.run_length >= print_run)\
            .order_by(Quantity.run_length)\
            .first()
    
    def find_all_print_types(self) -> List[str]:
        """
        Retorna todos os tipos de impressão disponíveis.
        Utiliza a tabela de tipos de impressão se disponível, caso contrário,
        obtém os tipos distintos da tabela de quantidades.
        """
        # Tentar obter da tabela PrintType primeiro
        result = self.db_session.query(PrintType.name).all()
        
        if result:
            return [r[0] for r in result]
        
        # Fallback para consulta anterior caso a tabela PrintType esteja vazia
        result = self.db_session.query(Quantity.print_type)\
            .distinct()\
            .all()
        
        return [r[0] for r in result] 