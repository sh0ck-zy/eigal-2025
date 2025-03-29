# app/models/quantities.py
from app import db

class Quantity(db.Model):
    __tablename__ = 'quantities'
    
    id = db.Column(db.Integer, primary_key=True)
    print_type = db.Column(db.String(10), nullable=False)  # ex: "4/0", "4/4", "2/2"
    print_run = db.Column(db.Integer, nullable=False)      # quantidade a ser impressa
    waste_amount = db.Column(db.Integer, nullable=False)   # desperdício esperado em folhas
    adjustment = db.Column(db.String(20))                  # ajustes necessários
    is_special_case = db.Column(db.Boolean, default=False) # flag para casos especiais
    
    def to_dict(self):
        return {
            'id': self.id,
            'print_type': self.print_type,
            'print_run': self.print_run,
            'waste_amount': self.waste_amount,
            'adjustment': self.adjustment,
            'is_special_case': self.is_special_case
        }