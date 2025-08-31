#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serviço de cálculos para preços-alvo, margens e ROI
"""

from typing import Dict, Any, Optional
from models.imovel import Imovel
from models.localizacao import LocalizacaoIndice
from models.parametros import ParametrosGlobais
from models.database import DatabaseManager
import logging

class CalculoService:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.parametros = ParametrosGlobais()
        # Cache para fatores de localização
        self._fatores_cache = {}
        
    def calcular_preco_venda_estimado(self, imovel: Imovel) -> float:
        """Calcula o preço de venda estimado do imóvel"""
        try:
            # Obter fator de localização
            fator_localizacao = self.get_fator_localizacao(imovel.cidade, imovel.cep)
            
            # Obter fator de padrão
            fator_padrao = self.parametros.get_fator_padrao(imovel.padrao_acabamento)
            
            # Calcular preço estimado
            preco_estimado = (
                self.parametros.preco_base_m2 * 
                imovel.metragem * 
                fator_localizacao * 
                fator_padrao
            )
            
            return round(preco_estimado, 2)
            
        except Exception as e:
            logging.error(f"Erro ao calcular preço de venda estimado: {e}")
            return 0.0
            
    def get_fator_localizacao(self, cidade: str, cep: str = None) -> float:
        """Obtém o fator de localização para uma cidade/CEP"""
        # Criar chave de cache
        cache_key = f"{cidade}:{cep or 'default'}"
        
        # Verificar cache primeiro
        if cache_key in self._fatores_cache:
            return self._fatores_cache[cache_key]
        
        try:
            if cep:
                query = """
                    SELECT fator_localizacao 
                    FROM localizacao_indices 
                    WHERE cidade = ? AND cep = ?
                    ORDER BY id DESC LIMIT 1
                """
                result = self.db_manager.execute_query(query, (cidade, cep))
            else:
                query = """
                    SELECT fator_localizacao 
                    FROM localizacao_indices 
                    WHERE cidade = ?
                    ORDER BY id DESC LIMIT 1
                """
                result = self.db_manager.execute_query(query, (cidade,))
                
            if result:
                fator = result[0][0]
                # Armazenar no cache
                self._fatores_cache[cache_key] = fator
                return fator
            else:
                # Retornar fator padrão se não encontrar (sem warning)
                fator_padrao = 1.0
                self._fatores_cache[cache_key] = fator_padrao
                return fator_padrao
                
        except Exception as e:
            logging.error(f"Erro ao obter fator de localização: {e}")
            fator_padrao = 1.0
            self._fatores_cache[cache_key] = fator_padrao
            return fator_padrao
            
    def calcular_custos_totais(self, imovel: Imovel) -> Dict[str, float]:
        """Calcula todos os custos do imóvel"""
        custo_aquisicao = imovel.custo_aquisicao or 0.0
        custos_reforma = imovel.custos_reforma or 0.0
        custos_transacao = imovel.custos_transacao or 0.0
        
        custo_total = custo_aquisicao + custos_reforma + custos_transacao
        
        return {
            'custo_aquisicao': custo_aquisicao,
            'custos_reforma': custos_reforma,
            'custos_transacao': custos_transacao,
            'custo_total': custo_total
        }
        
    def calcular_lucros(self, imovel: Imovel, custo_total: float) -> Dict[str, float]:
        """Calcula os lucros do credor e investidor"""
        # Lucro do credor
        percentual_credor = imovel.percentual_lucro_credor or self.parametros.percentual_lucro_credor_default
        lucro_credor = custo_total * (percentual_credor / 100)
        
        # Lucro do investidor
        lucro_investidor = custo_total * (self.parametros.lucro_desejado_investidor / 100)
        
        return {
            'percentual_credor': percentual_credor,
            'lucro_credor': lucro_credor,
            'lucro_investidor': lucro_investidor
        }
        
    def calcular_preco_minimo(self, custo_total: float, lucro_credor: float) -> float:
        """Calcula o preço mínimo de venda"""
        return custo_total + lucro_credor
        
    def calcular_margem(self, preco_venda: float, custo_total: float) -> float:
        """Calcula a margem de lucro"""
        return preco_venda - custo_total
        
    def calcular_roi(self, margem: float, custo_total: float) -> float:
        """Calcula o ROI (Return on Investment)"""
        if custo_total > 0:
            return (margem / custo_total) * 100
        return 0.0
        
    def calcular_payback(self, custo_total: float, margem_mensal: float) -> float:
        """Calcula o tempo de payback em meses"""
        if margem_mensal > 0:
            return custo_total / margem_mensal
        return float('inf')
        
    def calcular_tudo(self, imovel: Imovel) -> Dict[str, Any]:
        """Calcula todos os valores financeiros do imóvel"""
        try:
            # Calcular preço de venda estimado
            preco_venda_estimado = self.calcular_preco_venda_estimado(imovel)
            
            # Calcular custos totais
            custos = self.calcular_custos_totais(imovel)
            custo_total = custos['custo_total']
            
            # Calcular lucros
            lucros = self.calcular_lucros(imovel, custo_total)
            lucro_credor = lucros['lucro_credor']
            lucro_investidor = lucros['lucro_investidor']
            
            # Calcular preço mínimo
            preco_minimo = self.calcular_preco_minimo(custo_total, lucro_credor)
            
            # Calcular margem
            margem = self.calcular_margem(preco_venda_estimado, custo_total)
            
            # Calcular ROI
            roi = self.calcular_roi(margem, custo_total)
            
            # Calcular payback estimado (assumindo margem mensal como 1/12 da margem anual)
            margem_mensal = margem / 12 if margem > 0 else 0
            payback_meses = self.calcular_payback(custo_total, margem_mensal)
            
            return {
                'preco_venda_estimado': preco_venda_estimado,
                'custo_total': custo_total,
                'lucro_credor': lucro_credor,
                'lucro_investidor': lucro_investidor,
                'preco_minimo': preco_minimo,
                'margem': margem,
                'roi': roi,
                'payback_meses': payback_meses
            }
            
        except Exception as e:
            logging.error(f"Erro ao calcular valores do imóvel: {e}")
            # Retornar valores padrão em caso de erro
            return {
                'preco_venda_estimado': 0.0,
                'custo_total': 0.0,
                'lucro_credor': 0.0,
                'lucro_investidor': 0.0,
                'preco_minimo': 0.0,
                'margem': 0.0,
                'roi': 0.0,
                'payback_meses': 0.0
            }
            
    def limpar_cache(self):
        """Limpa o cache de fatores de localização"""
        self._fatores_cache.clear()
