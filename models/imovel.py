#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de dados para Imóvel
"""

from datetime import datetime
from typing import Optional, Dict, Any
import logging

class Imovel:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.endereco = kwargs.get('endereco', '')
        self.cidade = kwargs.get('cidade', '')
        self.estado = kwargs.get('estado', '')
        self.cep = kwargs.get('cep', '')
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.metragem = kwargs.get('metragem', 0.0)
        self.quartos = kwargs.get('quartos', 0)
        self.banheiros = kwargs.get('banheiros', 0)
        self.ano = kwargs.get('ano')
        self.padrao_acabamento = kwargs.get('padrao_acabamento', 'medio')
        self.custo_aquisicao = kwargs.get('custo_aquisicao', 0.0)
        self.custos_reforma = kwargs.get('custos_reforma', 0.0)
        self.custos_transacao = kwargs.get('custos_transacao', 0.0)
        self.percentual_lucro_credor = kwargs.get('percentual_lucro_credor', 10.0)
        self.status = kwargs.get('status', 'em_analise')
        self.data_criacao = kwargs.get('data_criacao')
        self.data_atualizacao = kwargs.get('data_atualizacao')
        
        # Validações
        self.validate()
        
    def validate(self):
        """Valida os dados do imóvel"""
        errors = []
        
        if not self.endereco:
            errors.append("Endereço é obrigatório")
            
        if not self.cidade:
            errors.append("Cidade é obrigatória")
            
        if not self.estado:
            errors.append("Estado é obrigatório")
            
        if self.metragem <= 0:
            errors.append("Metragem deve ser maior que zero")
            
        if self.custo_aquisicao < 0:
            errors.append("Custo de aquisição não pode ser negativo")
            
        if self.custos_reforma < 0:
            errors.append("Custos de reforma não podem ser negativos")
            
        if self.custos_transacao < 0:
            errors.append("Custos de transação não podem ser negativos")
            
        if self.percentual_lucro_credor < 0 or self.percentual_lucro_credor > 100:
            errors.append("Percentual de lucro do credor deve estar entre 0 e 100")
            
        if self.padrao_acabamento not in ['baixo', 'medio', 'alto']:
            errors.append("Padrão de acabamento deve ser 'baixo', 'medio' ou 'alto'")
            
        if self.status not in ['em_analise', 'comprado', 'vendido']:
            errors.append("Status deve ser 'em_analise', 'comprado' ou 'vendido'")
            
        if errors:
            raise ValueError("; ".join(errors))
            
    def to_dict(self) -> Dict[str, Any]:
        """Converte o imóvel para dicionário"""
        return {
            'id': self.id,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'metragem': self.metragem,
            'quartos': self.quartos,
            'banheiros': self.banheiros,
            'ano': self.ano,
            'padrao_acabamento': self.padrao_acabamento,
            'custo_aquisicao': self.custo_aquisicao,
            'custos_reforma': self.custos_reforma,
            'custos_transacao': self.custos_transacao,
            'percentual_lucro_credor': self.percentual_lucro_credor,
            'status': self.status,
            'data_criacao': self.data_criacao,
            'data_atualizacao': self.data_atualizacao
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Imovel':
        """Cria um imóvel a partir de um dicionário"""
        return cls(**data)
        
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Imovel':
        """Cria um imóvel a partir de uma linha do banco"""
        columns = [
            'id', 'endereco', 'cidade', 'estado', 'cep', 'latitude', 'longitude',
            'metragem', 'quartos', 'banheiros', 'ano', 'padrao_acabamento',
            'custo_aquisicao', 'custos_reforma', 'custos_transacao',
            'percentual_lucro_credor', 'status', 'data_criacao', 'data_atualizacao'
        ]
        
        data = dict(zip(columns, row))
        return cls(**data)
        
    def get_custo_total(self) -> float:
        """Calcula o custo total do imóvel"""
        return self.custo_aquisicao + self.custos_reforma + self.custos_transacao
        
    def get_lucro_credor(self) -> float:
        """Calcula o lucro do credor"""
        return self.get_custo_total() * (self.percentual_lucro_credor / 100)
        
    def get_endereco_completo(self) -> str:
        """Retorna o endereço completo formatado"""
        endereco_parts = [self.endereco, self.cidade, self.estado]
        if self.cep:
            endereco_parts.append(self.cep)
        return ", ".join(filter(None, endereco_parts))
        
    def __str__(self) -> str:
        return f"Imóvel {self.id}: {self.get_endereco_completo()}"
        
    def __repr__(self) -> str:
        return f"<Imovel(id={self.id}, endereco='{self.endereco}', cidade='{self.cidade}')>"
