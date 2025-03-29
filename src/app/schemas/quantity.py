# app/schemas/quantity.py
from pydantic import BaseModel, Field
from typing import Optional


# Request DTO
class WasteCalculationRequest(BaseModel):
    print_type: str = Field(..., description="Tipo de impressão (ex: 4/0, 4/4)")
    print_run: int = Field(..., gt=0, description="Quantidade a ser impressa")


# Response DTO
class WasteCalculationResponse(BaseModel):
    print_type: str
    print_run: int
    waste_amount: int
    adjustment: Optional[str] = None
    is_special_case: bool = False
    
    class Config:
        orm_mode = True  # Compatibilidade com versões anteriores do Pydantic
        from_attributes = True  # Nova forma recomendada para Pydantic v2 