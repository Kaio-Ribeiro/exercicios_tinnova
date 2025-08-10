from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import create_tables
from .routers import veiculos_router

# Criar as tabelas do banco de dados
create_tables()

# Criar aplicação FastAPI
app = FastAPI(
    title="Sistema de Cadastro de Veículos",
    description="API REST para gerenciamento de veículos com operações CRUD completas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL do React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(veiculos_router)

@app.get("/")
def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Sistema de Cadastro de Veículos - API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "veiculos": "/veiculos",
            "stats": {
                "nao_vendidos": "/veiculos/stats/nao-vendidos",
                "por_decada": "/veiculos/stats/por-decada", 
                "por_marca": "/veiculos/stats/por-marca",
                "ultima_semana": "/veiculos/stats/ultima-semana"
            }
        }
    }

@app.get("/health")
def health_check():
    """Endpoint para verificação de saúde da API"""
    return {"status": "healthy", "message": "API funcionando corretamente"}
