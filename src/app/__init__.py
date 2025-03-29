from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.api.routes import quantities
from app.config.settings import Settings
from app.core.database import Base, engine

def create_app() -> FastAPI:
    # Carrega configurações
    settings = Settings()
    
    # Cria a aplicação
    app = FastAPI(
        title="Print Shop Waste Calculator",
        description="API para cálculo de desperdício em gráficas",
        version="1.0.0"
    )
    
    # Configuração de CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Registra rotas
    app.include_router(quantities.router, prefix="/api", tags=["quantities"])
    
    # Configurar pasta de arquivos estáticos
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Cria as tabelas no banco de dados
    Base.metadata.create_all(bind=engine)
    
    # Servir o arquivo index.html na rota raiz
    @app.get("/")
    async def serve_index():
        return FileResponse("index.html")
    
    return app

app = create_app()