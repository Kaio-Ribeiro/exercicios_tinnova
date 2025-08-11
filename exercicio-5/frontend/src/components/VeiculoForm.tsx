import React, { useState, useEffect } from 'react';
import { Veiculo, MARCAS_VALIDAS } from '../types/veiculo';
import { veiculosService } from '../services/api';

interface VeiculoFormProps {
  veiculo?: Veiculo;
  onSave: () => void;
  onCancel: () => void;
}

const VeiculoForm: React.FC<VeiculoFormProps> = ({ veiculo, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    veiculo: '',
    marca: '',
    ano: new Date().getFullYear(),
    descricao: '',
    vendido: false,
  });

  const [errors, setErrors] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (veiculo) {
      setFormData({
        veiculo: veiculo.veiculo,
        marca: veiculo.marca,
        ano: veiculo.ano,
        descricao: veiculo.descricao || '',
        vendido: veiculo.vendido,
      });
    }
  }, [veiculo]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors([]);
    setLoading(true);

    try {
      if (veiculo) {
        await veiculosService.atualizarVeiculo(veiculo.id!, formData);
      } else {
        await veiculosService.criarVeiculo(formData);
      }
      onSave();
    } catch (error: any) {
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          setErrors(error.response.data.detail.map((err: any) => err.msg));
        } else {
          setErrors([error.response.data.detail]);
        }
      } else {
        setErrors(['Erro ao salvar veículo']);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '500px', margin: '0 auto' }}>
      <h2>{veiculo ? 'Editar Veículo' : 'Novo Veículo'}</h2>
      
      {errors.length > 0 && (
        <div style={{ color: 'red', marginBottom: '10px' }}>
          {errors.map((error, index) => (
            <div key={index}>{error}</div>
          ))}
        </div>
      )}

      <div style={{ marginBottom: '15px' }}>
        <label>Veículo:</label>
        <input
          type="text"
          value={formData.veiculo}
          onChange={(e) => setFormData({ ...formData, veiculo: e.target.value })}
          required
          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label>Marca:</label>
        <select
          value={formData.marca}
          onChange={(e) => setFormData({ ...formData, marca: e.target.value })}
          required
          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
        >
          <option value="">Selecione uma marca</option>
          {MARCAS_VALIDAS.map((marca) => (
            <option key={marca} value={marca}>
              {marca}
            </option>
          ))}
        </select>
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label>Ano:</label>
        <input
          type="number"
          value={formData.ano}
          onChange={(e) => setFormData({ ...formData, ano: parseInt(e.target.value) })}
          min="1900"
          max="2030"
          required
          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label>Descrição:</label>
        <textarea
          value={formData.descricao}
          onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
          rows={3}
          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label>
          <input
            type="checkbox"
            checked={formData.vendido}
            onChange={(e) => setFormData({ ...formData, vendido: e.target.checked })}
            style={{ marginRight: '8px' }}
          />
          Vendido
        </label>
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <button type="submit" disabled={loading} style={{ padding: '10px 20px' }}>
          {loading ? 'Salvando...' : 'Salvar'}
        </button>
        <button type="button" onClick={onCancel} style={{ padding: '10px 20px' }}>
          Cancelar
        </button>
      </div>
    </form>
  );
};

export default VeiculoForm;
