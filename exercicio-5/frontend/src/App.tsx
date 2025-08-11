import React, { useState } from 'react';
import VeiculosList from './components/VeiculosList';
import Dashboard from './components/Dashboard';
import './App.css';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'veiculos' | 'dashboard'>('veiculos');

  return (
    <div className="App">
      <nav style={{ 
        backgroundColor: '#343a40', 
        padding: '1rem 2rem', 
        marginBottom: '20px',
        display: 'flex',
        alignItems: 'center',
        gap: '20px'
      }}>
        <h1 style={{ color: 'white', margin: 0 }}>Sistema de Veículos</h1>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={() => setActiveTab('veiculos')}
            style={{
              padding: '8px 16px',
              backgroundColor: activeTab === 'veiculos' ? '#007bff' : 'transparent',
              color: 'white',
              border: '1px solid #007bff',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Veículos
          </button>
          <button
            onClick={() => setActiveTab('dashboard')}
            style={{
              padding: '8px 16px',
              backgroundColor: activeTab === 'dashboard' ? '#007bff' : 'transparent',
              color: 'white',
              border: '1px solid #007bff',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Dashboard
          </button>
        </div>
      </nav>

      <main>
        {activeTab === 'veiculos' && <VeiculosList />}
        {activeTab === 'dashboard' && <Dashboard />}
      </main>
    </div>
  );
};

export default App;
