from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import List, Optional

from ..models import Veiculo
from ..schemas import VeiculoCreate, VeiculoUpdate, VeiculoPatch

class VeiculoService:
    """Serviço para operações com veículos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_veiculo(self, veiculo_id: int) -> Optional[Veiculo]:
        """Busca um veículo por ID"""
        return self.db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
    
    def get_veiculos(
        self, 
        skip: int = 0, 
        limit: int = 100,
        marca: Optional[str] = None,
        ano: Optional[int] = None
    ) -> List[Veiculo]:
        """Lista veículos com filtros opcionais"""
        query = self.db.query(Veiculo)
        
        if marca:
            query = query.filter(Veiculo.marca == marca)
        if ano:
            query = query.filter(Veiculo.ano == ano)
            
        return query.offset(skip).limit(limit).all()
    
    def create_veiculo(self, veiculo: VeiculoCreate) -> Veiculo:
        """Cria um novo veículo"""
        db_veiculo = Veiculo(**veiculo.dict())
        self.db.add(db_veiculo)
        self.db.commit()
        self.db.refresh(db_veiculo)
        return db_veiculo
    
    def update_veiculo(self, veiculo_id: int, veiculo: VeiculoUpdate) -> Optional[Veiculo]:
        """Atualiza um veículo completamente"""
        db_veiculo = self.get_veiculo(veiculo_id)
        if db_veiculo:
            for key, value in veiculo.dict().items():
                setattr(db_veiculo, key, value)
            db_veiculo.updated = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_veiculo)
        return db_veiculo
    
    def patch_veiculo(self, veiculo_id: int, veiculo: VeiculoPatch) -> Optional[Veiculo]:
        """Atualiza um veículo parcialmente"""
        db_veiculo = self.get_veiculo(veiculo_id)
        if db_veiculo:
            update_data = veiculo.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_veiculo, key, value)
            db_veiculo.updated = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_veiculo)
        return db_veiculo
    
    def delete_veiculo(self, veiculo_id: int) -> bool:
        """Remove um veículo"""
        db_veiculo = self.get_veiculo(veiculo_id)
        if db_veiculo:
            self.db.delete(db_veiculo)
            self.db.commit()
            return True
        return False
    
    def count_nao_vendidos(self) -> int:
        """Conta veículos não vendidos"""
        return self.db.query(Veiculo).filter(Veiculo.vendido == False).count()
    
    def get_distribuicao_por_decada(self) -> List[dict]:
        """Retorna distribuição de veículos por década"""
        result = self.db.query(
            func.floor(Veiculo.ano / 10) * 10,
            func.count(Veiculo.id)
        ).group_by(func.floor(Veiculo.ano / 10) * 10).all()
        
        return [
            {"decada": f"Década {int(decada)}", "quantidade": quantidade}
            for decada, quantidade in result
        ]
    
    def get_distribuicao_por_marca(self) -> List[dict]:
        """Retorna distribuição de veículos por marca"""
        result = self.db.query(
            Veiculo.marca,
            func.count(Veiculo.id)
        ).group_by(Veiculo.marca).all()
        
        return [
            {"marca": marca, "quantidade": quantidade}
            for marca, quantidade in result
        ]
    
    def get_veiculos_ultima_semana(self) -> List[Veiculo]:
        """Retorna veículos registrados na última semana"""
        uma_semana_atras = datetime.utcnow() - timedelta(days=7)
        return self.db.query(Veiculo).filter(
            Veiculo.created >= uma_semana_atras
        ).all()
