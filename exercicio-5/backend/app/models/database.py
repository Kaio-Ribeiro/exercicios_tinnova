from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Base para os modelos
Base = declarative_base()

# Configuração do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/veiculos.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Veiculo(Base):
    """Modelo de dados para veículos"""
    __tablename__ = "veiculos"
    
    id = Column(Integer, primary_key=True, index=True)
    veiculo = Column(String(100), nullable=False, index=True)
    marca = Column(String(50), nullable=False, index=True)
    ano = Column(Integer, nullable=False, index=True)
    descricao = Column(Text)
    vendido = Column(Boolean, default=False, index=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Função para criar as tabelas
def create_tables():
    Base.metadata.create_all(bind=engine)

# Função para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
