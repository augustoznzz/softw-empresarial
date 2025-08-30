#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de dados para índices de localização
"""

from typing import Optional, Dict, Any
import logging

class LocalizacaoIndice:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.cidade = kwargs.get('cidade', '')
        self.bairro = kwargs.get('bairro', '')
        self.cep = kwargs.get('cep', '')
        self.fator_localizacao = kwargs.get('fator_localizacao', 1.0)
        self.data_criacao = kwargs.get('data_criacao')
        
        # Validações
        self.validate()
        
    def validate(self):
        """Valida os dados do índice de localização"""
        errors = []
        
        if not self.cidade:
            errors.append("Cidade é obrigatória")
            
        if self.fator_localizacao < 0.5 or self.fator_localizacao > 2.0:
            errors.append("Fator de localização deve estar entre 0.5 e 2.0")
            
        if errors:
            raise ValueError("; ".join(errors))
            
    def to_dict(self) -> Dict[str, Any]:
        """Converte o índice para dicionário"""
        return {
            'id': self.id,
            'cidade': self.cidade,
            'bairro': self.bairro,
            'cep': self.cep,
            'fator_localizacao': self.fator_localizacao,
            'data_criacao': self.data_criacao
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LocalizacaoIndice':
        """Cria um índice a partir de um dicionário"""
        return cls(**data)
        
    @classmethod
    def from_db_row(cls, row: tuple) -> 'LocalizacaoIndice':
        """Cria um índice a partir de uma linha do banco"""
        columns = ['id', 'cidade', 'bairro', 'cep', 'fator_localizacao', 'data_criacao']
        data = dict(zip(columns, row))
        return cls(**data)
        
    def get_localizacao_completa(self) -> str:
        """Retorna a localização completa formatada"""
        parts = [self.cidade]
        if self.bairro:
            parts.append(self.bairro)
        if self.cep:
            parts.append(self.cep)
        return " - ".join(parts)
        
    def __str__(self) -> str:
        return f"{self.get_localizacao_completa()} (Fator: {self.fator_localizacao:.2f})"
        
    def __repr__(self) -> str:
        return f"<LocalizacaoIndice(id={self.id}, cidade='{self.cidade}', fator={self.fator_localizacao})>"
