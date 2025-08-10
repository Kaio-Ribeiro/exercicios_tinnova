from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

# Lista de marcas válidas
MARCAS_VALIDAS = [
    "Volkswagen", "Ford", "Chevrolet", "Fiat", "Honda", "Toyota", 
    "Nissan", "Hyundai", "Renault", "Peugeot", "BMW", "Mercedes-Benz", "Audi"
]

class VeiculoBase(BaseModel):
    """Schema base para veículo"""
    veiculo: str = Field(..., min_length=1, max_length=100, description="Nome do veículo")
    marca: str = Field(..., min_length=1, max_length=50, description="Marca do veículo")
    ano: int = Field(..., ge=1900, le=2030, description="Ano de fabricação")
    descricao: Optional[str] = Field(None, description="Descrição do veículo")
    vendido: bool = Field(False, description="Status de venda")

    @validator('marca')
    def validar_marca(cls, v):
        if v not in MARCAS_VALIDAS:
            raise ValueError(f'Marca inválida. Marcas aceitas: {", ".join(MARCAS_VALIDAS)}')
        return v

    @validator('ano')
    def validar_ano(cls, v):
        if v < 1900 or v > 2030:
            raise ValueError('Ano deve estar entre 1900 e 2030')
        return v

class VeiculoCreate(VeiculoBase):
    """Schema para criação de veículo"""
    pass

class VeiculoUpdate(BaseModel):
    """Schema para atualização completa de veículo"""
    veiculo: str = Field(..., min_length=1, max_length=100)
    marca: str = Field(..., min_length=1, max_length=50)
    ano: int = Field(..., ge=1900, le=2030)
    descricao: Optional[str] = None
    vendido: bool = False

    @validator('marca')
    def validar_marca(cls, v):
        if v not in MARCAS_VALIDAS:
            raise ValueError(f'Marca inválida. Marcas aceitas: {", ".join(MARCAS_VALIDAS)}')
        return v

class VeiculoPatch(BaseModel):
    """Schema para atualização parcial de veículo"""
    veiculo: Optional[str] = Field(None, min_length=1, max_length=100)
    marca: Optional[str] = Field(None, min_length=1, max_length=50)
    ano: Optional[int] = Field(None, ge=1900, le=2030)
    descricao: Optional[str] = None
    vendido: Optional[bool] = None

    @validator('marca')
    def validar_marca(cls, v):
        if v is not None and v not in MARCAS_VALIDAS:
            raise ValueError(f'Marca inválida. Marcas aceitas: {", ".join(MARCAS_VALIDAS)}')
        return v

class VeiculoResponse(VeiculoBase):
    """Schema para resposta de veículo"""
    id: int
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True

class VeiculoStats(BaseModel):
    """Schema para estatísticas"""
    total_nao_vendidos: int

class VeiculoPorDecada(BaseModel):
    """Schema para distribuição por década"""
    decada: str
    quantidade: int

class VeiculoPorMarca(BaseModel):
    """Schema para distribuição por marca"""
    marca: str
    quantidade: int
