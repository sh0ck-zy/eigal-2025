# app/models/quantities.py
from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class Quantity(Base):
    __tablename__ = 'quantities'
    
    id = Column(Integer, primary_key=True, index=True)
    print_type = Column(String(10), nullable=False)  # ex: "4/0", "4/4", "2/2"
    run_length = Column(Integer, nullable=False)     # quantidade a ser impressa (renomeado para corresponder ao Excel)
    waste_sheets = Column(Integer, nullable=False)   # desperdício esperado em folhas (renomeado para corresponder ao Excel)
    adjustment = Column(String(20), nullable=True)   # ajustes necessários
    is_special_case = Column(Boolean, default=False) # flag para casos especiais
    
    def to_dict(self):
        return {
            'id': self.id,
            'print_type': self.print_type,
            'print_run': self.run_length,      # mantemos a API compatível
            'waste_amount': self.waste_sheets, # mantemos a API compatível
            'adjustment': self.adjustment,
            'is_special_case': self.is_special_case
        }


class PrintType(Base):
    __tablename__ = 'print_types'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10), nullable=False, unique=True)  # ex: "4/0", "4/4", "2/2"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }