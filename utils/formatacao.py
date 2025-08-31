#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários de formatação para o sistema
"""

def formatar_moeda(valor: float) -> str:
    """
    Formata um valor para o padrão monetário brasileiro
    
    Args:
        valor: Valor numérico a ser formatado
        
    Returns:
        String formatada como 'R$ 123.456' (sem centavos, com pontos a cada 3 dígitos)
    """
    if valor is None:
        valor = 0.0
    
    # Converter para inteiro para remover centavos
    valor_inteiro = int(round(valor))
    
    # Formatação com pontos como separador de milhares
    valor_formatado = f"{valor_inteiro:,}".replace(",", ".")
    
    return f"R$ {valor_formatado}"


def formatar_percentual(valor: float, decimais: int = 1) -> str:
    """
    Formata um valor percentual
    
    Args:
        valor: Valor percentual
        decimais: Número de casas decimais (padrão: 1)
        
    Returns:
        String formatada como '15,2%'
    """
    if valor is None:
        valor = 0.0
    
    # Usar vírgula como separador decimal para percentuais
    valor_str = f"{valor:.{decimais}f}".replace(".", ",")
    return f"{valor_str}%"


def formatar_metragem(valor: float) -> str:
    """
    Formata metragem
    
    Args:
        valor: Valor da metragem
        
    Returns:
        String formatada como '85,5 m²'
    """
    if valor is None:
        valor = 0.0
    
    # Usar vírgula como separador decimal
    valor_str = f"{valor:.1f}".replace(".", ",")
    return f"{valor_str} m²"
