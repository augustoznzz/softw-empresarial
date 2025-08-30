#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para popular o banco de dados com dados de exemplo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import DatabaseManager
import logging

def seed_imoveis():
    """Insere imóveis de exemplo no banco"""
    print("📋 Inserindo imóveis de exemplo...")
    
    db = DatabaseManager()
    
    # Lista de imóveis de Santa Catarina
    imoveis = [
        # Região Norte - Florianópolis
        {
            'endereco': 'Rua das Palmeiras, 123',
            'cidade': 'Florianópolis',
            'estado': 'SC',
            'cep': '88010-000',
            'latitude': -27.5969,
            'longitude': -48.5495,
            'metragem': 85.0,
            'quartos': 2,
            'banheiros': 1,
            'ano': 2015,
            'padrao_acabamento': 'medio',
            'custo_aquisicao': 280000.0,
            'custos_reforma': 45000.0,
            'custos_transacao': 12000.0,
            'percentual_lucro_credor': 12.0,
            'status': 'em_analise'
        },
        {
            'endereco': 'Av. Beira Mar Norte, 500',
            'cidade': 'Florianópolis',
            'estado': 'SC',
            'cep': '88015-000',
            'latitude': -27.5945,
            'longitude': -48.5477,
            'metragem': 120.0,
            'quartos': 3,
            'banheiros': 2,
            'ano': 2018,
            'padrao_acabamento': 'alto',
            'custo_aquisicao': 450000.0,
            'custos_reforma': 60000.0,
            'custos_transacao': 18000.0,
            'percentual_lucro_credor': 15.0,
            'status': 'em_analise'
        },
        {
            'endereco': 'Rua João Pio Duarte Silva, 789',
            'cidade': 'Florianópolis',
            'estado': 'SC',
            'cep': '88020-000',
            'latitude': -27.5920,
            'longitude': -48.5450,
            'metragem': 95.0,
            'quartos': 2,
            'banheiros': 2,
            'ano': 2016,
            'padrao_acabamento': 'medio',
            'custo_aquisicao': 320000.0,
            'custos_reforma': 38000.0,
            'custos_transacao': 14000.0,
            'percentual_lucro_credor': 10.0,
            'status': 'comprado'
        },
        
        # Região Sul - Capinzal
        {
            'endereco': 'Rua XV de Novembro, 456',
            'cidade': 'Capinzal',
            'estado': 'SC',
            'cep': '89665-000',
            'latitude': -27.3400,
            'longitude': -51.6100,
            'metragem': 110.0,
            'quartos': 3,
            'banheiros': 2,
            'ano': 2014,
            'padrao_acabamento': 'baixo',
            'custo_aquisicao': 180000.0,
            'custos_reforma': 25000.0,
            'custos_transacao': 8000.0,
            'percentual_lucro_credor': 8.0,
            'status': 'em_analise'
        },
        {
            'endereco': 'Av. Getúlio Vargas, 321',
            'cidade': 'Capinzal',
            'estado': 'SC',
            'cep': '89665-000',
            'latitude': -27.3420,
            'longitude': -51.6120,
            'metragem': 140.0,
            'quartos': 4,
            'banheiros': 3,
            'ano': 2017,
            'padrao_acabamento': 'medio',
            'custo_aquisicao': 250000.0,
            'custos_reforma': 35000.0,
            'custos_transacao': 10000.0,
            'percentual_lucro_credor': 12.0,
            'status': 'vendido'
        },
        
        # Região Leste - Itajaí
        {
            'endereco': 'Rua Lauro Müller, 654',
            'cidade': 'Itajaí',
            'estado': 'SC',
            'cep': '88301-000',
            'latitude': -26.9089,
            'longitude': -48.6617,
            'metragem': 90.0,
            'quartos': 2,
            'banheiros': 1,
            'ano': 2013,
            'padrao_acabamento': 'baixo',
            'custo_aquisicao': 220000.0,
            'custos_reforma': 30000.0,
            'custos_transacao': 9000.0,
            'percentual_lucro_credor': 9.0,
            'status': 'em_analise'
        },
        {
            'endereco': 'Av. Beira Rio, 987',
            'cidade': 'Itajaí',
            'estado': 'SC',
            'cep': '88302-000',
            'latitude': -26.9100,
            'longitude': -48.6630,
            'metragem': 130.0,
            'quartos': 3,
            'banheiros': 2,
            'ano': 2019,
            'padrao_acabamento': 'alto',
            'custo_aquisicao': 380000.0,
            'custos_reforma': 55000.0,
            'custos_transacao': 15000.0,
            'percentual_lucro_credor': 18.0,
            'status': 'comprado'
        },
        
        # Região Oeste - Chapecó
        {
            'endereco': 'Rua Nereu Ramos, 147',
            'cidade': 'Chapecó',
            'estado': 'SC',
            'cep': '89801-000',
            'latitude': -27.0965,
            'longitude': -52.6178,
            'metragem': 100.0,
            'quartos': 3,
            'banheiros': 2,
            'ano': 2016,
            'padrao_acabamento': 'medio',
            'custo_aquisicao': 260000.0,
            'custos_reforma': 40000.0,
            'custos_transacao': 11000.0,
            'percentual_lucro_credor': 11.0,
            'status': 'em_analise'
        },
        {
            'endereco': 'Av. Getúlio Vargas, 258',
            'cidade': 'Chapecó',
            'estado': 'SC',
            'cep': '89802-000',
            'latitude': -27.0980,
            'longitude': -52.6190,
            'metragem': 150.0,
            'quartos': 4,
            'banheiros': 3,
            'ano': 2018,
            'padrao_acabamento': 'alto',
            'custo_aquisicao': 420000.0,
            'custos_reforma': 65000.0,
            'custos_transacao': 17000.0,
            'percentual_lucro_credor': 20.0,
            'status': 'vendido'
        },
        
        # Região Central - Blumenau
        {
            'endereco': 'Rua XV de Novembro, 369',
            'cidade': 'Blumenau',
            'estado': 'SC',
            'cep': '89010-000',
            'latitude': -26.9189,
            'longitude': -49.0661,
            'metragem': 95.0,
            'quartos': 2,
            'banheiros': 2,
            'ano': 2015,
            'padrao_acabamento': 'medio',
            'custo_aquisicao': 290000.0,
            'custos_reforma': 42000.0,
            'custos_transacao': 13000.0,
            'percentual_lucro_credor': 13.0,
            'status': 'em_analise'
        },
        {
            'endereco': 'Av. Beira Rio, 741',
            'cidade': 'Blumenau',
            'estado': 'SC',
            'cep': '89012-000',
            'latitude': -26.9200,
            'longitude': -49.0680,
            'metragem': 125.0,
            'quartos': 3,
            'banheiros': 2,
            'ano': 2017,
            'padrao_acabamento': 'alto',
            'custo_aquisicao': 350000.0,
            'custos_reforma': 50000.0,
            'custos_transacao': 14000.0,
            'percentual_lucro_credor': 16.0,
            'status': 'comprado'
        }
    ]
    
    for imovel_data in imoveis:
        try:
            # Verificar se já existe
            query = """
                SELECT id FROM imoveis 
                WHERE endereco = ? AND cidade = ? AND estado = ?
            """
            existing = db.execute_query(query, (
                imovel_data['endereco'], 
                imovel_data['cidade'], 
                imovel_data['estado']
            ))
            
            if existing:
                print(f"Imóvel já existe: {imovel_data['endereco']}, {imovel_data['cidade']}")
                continue
                
            # Inserir novo imóvel
            query = """
                INSERT INTO imoveis (
                    endereco, cidade, estado, cep, latitude, longitude,
                    metragem, quartos, banheiros, ano, padrao_acabamento,
                    custo_aquisicao, custos_reforma, custos_transacao,
                    percentual_lucro_credor, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            db.execute_query(query, (
                imovel_data['endereco'], imovel_data['cidade'], imovel_data['estado'],
                imovel_data['cep'], imovel_data['latitude'], imovel_data['longitude'],
                imovel_data['metragem'], imovel_data['quartos'], imovel_data['banheiros'],
                imovel_data['ano'], imovel_data['padrao_acabamento'],
                imovel_data['custo_aquisicao'], imovel_data['custos_reforma'],
                imovel_data['custos_transacao'], imovel_data['percentual_lucro_credor'],
                imovel_data['status']
            ))
            
        except Exception as e:
            logging.error(f"Erro ao inserir imóvel {imovel_data['endereco']}: {e}")
    
    print(f"✅ {len(imoveis)} imóveis de exemplo processados!")

def seed_localizacao_indices():
    """Insere índices de localização de exemplo"""
    print("\n==================================================")
    print("📍 Inserindo índices de localização...")
    
    db = DatabaseManager()
    
    # Índices de localização para Santa Catarina
    indices = [
        # Região Norte
        {'cidade': 'Florianópolis', 'bairro': 'Centro', 'cep': '88010-000', 'fator_localizacao': 1.25},
        {'cidade': 'Florianópolis', 'bairro': 'Beira Mar Norte', 'cep': '88015-000', 'fator_localizacao': 1.40},
        {'cidade': 'Florianópolis', 'bairro': 'Trindade', 'cep': '88020-000', 'fator_localizacao': 1.15},
        {'cidade': 'Florianópolis', 'bairro': 'Córrego Grande', 'cep': '88037-000', 'fator_localizacao': 1.10},
        {'cidade': 'Florianópolis', 'bairro': 'Córrego Grande', 'cep': '88037-000', 'fator_localizacao': 1.10},
        
        # Região Sul
        {'cidade': 'Capinzal', 'bairro': 'Centro', 'cep': '89665-000', 'fator_localizacao': 0.95},
        {'cidade': 'Capinzal', 'bairro': 'Vila Nova', 'cep': '89665-000', 'fator_localizacao': 0.90},
        {'cidade': 'Capinzal', 'bairro': 'Vila Nova', 'cep': '89665-000', 'fator_localizacao': 0.90},
        
        # Região Leste
        {'cidade': 'Itajaí', 'bairro': 'Centro', 'cep': '88301-000', 'fator_localizacao': 1.20},
        {'cidade': 'Itajaí', 'bairro': 'Beira Rio', 'cep': '88302-000', 'fator_localizacao': 1.30},
        {'cidade': 'Itajaí', 'bairro': 'Cidade Nova', 'cep': '88303-000', 'fator_localizacao': 1.05},
        {'cidade': 'Itajaí', 'bairro': 'Cidade Nova', 'cep': '88303-000', 'fator_localizacao': 1.05},
        
        # Região Oeste
        {'cidade': 'Chapecó', 'bairro': 'Centro', 'cep': '89801-000', 'fator_localizacao': 1.10},
        {'cidade': 'Chapecó', 'bairro': 'Jardim Itália', 'cep': '89802-000', 'fator_localizacao': 1.15},
        {'cidade': 'Chapecó', 'bairro': 'Jardim Itália', 'cep': '89802-000', 'fator_localizacao': 1.15},
        
        # Região Central
        {'cidade': 'Blumenau', 'bairro': 'Centro', 'cep': '89010-000', 'fator_localizacao': 1.20},
        {'cidade': 'Blumenau', 'bairro': 'Beira Rio', 'cep': '89012-000', 'fator_localizacao': 1.25},
        {'cidade': 'Blumenau', 'bairro': 'Vila Nova', 'cep': '89035-000', 'fator_localizacao': 1.00},
        {'cidade': 'Blumenau', 'bairro': 'Vila Nova', 'cep': '89035-000', 'fator_localizacao': 1.00}
    ]
    
    for indice in indices:
        try:
            # Verificar se já existe
            query = """
                SELECT id FROM localizacao_indices 
                WHERE cidade = ? AND bairro = ?
            """
            existing = db.execute_query(query, (indice['cidade'], indice['bairro']))
            
            if existing:
                print(f"Índice já existe: {indice['cidade']} - {indice['bairro']}")
                continue
                
            # Inserir novo índice
            query = """
                INSERT INTO localizacao_indices (cidade, bairro, cep, fator_localizacao)
                VALUES (?, ?, ?, ?)
            """
            
            db.execute_query(query, (
                indice['cidade'], indice['bairro'], 
                indice['cep'], indice['fator_localizacao']
            ))
            
        except Exception as e:
            logging.error(f"Erro ao inserir índice {indice['cidade']}-{indice['bairro']}: {e}")
    
    print(f"✅ {len(indices)} índices de localização processados!")

def main():
    """Função principal"""
    print("🌱 Iniciando seed do banco de dados...")
    
    try:
        seed_imoveis()
        seed_localizacao_indices()
        
        print("\n==================================================")
        print("🎉 Seed concluído com sucesso!")
        print("O banco de dados foi populado com dados de Santa Catarina.")
        print("Você pode agora executar a aplicação principal.")
        
    except Exception as e:
        logging.error(f"Erro durante o seed: {e}")
        print(f"❌ Erro durante o seed: {e}")

if __name__ == "__main__":
    main()
