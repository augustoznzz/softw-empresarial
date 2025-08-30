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
                return result[0][0]
            else:
                # Retornar fator padrão se não encontrar
                logging.warning(f"Fator de localização não encontrado para {cidade}/{cep}, usando 1.0")
                return 1.0
                
        except Exception as e:
            logging.error(f"Erro ao obter fator de localização: {e}")
            return 1.0
            
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
        
    def calcular_preco_minimo(self, custo_total: float, lucro_credor: float, lucro_investidor: float) -> float:
        """Calcula o preço mínimo de venda"""
        return custo_total + lucro_credor + lucro_investidor
        
    def calcular_margem(self, preco_estimado: float, preco_minimo: float) -> float:
        """Calcula a margem de lucro"""
        return preco_estimado - preco_minimo
        
    def calcular_roi(self, margem: float, custo_total: float) -> float:
        """Calcula o ROI (Return on Investment)"""
        if custo_total > 0:
            return (margem / custo_total) * 100
        return 0.0
        
    def calcular_payback(self, margem: float, custo_total: float) -> Optional[float]:
        """Calcula o tempo de payback em meses (estimativa)"""
        if margem > 0 and custo_total > 0:
            # Estimativa: payback = custo_total / margem_mensal
            # Assumindo que a margem é anual, dividir por 12
            margem_mensal = margem / 12
            if margem_mensal > 0:
                return custo_total / margem_mensal
        return None
        
    def calcular_tudo(self, imovel: Imovel) -> Dict[str, Any]:
        """Calcula todos os valores para um imóvel"""
        try:
            # Preço de venda estimado
            preco_venda_estimado = self.calcular_preco_venda_estimado(imovel)
            
            # Custos totais
            custos = self.calcular_custos_totais(imovel)
            
            # Lucros
            lucros = self.calcular_lucros(imovel, custos['custo_total'])
            
            # Preço mínimo
            preco_minimo = self.calcular_preco_minimo(
                custos['custo_total'],
                lucros['lucro_credor'],
                lucros['lucro_investidor']
            )
            
            # Margem
            margem = self.calcular_margem(preco_venda_estimado, preco_minimo)
            
            # ROI
            roi = self.calcular_roi(margem, custos['custo_total'])
            
            # Payback
            payback = self.calcular_payback(margem, custos['custo_total'])
            
            # Fator de localização
            fator_localizacao = self.get_fator_localizacao(imovel.cidade, imovel.cep)
            
            # Fator de padrão
            fator_padrao = self.parametros.get_fator_padrao(imovel.padrao_acabamento)
            
            return {
                'preco_venda_estimado': round(preco_venda_estimado, 2),
                'custo_total': round(custos['custo_total'], 2),
                'lucro_credor': round(lucros['lucro_credor'], 2),
                'lucro_investidor': round(lucros['lucro_investidor'], 2),
                'preco_minimo': round(preco_minimo, 2),
                'margem': round(margem, 2),
                'roi': round(roi, 2),
                'payback': round(payback, 2) if payback else None,
                'fator_localizacao': fator_localizacao,
                'fator_padrao': fator_padrao,
                'percentual_credor': lucros['percentual_credor'],
                'percentual_investidor': self.parametros.lucro_desejado_investidor,
                'preco_base_m2': self.parametros.preco_base_m2
            }
            
        except Exception as e:
            logging.error(f"Erro ao calcular valores do imóvel: {e}")
            return {}
            
    def simular_cenarios(self, imovel: Imovel, percentuais_credor: list, percentuais_investidor: list) -> Dict[str, Any]:
        """Simula diferentes cenários de percentuais"""
        cenarios = {}
        
        for perc_credor in percentuais_credor:
            for perc_investidor in percentuais_investidor:
                # Criar cópia do imóvel com percentual alterado
                imovel_simulacao = Imovel(**imovel.to_dict())
                imovel_simulacao.percentual_lucro_credor = perc_credor
                
                # Calcular com novos percentuais
                resultado = self.calcular_tudo(imovel_simulacao)
                
                chave = f"credor_{perc_credor}_investidor_{perc_investidor}"
                cenarios[chave] = {
                    'percentual_credor': perc_credor,
                    'percentual_investidor': perc_investidor,
                    'margem': resultado.get('margem', 0),
                    'roi': resultado.get('roi', 0),
                    'preco_minimo': resultado.get('preco_minimo', 0)
                }
                
        return cenarios
        
    def validar_viabilidade(self, imovel: Imovel) -> Dict[str, Any]:
        """Valida a viabilidade do investimento"""
        resultado = self.calcular_tudo(imovel)
        
        margem = resultado.get('margem', 0)
        roi = resultado.get('roi', 0)
        
        # Critérios de viabilidade
        viabilidade = {
            'margem_positiva': margem > 0,
            'roi_minimo': roi >= 10,  # ROI mínimo de 10%
            'margem_minima': margem >= resultado.get('custo_total', 0) * 0.05,  # Margem mínima de 5%
            'viabilidade_geral': False
        }
        
        # Viabilidade geral
        viabilidade['viabilidade_geral'] = (
            viabilidade['margem_positiva'] and 
            viabilidade['roi_minimo'] and 
            viabilidade['margem_minima']
        )
        
        # Recomendações
        recomendacoes = []
        if not viabilidade['margem_positiva']:
            recomendacoes.append("Margem negativa - reavaliar preço ou custos")
        if not viabilidade['roi_minimo']:
            recomendacoes.append("ROI abaixo do mínimo recomendado")
        if not viabilidade['margem_minima']:
            recomendacoes.append("Margem muito baixa - risco alto")
            
        viabilidade['recomendacoes'] = recomendacoes
        
        return viabilidade
