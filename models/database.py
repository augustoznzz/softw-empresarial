#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de banco de dados SQLite para o sistema de imóveis
"""

import sqlite3
import os
from datetime import datetime
import logging

class DatabaseManager:
    def __init__(self, db_path="imoveis.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Inicializa o banco de dados e cria as tabelas"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Criar tabela de imóveis
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS imoveis (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        endereco TEXT NOT NULL,
                        cidade TEXT NOT NULL,
                        estado TEXT NOT NULL,
                        cep TEXT,
                        latitude REAL,
                        longitude REAL,
                        metragem REAL NOT NULL,
                        quartos INTEGER,
                        banheiros INTEGER,
                        ano INTEGER,
                        padrao_acabamento TEXT CHECK(padrao_acabamento IN ('baixo', 'medio', 'alto')) DEFAULT 'medio',
                        custo_aquisicao REAL NOT NULL,
                        custos_reforma REAL DEFAULT 0,
                        custos_transacao REAL DEFAULT 0,
                        percentual_lucro_credor REAL DEFAULT 10.0,
                        status TEXT CHECK(status IN ('em_analise', 'comprado', 'vendido')) DEFAULT 'em_analise',
                        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Criar tabela de índices de localização
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS localizacao_indices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cidade TEXT NOT NULL,
                        bairro TEXT,
                        cep TEXT,
                        fator_localizacao REAL NOT NULL CHECK(fator_localizacao >= 0.5 AND fator_localizacao <= 2.0),
                        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Criar tabela de parâmetros globais
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS parametros_globais (
                        chave TEXT PRIMARY KEY,
                        valor REAL NOT NULL,
                        descricao TEXT,
                        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Inserir parâmetros padrão se não existirem
                self.insert_default_params(cursor)
                
                # Inserir dados de localização padrão se não existirem
                self.insert_default_localizacao(cursor)
                
                conn.commit()
                
        except Exception as e:
            logging.error(f"Erro ao inicializar banco de dados: {e}")
            raise
            
    def insert_default_params(self, cursor):
        """Insere parâmetros padrão no banco"""
        default_params = [
            ('preco_base_m2', 5000.0, 'Preço base por metro quadrado'),
            ('fator_padrao_baixo', 0.9, 'Fator para padrão de acabamento baixo'),
            ('fator_padrao_medio', 1.0, 'Fator para padrão de acabamento médio'),
            ('fator_padrao_alto', 1.1, 'Fator para padrão de acabamento alto'),
            ('percentual_lucro_credor_default', 10.0, 'Percentual padrão de lucro do credor'),
            ('lucro_desejado_investidor_default', 15.0, 'Percentual padrão de lucro desejado do investidor')
        ]
        
        for chave, valor, descricao in default_params:
            cursor.execute("""
                INSERT OR IGNORE INTO parametros_globais (chave, valor, descricao)
                VALUES (?, ?, ?)
            """, (chave, valor, descricao))
            
    def insert_default_localizacao(self, cursor):
        """Insere dados de localização padrão"""
        default_localizacoes = [
            ('Florianópolis', 'Centro', '88010-000', 1.3),
            ('Florianópolis', 'Trindade', '88040-000', 1.25),
            ('Florianópolis', 'Córrego Grande', '88037-000', 1.4),
            ('Criciúma', 'Centro', '88801-000', 0.9),
            ('Criciúma', 'São Luiz', '88802-000', 1.0),
            ('Capinzal', 'Centro', '89665-000', 0.8),
            ('Capinzal', 'Vila Nova', '89665-001', 0.85),
            ('Blumenau', 'Centro', '89010-000', 1.2),
            ('Blumenau', 'Vila Nova', '89036-000', 1.15),
            ('Joinville', 'Centro', '89201-000', 1.1),
            ('Joinville', 'Boa Vista', '89205-000', 1.05),
            ('Chapecó', 'Centro', '89801-000', 0.95)
        ]
        
        for cidade, bairro, cep, fator in default_localizacoes:
            cursor.execute("""
                INSERT OR IGNORE INTO localizacao_indices (cidade, bairro, cep, fator_localizacao)
                VALUES (?, ?, ?, ?)
            """, (cidade, bairro, cep, fator))
            
    def get_connection(self):
        """Retorna uma conexão com o banco"""
        return sqlite3.connect(self.db_path)
        
    def execute_query(self, query, params=None):
        """Executa uma query e retorna os resultados"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                    
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return cursor.rowcount
                    
        except Exception as e:
            logging.error(f"Erro ao executar query: {e}")
            raise
            
    def execute_many(self, query, params_list):
        """Executa uma query múltiplas vezes com diferentes parâmetros"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(query, params_list)
                conn.commit()
                return cursor.rowcount
                
        except Exception as e:
            logging.error(f"Erro ao executar query múltipla: {e}")
            raise
            
    def get_table_info(self, table_name):
        """Retorna informações sobre uma tabela"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info({table_name})")
                return cursor.fetchall()
                
        except Exception as e:
            logging.error(f"Erro ao obter informações da tabela: {e}")
            raise
            
    def backup_database(self, backup_path):
        """Faz backup do banco de dados"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            logging.error(f"Erro ao fazer backup: {e}")
            return False
            
    def restore_database(self, backup_path):
        """Restaura o banco de dados de um backup"""
        try:
            import shutil
            shutil.copy2(backup_path, self.db_path)
            return True
        except Exception as e:
            logging.error(f"Erro ao restaurar backup: {e}")
            return False
