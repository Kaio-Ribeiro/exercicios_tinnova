import axios from 'axios';
import { Veiculo, VeiculoStats, VeiculoPorDecada, VeiculoPorMarca } from '../types/veiculo';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const veiculosService = {
  // Listar veículos
  async listarVeiculos(params?: { marca?: string; ano?: number }): Promise<Veiculo[]> {
    const response = await api.get('/veiculos/', { params });
    return response.data;
  },

  // Obter veículo por ID
  async obterVeiculo(id: number): Promise<Veiculo> {
    const response = await api.get(`/veiculos/${id}`);
    return response.data;
  },

  // Criar veículo
  async criarVeiculo(veiculo: Omit<Veiculo, 'id' | 'created' | 'updated'>): Promise<Veiculo> {
    const response = await api.post('/veiculos/', veiculo);
    return response.data;
  },

  // Atualizar veículo (PUT)
  async atualizarVeiculo(id: number, veiculo: Omit<Veiculo, 'id' | 'created' | 'updated'>): Promise<Veiculo> {
    const response = await api.put(`/veiculos/${id}`, veiculo);
    return response.data;
  },

  // Atualizar veículo parcialmente (PATCH)
  async atualizarVeiculoParcial(id: number, veiculo: Partial<Omit<Veiculo, 'id' | 'created' | 'updated'>>): Promise<Veiculo> {
    const response = await api.patch(`/veiculos/${id}`, veiculo);
    return response.data;
  },

  // Excluir veículo
  async excluirVeiculo(id: number): Promise<void> {
    await api.delete(`/veiculos/${id}`);
  },

  // Estatísticas
  async contarNaoVendidos(): Promise<VeiculoStats> {
    const response = await api.get('/veiculos/stats/nao-vendidos');
    return response.data;
  },

  async distribuicaoPorDecada(): Promise<VeiculoPorDecada[]> {
    const response = await api.get('/veiculos/stats/por-decada');
    return response.data;
  },

  async distribuicaoPorMarca(): Promise<VeiculoPorMarca[]> {
    const response = await api.get('/veiculos/stats/por-marca');
    return response.data;
  },

  async veiculosUltimaSemana(): Promise<Veiculo[]> {
    const response = await api.get('/veiculos/stats/ultima-semana');
    return response.data;
  },
};
