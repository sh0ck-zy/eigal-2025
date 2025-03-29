# app/core/exceptions.py
from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    """Exceção base para todas as exceções específicas da aplicação"""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(BaseAppException):
    """Exceção lançada quando um recurso não é encontrado"""
    def __init__(self, detail: str = "Recurso não encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ValidationException(BaseAppException):
    """Exceção lançada quando ocorre um erro de validação"""
    def __init__(self, detail: str = "Erro de validação"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) 