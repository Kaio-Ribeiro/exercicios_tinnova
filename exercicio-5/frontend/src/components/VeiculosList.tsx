import React, { useState, useEffect, useCallback } from 'react';
import { Veiculo } from '../types/veiculo';
import { veiculosService } from '../services/api';
import VeiculoForm from './VeiculoForm';

const VeiculosList: React.FC = () => {
  const [veiculos, setVeiculos] = useState<Veiculo[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingVeiculo, setEditingVeiculo] = useState<Veiculo | undefined>();
  const [filtros, setFiltros] = useState({ marca: '', ano: '' });

  const carregarVeiculos = useCallback(async () => {
    try {
      setLoading(true);
      const params: { marca?: string; ano?: number } = {};
      if (filtros.marca) params.marca = filtros.marca;
      if (filtros.ano && filtros.ano !== '') params.ano = parseInt(filtros.ano);
      
      const data = await veiculosService.listarVeiculos(params);
      setVeiculos(data);
    } catch (error) {
      console.error('Erro ao carregar veículos:', error);
    } finally {
      setLoading(false);
    }
  }, [filtros]);

  useEffect(() => {
    carregarVeiculos();
  }, [carregarVeiculos]);

  const handleEdit = (veiculo: Veiculo) => {
    setEditingVeiculo(veiculo);
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (!id) {
      console.error('ID do veículo não encontrado');
      return;
    }
    
    if (window.confirm('Tem certeza que deseja excluir este veículo?')) {
      try {
        await veiculosService.excluirVeiculo(id);
        carregarVeiculos();
      } catch (error) {
        console.error('Erro ao excluir veículo:', error);
        alert('Erro ao excluir veículo. Tente novamente.');
      }
    }
  };

  const handleFormSave = () => {
    setShowForm(false);
    setEditingVeiculo(undefined);
    carregarVeiculos();
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingVeiculo(undefined);
  };

  if (showForm) {
    return (
      <VeiculoForm
        veiculo={editingVeiculo}
        onSave={handleFormSave}
        onCancel={handleFormCancel}
      />
    );
  }

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Lista de Veículos</h1>
        <button 
          onClick={() => setShowForm(true)}
          style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}
        >
          Novo Veículo
        </button>
      </div>

      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
        <input
          type="text"
          placeholder="Filtrar por marca"
          value={filtros.marca}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFiltros({ ...filtros, marca: e.target.value })}
          style={{ padding: '8px' }}
        />
        <input
          type="number"
          placeholder="Filtrar por ano"
          value={filtros.ano}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFiltros({ ...filtros, ano: e.target.value })}
          style={{ padding: '8px' }}
        />
        <button onClick={carregarVeiculos} style={{ padding: '8px 16px' }}>
          Buscar
        </button>
      </div>

      {loading ? (
        <div>Carregando...</div>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ backgroundColor: '#f8f9fa' }}>
                <th style={{ border: '1px solid #ddd', padding: '12px', textAlign: 'left' }}>ID</th>
                <th style={{ border: '1px solid #ddd', padding: '12px', textAlign: 'left' }}>Veículo</th>
                <th style={{ border: '1px solid #ddd', padding: '12px', textAlign: 'left' }}>Marca</th>
                <th style={{ border: '1px solid #ddd', padding: '12px', textAlign: 'left' }}>Ano</th>
                <th style={{ border: '1px solid #ddd', padding: '12px', textAlign: 'left' }}>Status</th>
                <th style={{ border: '1px solid #ddd', padding: '12px', textAlign: 'left' }}>Ações</th>
              </tr>
            </thead>
            <tbody>
              {veiculos.map((veiculo) => (
                <tr key={veiculo.id}>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>{veiculo.id}</td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>{veiculo.veiculo}</td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>{veiculo.marca}</td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>{veiculo.ano}</td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    <span style={{ 
                      padding: '4px 8px', 
                      borderRadius: '4px',
                      backgroundColor: veiculo.vendido ? '#d4edda' : '#f8d7da',
                      color: veiculo.vendido ? '#155724' : '#721c24'
                    }}>
                      {veiculo.vendido ? 'Vendido' : 'Disponível'}
                    </span>
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                    <button
                      onClick={() => handleEdit(veiculo)}
                      style={{ marginRight: '8px', padding: '6px 12px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px' }}
                    >
                      Editar
                    </button>
                    <button
                      onClick={() => handleDelete(veiculo.id as number)}
                      style={{ padding: '6px 12px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px' }}
                    >
                      Excluir
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {veiculos.length === 0 && (
            <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
              Nenhum veículo encontrado
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default VeiculosList;
