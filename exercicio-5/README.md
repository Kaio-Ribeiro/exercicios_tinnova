# Sistema de Cadastro de Veículos

Uma aplicação full-stack para gerenciamento de veículos com FastAPI (backend) e React (frontend).

## Funcionalidades

- ✅ Cadastro de veículos
- ✅ Atualização de dados de veículos
- ✅ Exclusão de veículos
- ✅ Consulta de veículos não vendidos
- ✅ Distribuição de veículos por década
- ✅ Distribuição de veículos por fabricante
- ✅ Veículos registrados na última semana
- ✅ Validação de marcas de veículos

## Tecnologias

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest

### Frontend
- React
- TypeScript
- Axios
- Material-UI
- React Router

## Estrutura do Projeto

```
exercicio-5/
├── backend/
│   ├── app/
│   │   ├── models/        # Modelos do banco de dados
│   │   ├── schemas/       # Schemas Pydantic
│   │   ├── routers/       # Endpoints da API
│   │   ├── services/      # Lógica de negócio
│   │   └── main.py        # Aplicação principal
│   ├── tests/             # Testes unitários
│   └── requirements.txt   # Dependências Python
├── frontend/
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── services/      # Comunicação com API
│   │   └── App.tsx        # Aplicação principal
│   └── package.json       # Dependências Node.js
├── docker-compose.yml     # Orquestração Docker
├── Makefile              # Comandos de desenvolvimento
├── start.sh              # Script de inicialização (Linux/Mac)
├── start.ps1             # Script de inicialização (Windows)
└── README.md
```

## Como Executar

### Opção 1: Com Docker (Recomendado) 🐳

**Pré-requisitos:**
- Docker e Docker Compose instalados

**Inicialização:**
```bash
docker-compose up --build -d
```

**Comandos úteis:**
```bash
docker-compose down     # Parar serviços
docker-compose logs     # Ver logs
```

### Opção 2: Instalação Manual

**Pré-requisitos:**
- Python 3.8+ e pip
- Node.js 16+ e npm

#### Backend (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend (Terminal 2)
```bash
cd frontend
npm install
npm start
```

### URLs Importantes
- **Frontend**: http://localhost:3000
- **API Backend**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs

## Testes

### Com Docker
```bash
docker-compose exec backend pytest tests/
```

### Manual
```bash
cd backend
pytest tests/
```

## API Endpoints

- `GET /veiculos` - Lista todos os veículos
- `GET /veiculos?marca={marca}&ano={ano}` - Filtra veículos
- `GET /veiculos/{id}` - Detalhes de um veículo
- `POST /veiculos` - Cria um novo veículo
- `PUT /veiculos/{id}` - Atualiza um veículo completo
- `PATCH /veiculos/{id}` - Atualiza parcialmente um veículo
- `DELETE /veiculos/{id}` - Remove um veículo
- `GET /veiculos/stats/nao-vendidos` - Conta veículos não vendidos
- `GET /veiculos/stats/por-decada` - Distribuição por década
- `GET /veiculos/stats/por-marca` - Distribuição por marca
- `GET /veiculos/stats/ultima-semana` - Veículos da última semana

## Testes

Para executar os testes:
```bash
cd backend
pytest tests/
```

## Modelo de Dados

```json
{
  "veiculo": "string",
  "marca": "string", 
  "ano": "integer",
  "descricao": "text",
  "vendido": "boolean",
  "created": "datetime",
  "updated": "datetime"
}
```

## Marcas Válidas

O sistema valida as seguintes marcas:
- Volkswagen, Ford, Chevrolet, Fiat, Honda, Toyota, Nissan, Hyundai, Renault, Peugeot, BMW, Mercedes-Benz, Audi

## Autor

Desenvolvido como parte do teste técnico da Tinnova.
