#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de dados para parâmetros globais do sistema
"""

from typing import Dict, Any, Optional
import logging
from models.database import DatabaseManager

class ParametrosGlobais:
    def __init__(self):
        self.db_manager = DatabaseManager()
        
        # Parâmetros padrão
        self.preco_base_m2 = 5000.0
        self.fator_padrao_baixo = 0.9
        self.fator_padrao_medio = 1.0
        self.fator_padrao_alto = 1.1
        self.percentual_lucro_credor_default = 10.0
        self.lucro_desejado_investidor = 15.0
        
        # Carregar do banco
        self.load_from_db()
        
    def load_from_db(self):
        """Carrega parâmetros do banco de dados"""
        try:
            query = "SELECT chave, valor FROM parametros_globais"
            results = self.db_manager.execute_query(query)
            
            for chave, valor in results:
                if hasattr(self, chave):
                    setattr(self, chave, valor)
                    
        except Exception as e:
            logging.warning(f"Erro ao carregar parâmetros do banco: {e}")
            
    def save_to_db(self):
        """Salva parâmetros no banco de dados"""
        try:
            # Atualizar parâmetros existentes
            params_to_update = [
                ('preco_base_m2', self.preco_base_m2),
                ('fator_padrao_baixo', self.fator_padrao_baixo),
                ('fator_padrao_medio', self.fator_padrao_medio),
                ('fator_padrao_alto', self.fator_padrao_alto),
                ('percentual_lucro_credor_default', self.percentual_lucro_credor_default),
                ('lucro_desejado_investidor', self.lucro_desejado_investidor)
            ]
            
            for chave, valor in params_to_update:
                query = """
                    UPDATE parametros_globais 
                    SET valor = ?, data_atualizacao = CURRENT_TIMESTAMP 
                    WHERE chave = ?
                """
                self.db_manager.execute_query(query, (valor, chave))
                
        except Exception as e:
            logging.error(f"Erro ao salvar parâmetros no banco: {e}")
            raise
            
    def get_fator_padrao(self, padrao: str) -> float:
        """Retorna o fator para um padrão de acabamento específico"""
        padrao_map = {
            'baixo': self.fator_padrao_baixo,
            'medio': self.fator_padrao_medio,
            'alto': self.fator_padrao_alto
        }
        return padrao_map.get(padrao, 1.0)
        
    def to_dict(self) -> Dict[str, Any]:
        """Converte os parâmetros para dicionário"""
        return {
            'preco_base_m2': self.preco_base_m2,
            'fator_padrao_baixo': self.fator_padrao_baixo,
            'fator_padrao_medio': self.fator_padrao_medio,
            'fator_padrao_alto': self.fator_padrao_alto,
            'percentual_lucro_credor_default': self.percentual_lucro_credor_default,
            'lucro_desejado_investidor': self.lucro_desejado_investidor
        }
        
    def update_from_dict(self, data: Dict[str, Any]):
        """Atualiza parâmetros a partir de um dicionário"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
                
        # Salvar no banco
        self.save_to_db()
        
    def reset_to_defaults(self):
        """Reseta parâmetros para valores padrão"""
        self.preco_base_m2 = 5000.0
        self.fator_padrao_baixo = 0.9
        self.fator_padrao_medio = 1.0
        self.fator_padrao_alto = 1.1
        self.percentual_lucro_credor_default = 10.0
        self.lucro_desejado_investidor = 15.0
        
        self.save_to_db()
        
    def __str__(self) -> str:
        return f"Parâmetros: Preço Base m²={self.preco_base_m2}, Lucro Investidor={self.lucro_desejado_investidor}%"
        
    def __repr__(self) -> str:
        return f"<ParametrosGlobais(preco_base_m2={self.preco_base_m2}, lucro_investidor={self.lucro_desejado_investidor})>"
