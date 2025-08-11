export interface Veiculo {
  id?: number;
  veiculo: string;
  marca: string;
  ano: number;
  descricao?: string;
  vendido: boolean;
  created?: string;
  updated?: string;
}

export interface VeiculoStats {
  total_nao_vendidos: number;
}

export interface VeiculoPorDecada {
  decada: string;
  quantidade: number;
}

export interface VeiculoPorMarca {
  marca: string;
  quantidade: number;
}

export const MARCAS_VALIDAS = [
  "Volkswagen", "Ford", "Chevrolet", "Fiat", "Honda", "Toyota",
  "Nissan", "Hyundai", "Renault", "Peugeot", "BMW", "Mercedes-Benz", "Audi"
];
