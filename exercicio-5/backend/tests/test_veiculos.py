import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(client: TestClient):
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"

def test_health_check(client: TestClient):
    """Testa o endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_create_veiculo(client: TestClient, veiculo_data):
    """Testa criação de veículo"""
    response = client.post("/veiculos/", json=veiculo_data)
    assert response.status_code == 201
    data = response.json()
    assert data["veiculo"] == veiculo_data["veiculo"]
    assert data["marca"] == veiculo_data["marca"]
    assert data["ano"] == veiculo_data["ano"]
    assert "id" in data
    assert "created" in data

def test_create_veiculo_marca_invalida(client: TestClient):
    """Testa criação de veículo com marca inválida"""
    invalid_data = {
        "veiculo": "Test",
        "marca": "MarcaInvalida",
        "ano": 2020,
        "descricao": "Teste",
        "vendido": False
    }
    response = client.post("/veiculos/", json=invalid_data)
    assert response.status_code == 422

def test_get_veiculos_empty(client: TestClient):
    """Testa listagem de veículos quando vazia"""
    response = client.get("/veiculos/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_veiculo_not_found(client: TestClient):
    """Testa busca de veículo inexistente"""
    response = client.get("/veiculos/999")
    assert response.status_code == 404

def test_crud_veiculo(client: TestClient, veiculo_data):
    """Testa operações CRUD completas"""
    # CREATE
    response = client.post("/veiculos/", json=veiculo_data)
    assert response.status_code == 201
    veiculo = response.json()
    veiculo_id = veiculo["id"]
    
    # READ
    response = client.get(f"/veiculos/{veiculo_id}")
    assert response.status_code == 200
    assert response.json()["id"] == veiculo_id
    
    # UPDATE (PUT)
    update_data = veiculo_data.copy()
    update_data["veiculo"] = "Civic Atualizado"
    response = client.put(f"/veiculos/{veiculo_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["veiculo"] == "Civic Atualizado"
    
    # UPDATE (PATCH)
    patch_data = {"vendido": True}
    response = client.patch(f"/veiculos/{veiculo_id}", json=patch_data)
    assert response.status_code == 200
    assert response.json()["vendido"] == True
    
    # DELETE
    response = client.delete(f"/veiculos/{veiculo_id}")
    assert response.status_code == 204
    
    # Verificar se foi deletado
    response = client.get(f"/veiculos/{veiculo_id}")
    assert response.status_code == 404

def test_stats_nao_vendidos(client: TestClient, veiculo_data):
    """Testa estatísticas de veículos não vendidos"""
    # Criar alguns veículos
    client.post("/veiculos/", json=veiculo_data)
    
    vendido_data = veiculo_data.copy()
    vendido_data["veiculo"] = "Outro"
    vendido_data["vendido"] = True
    client.post("/veiculos/", json=vendido_data)
    
    # Testar estatística
    response = client.get("/veiculos/stats/nao-vendidos")
    assert response.status_code == 200
    assert response.json()["total_nao_vendidos"] == 1

def test_stats_por_marca(client: TestClient, veiculo_data):
    """Testa estatísticas por marca"""
    # Criar veículo
    client.post("/veiculos/", json=veiculo_data)
    
    # Testar estatística
    response = client.get("/veiculos/stats/por-marca")
    assert response.status_code == 200
    stats = response.json()
    assert len(stats) == 1
    assert stats[0]["marca"] == "Honda"
    assert stats[0]["quantidade"] == 1

def test_stats_por_decada(client: TestClient, veiculo_data):
    """Testa estatísticas por década"""
    # Criar veículo
    client.post("/veiculos/", json=veiculo_data)
    
    # Testar estatística
    response = client.get("/veiculos/stats/por-decada")
    assert response.status_code == 200
    stats = response.json()
    assert len(stats) == 1
    assert "2020" in stats[0]["decada"]
    assert stats[0]["quantidade"] == 1

def test_filtros_veiculos(client: TestClient, veiculo_data):
    """Testa filtros de listagem"""
    # Criar veículo
    client.post("/veiculos/", json=veiculo_data)
    
    # Criar outro veículo com marca diferente
    outro_data = veiculo_data.copy()
    outro_data["veiculo"] = "Focus"
    outro_data["marca"] = "Ford"
    outro_data["ano"] = 2019
    client.post("/veiculos/", json=outro_data)
    
    # Testar filtro por marca
    response = client.get("/veiculos/?marca=Honda")
    assert response.status_code == 200
    veiculos = response.json()
    assert len(veiculos) == 1
    assert veiculos[0]["marca"] == "Honda"
    
    # Testar filtro por ano
    response = client.get("/veiculos/?ano=2019")
    assert response.status_code == 200
    veiculos = response.json()
    assert len(veiculos) == 1
    assert veiculos[0]["ano"] == 2019
