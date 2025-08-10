from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import get_db
from ..schemas import (
    VeiculoCreate, VeiculoUpdate, VeiculoPatch, VeiculoResponse,
    VeiculoStats, VeiculoPorDecada, VeiculoPorMarca
)
from ..services import VeiculoService

router = APIRouter(prefix="/veiculos", tags=["veiculos"])

@router.get("/", response_model=List[VeiculoResponse])
def listar_veiculos(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros"),
    marca: Optional[str] = Query(None, description="Filtrar por marca"),
    ano: Optional[int] = Query(None, ge=1900, le=2030, description="Filtrar por ano"),
    db: Session = Depends(get_db)
):
    """Lista todos os veículos com filtros opcionais"""
    service = VeiculoService(db)
    return service.get_veiculos(skip=skip, limit=limit, marca=marca, ano=ano)

@router.get("/{veiculo_id}", response_model=VeiculoResponse)
def obter_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    """Obtém detalhes de um veículo específico"""
    service = VeiculoService(db)
    veiculo = service.get_veiculo(veiculo_id)
    if veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo

@router.post("/", response_model=VeiculoResponse, status_code=201)
def criar_veiculo(veiculo: VeiculoCreate, db: Session = Depends(get_db)):
    """Cria um novo veículo"""
    service = VeiculoService(db)
    return service.create_veiculo(veiculo)

@router.put("/{veiculo_id}", response_model=VeiculoResponse)
def atualizar_veiculo(
    veiculo_id: int, 
    veiculo: VeiculoUpdate, 
    db: Session = Depends(get_db)
):
    """Atualiza todos os dados de um veículo"""
    service = VeiculoService(db)
    veiculo_atualizado = service.update_veiculo(veiculo_id, veiculo)
    if veiculo_atualizado is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo_atualizado

@router.patch("/{veiculo_id}", response_model=VeiculoResponse)
def atualizar_veiculo_parcial(
    veiculo_id: int, 
    veiculo: VeiculoPatch, 
    db: Session = Depends(get_db)
):
    """Atualiza parcialmente os dados de um veículo"""
    service = VeiculoService(db)
    veiculo_atualizado = service.patch_veiculo(veiculo_id, veiculo)
    if veiculo_atualizado is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo_atualizado

@router.delete("/{veiculo_id}", status_code=204)
def excluir_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    """Remove um veículo"""
    service = VeiculoService(db)
    if not service.delete_veiculo(veiculo_id):
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

@router.get("/stats/nao-vendidos", response_model=VeiculoStats)
def contar_nao_vendidos(db: Session = Depends(get_db)):
    """Retorna a quantidade de veículos não vendidos"""
    service = VeiculoService(db)
    count = service.count_nao_vendidos()
    return VeiculoStats(total_nao_vendidos=count)

@router.get("/stats/por-decada", response_model=List[VeiculoPorDecada])
def distribuicao_por_decada(db: Session = Depends(get_db)):
    """Retorna a distribuição de veículos por década de fabricação"""
    service = VeiculoService(db)
    return service.get_distribuicao_por_decada()

@router.get("/stats/por-marca", response_model=List[VeiculoPorMarca])
def distribuicao_por_marca(db: Session = Depends(get_db)):
    """Retorna a distribuição de veículos por marca"""
    service = VeiculoService(db)
    return service.get_distribuicao_por_marca()

@router.get("/stats/ultima-semana", response_model=List[VeiculoResponse])
def veiculos_ultima_semana(db: Session = Depends(get_db)):
    """Retorna veículos registrados na última semana"""
    service = VeiculoService(db)
    return service.get_veiculos_ultima_semana()
