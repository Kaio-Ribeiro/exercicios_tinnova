import React, { useState, useEffect } from 'react';
import { VeiculoStats, VeiculoPorDecada, VeiculoPorMarca, Veiculo } from '../types/veiculo';
import { veiculosService } from '../services/api';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<VeiculoStats | null>(null);
  const [porDecada, setPorDecada] = useState<VeiculoPorDecada[]>([]);
  const [porMarca, setPorMarca] = useState<VeiculoPorMarca[]>([]);
  const [ultimaSemana, setUltimaSemana] = useState<Veiculo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    try {
      setLoading(true);
      const [statsData, decadaData, marcaData, semanaData] = await Promise.all([
        veiculosService.contarNaoVendidos(),
        veiculosService.distribuicaoPorDecada(),
        veiculosService.distribuicaoPorMarca(),
        veiculosService.veiculosUltimaSemana(),
      ]);

      setStats(statsData);
      setPorDecada(decadaData);
      setPorMarca(marcaData);
      setUltimaSemana(semanaData);
    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div style={{ padding: '20px', textAlign: 'center' }}>Carregando...</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Dashboard - Estatísticas de Veículos</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        {/* Card de veículos não vendidos */}
        <div style={{ 
          border: '1px solid #ddd', 
          borderRadius: '8px', 
          padding: '20px', 
          backgroundColor: '#f8f9fa',
          textAlign: 'center'
        }}>
          <h3>Veículos Não Vendidos</h3>
          <div style={{ fontSize: '2em', fontWeight: 'bold', color: '#007bff' }}>
            {stats?.total_nao_vendidos || 0}
          </div>
        </div>

        {/* Card de veículos da última semana */}
        <div style={{ 
          border: '1px solid #ddd', 
          borderRadius: '8px', 
          padding: '20px', 
          backgroundColor: '#f8f9fa',
          textAlign: 'center'
        }}>
          <h3>Registrados esta Semana</h3>
          <div style={{ fontSize: '2em', fontWeight: 'bold', color: '#28a745' }}>
            {ultimaSemana.length}
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px' }}>
        {/* Distribuição por década */}
        <div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3>Distribuição por Década</h3>
          {porDecada.length > 0 ? (
            <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
              {porDecada.map((item, index) => (
                <div key={index} style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  padding: '10px 0', 
                  borderBottom: '1px solid #eee' 
                }}>
                  <span>{item.decada}</span>
                  <span style={{ fontWeight: 'bold' }}>{item.quantidade} veículos</span>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: '#666' }}>Nenhum dado disponível</p>
          )}
        </div>

        {/* Distribuição por marca */}
        <div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3>Distribuição por Marca</h3>
          {porMarca.length > 0 ? (
            <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
              {porMarca.map((item, index) => (
                <div key={index} style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  padding: '10px 0', 
                  borderBottom: '1px solid #eee' 
                }}>
                  <span>{item.marca}</span>
                  <span style={{ fontWeight: 'bold' }}>{item.quantidade} veículos</span>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: '#666' }}>Nenhum dado disponível</p>
          )}
        </div>
      </div>

      {/* Veículos da última semana */}
      {ultimaSemana.length > 0 && (
        <div style={{ marginTop: '30px', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3>Veículos Registrados na Última Semana</h3>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: '#f8f9fa' }}>
                  <th style={{ border: '1px solid #ddd', padding: '12px', textAlign: 'left' }}>Veículo</th>
                  <th style={{ border: '1px solid #ddd', padding: '12px', textAlign: 'left' }}>Marca</th>
                  <th style={{ border: '1px solid #ddd', padding: '12px', textAlign: 'left' }}>Ano</th>
                  <th style={{ border: '1px solid #ddd', padding: '12px', textAlign: 'left' }}>Data de Registro</th>
                </tr>
              </thead>
              <tbody>
                {ultimaSemana.map((veiculo) => (
                  <tr key={veiculo.id}>
                    <td style={{ border: '1px solid #ddd', padding: '12px' }}>{veiculo.veiculo}</td>
                    <td style={{ border: '1px solid #ddd', padding: '12px' }}>{veiculo.marca}</td>
                    <td style={{ border: '1px solid #ddd', padding: '12px' }}>{veiculo.ano}</td>
                    <td style={{ border: '1px solid #ddd', padding: '12px' }}>
                      {veiculo.created ? new Date(veiculo.created).toLocaleDateString('pt-BR') : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <button 
          onClick={carregarDados}
          style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}
        >
          Atualizar Dados
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
