# app/api/routes/quantities.py
from fastapi import APIRouter, Depends, Query
from typing import List

from app.schemas.quantity import WasteCalculationRequest, WasteCalculationResponse
from app.services.waste_calculation import WasteCalculationService, get_waste_calculation_service

router = APIRouter()

@router.get("/print-types", response_model=List[str])
async def get_print_types(
    service: WasteCalculationService = Depends(get_waste_calculation_service)
):
    """Retorna todos os tipos de impressão disponíveis"""
    return service.get_print_types()

@router.post("/waste-calculation", response_model=WasteCalculationResponse)
async def calculate_waste(
    request: WasteCalculationRequest,
    service: WasteCalculationService = Depends(get_waste_calculation_service)
):
    """Calcula o desperdício com base no tipo de impressão e quantidade"""
    return service.calculate_waste(request)

@router.get("/waste-calculation", response_model=WasteCalculationResponse)
async def calculate_waste_get(
    print_type: str = Query(..., description="Tipo de impressão (ex: 4/0, 4/4)"),
    print_run: int = Query(..., gt=0, description="Quantidade a ser impressa"),
    service: WasteCalculationService = Depends(get_waste_calculation_service)
):
    """Calcula o desperdício com base no tipo de impressão e quantidade (via query params)"""
    request = WasteCalculationRequest(print_type=print_type, print_run=print_run)
    return service.calculate_waste(request) 