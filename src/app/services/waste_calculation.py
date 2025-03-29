# app/services/waste_calculation.py
from fastapi import Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.repositories.quantity_repository import QuantityRepository
from app.schemas.quantity import WasteCalculationRequest, WasteCalculationResponse
from app.core.database import get_db
from app.core.exceptions import NotFoundException


class WasteCalculationService:
    def __init__(self, repository: QuantityRepository):
        self.repository = repository
    
    def calculate_waste(self, request: WasteCalculationRequest) -> WasteCalculationResponse:
        """Calcula o desperdício com base no tipo de impressão e quantidade."""
        # Busca o registro correspondente
        quantity = self.repository.find_by_print_type_and_run(
            request.print_type, request.print_run
        )
        
        if not quantity:
            raise NotFoundException(
                detail=f"Nenhum cálculo encontrado para tipo {request.print_type} com tiragem {request.print_run}"
            )
        
        # Retorna o resultado mapeado para o DTO de resposta
        return WasteCalculationResponse(
            print_type=quantity.print_type,
            print_run=request.print_run,
            waste_amount=quantity.waste_sheets,
            adjustment=quantity.adjustment,
            is_special_case=quantity.is_special_case
        )
    
    def get_print_types(self) -> List[str]:
        """Retorna todos os tipos de impressão disponíveis."""
        return self.repository.find_all_print_types()


# Provider para injeção de dependência
def get_waste_calculation_service(db: Session = Depends(get_db)) -> WasteCalculationService:
    """
    Factory function para criar e injetar uma instância do WasteCalculationService.
    Esta função é usada pelo sistema de injeção de dependência do FastAPI.
    """
    repository = QuantityRepository(db)
    return WasteCalculationService(repository) 