#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serviço para gerenciar cidades de Santa Catarina
Sistema híbrido: banco local + API online
"""

import sqlite3
import requests
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time

class CidadeService:
    def __init__(self, db_path="imoveis.db"):
        self.db_path = db_path
        self.api_url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/42/municipios"
        self.cache_duration = timedelta(days=7)  # Cache por 7 dias
        self.init_database()
        
    def init_database(self):
        """Inicializa a tabela de cidades no banco"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Criar tabela de cidades se não existir
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS cidades_sc (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        codigo_ibge TEXT UNIQUE,
                        nome TEXT NOT NULL,
                        regiao TEXT NOT NULL,
                        latitude REAL,
                        longitude REAL,
                        populacao INTEGER,
                        ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        fonte TEXT DEFAULT 'ibge'
                    )
                """)
                
                # Criar índices para performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_cidades_nome ON cidades_sc(nome)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_cidades_regiao ON cidades_sc(regiao)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_cidades_ibge ON cidades_sc(codigo_ibge)")
                
                conn.commit()
                
        except Exception as e:
            logging.error(f"Erro ao inicializar tabela de cidades: {e}")
            raise
    
    def get_regiao_por_nome_cidade(self, nome_cidade: str) -> str:
        """Determina a região baseada no nome da cidade (mapeamento conhecido)"""
        
        # Regiões Norte - cidades conhecidas
        cidades_norte = {
            'Joinville', 'São Francisco do Sul', 'Itapoá', 'Araquari', 'Garuva',
            'São Bento do Sul', 'Campo Alegre', 'Rio Negrinho', 'Canoinhas',
            'Mafra', 'Major Vieira', 'Irineópolis', 'Monte Castelo', 'Papanduva',
            'Três Barras', 'Bela Vista do Toldo', 'Timbó Grande', 'Santa Terezinha',
            'Doutor Pedrinho', 'Corupá', 'Schroeder', 'Guaramirim', 'Massaranduba',
            'Jaraguá do Sul', 'Pomerode', 'Blumenau', 'Indaial', 'Rodeio',
            'Ascurra', 'Apiúna', 'Ibirama', 'Lontras', 'Rio do Sul',
            'Aurora', 'Agrolândia', 'Benedito Novo', 'Timbó', 'Rio dos Cedros',
            'Itaiópolis', 'Matos Costa'
        }
        
        # Regiões Sul - cidades conhecidas  
        cidades_sul = {
            'Criciúma', 'Içara', 'Nova Veneza', 'Forquilhinha', 'Siderópolis',
            'Urussanga', 'Cocal do Sul', 'Morro da Fumaça', 'Araranguá',
            'Balneário Arroio do Silva', 'Balneário Gaivota', 'Balneário Rincão',
            'Sombrio', 'Santa Rosa do Sul', 'São João do Sul', 'Passo de Torres',
            'Jacinto Machado', 'Maracajá', 'Meleiro', 'Turvo', 'Ermo',
            'Sangão', 'Jaguaruna', 'Laguna', 'Imbituba', 'Garopaba',
            'Paulo Lopes', 'Tubarão', 'Capivari de Baixo', 'Pedras Grandes',
            'Treze de Maio', 'Orleans', 'Lauro Müller', 'Bom Jardim da Serra',
            'Urubici', 'São Joaquim', 'Urupema', 'Bom Retiro'
        }
        
        # Regiões Oeste - cidades conhecidas
        cidades_oeste = {
            'Chapecó', 'São Miguel do Oeste', 'Xanxerê', 'Concórdia', 'Joaçaba',
            'Videira', 'Caçador', 'São Lourenço do Oeste', 'Palmitos', 'Caibi',
            'Maravilha', 'Cunha Porã', 'São José do Cedro', 'Guaraciaba',
            'Itapiranga', 'Mondaí', 'Riqueza', 'Romelândia', 'Bandeirante',
            'Barra Bonita', 'Belmonte', 'Descanso', 'Dionísio Cerqueira',
            'Guarujá do Sul', 'Paraíso', 'São João do Oeste', 'Tunápolis',
            'Capinzal', 'Herval d\'Oeste', 'Ouro', 'Lacerdópolis', 'Tangará',
            'Pinheiro Preto', 'Salto Veloso', 'Treze Tílias', 'Vargem Bonita',
            'Fraiburgo', 'Lebon Régis', 'Monte Carlo', 'Rio das Antas',
            'Abelardo Luz', 'Entre Rios', 'Vargeão', 'Xaxim', 'Águas de Chapecó',
            'Águas Frias', 'Caxambu do Sul', 'Cordilheira Alta', 'Cunhataí',
            'Formosa do Sul', 'Guatambu', 'Irati', 'Jardinópolis', 'Modelo',
            'Nova Erechim', 'Nova Itaberaba', 'Peritiba', 'Pinhalzinho',
            'Planalto Alegre', 'Quilombo', 'Saltinho', 'Santa Terezinha do Progresso',
            'Santiago do Sul', 'São Bernardino', 'São Carlos', 'São Domingos',
            'Saudades', 'Serra Alta', 'Sul Brasil', 'Tigrinhos', 'União do Oeste'
        }
        
        # Regiões Leste - cidades conhecidas
        cidades_leste = {
            'Florianópolis', 'São José', 'Palhoça', 'Biguaçu', 'Santo Amaro da Imperatriz',
            'Águas Mornas', 'São Pedro de Alcântara', 'Antônio Carlos', 'Governador Celso Ramos',
            'Itajaí', 'Balneário Camboriú', 'Camboriú', 'Navegantes', 'Penha',
            'Piçarras', 'Balneário Piçarras', 'Itapema', 'Porto Belo', 'Bombinhas',
            'Tijucas', 'Canelinha', 'São João Batista', 'Nova Trento', 'Major Gercino',
            'Brusque', 'Guabiruba', 'Botuverá', 'Nova Trento', 'Gaspar'
        }
        
        # Verificar se a cidade está em alguma região conhecida
        if nome_cidade in cidades_norte:
            return "Norte"
        elif nome_cidade in cidades_sul:
            return "Sul"
        elif nome_cidade in cidades_oeste:
            return "Oeste"
        elif nome_cidade in cidades_leste:
            return "Leste"
        else:
            return "Central"  # Default para cidades não mapeadas
    
    def get_regiao_por_coordenadas(self, lat: float, lon: float) -> str:
        """Fallback: Determina a região baseada nas coordenadas geográficas"""
        # Fallback simples se o mapeamento por nome não funcionar
        if lat > -27.0:
            return "Norte"
        elif lat < -28.5:
            return "Sul"
        elif lon < -52.0:
            return "Oeste"
        elif lon > -49.0:
            return "Leste"
        else:
            return "Central"
    
    def buscar_cidades_online(self) -> List[Dict]:
        """Busca cidades de SC na API do IBGE"""
        try:
            logging.info("Buscando cidades de SC na API do IBGE...")
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            cidades = response.json()
            cidades_processadas = []
            
            for cidade in cidades:
                # Obter coordenadas da cidade
                coords = self._get_coordenadas_cidade(cidade['id'])
                
                # Primeiro tentar mapear por nome da cidade
                regiao = self.get_regiao_por_nome_cidade(cidade['nome'])
                
                # Se não encontrou por nome, usar coordenadas como fallback
                if regiao == "Central" and coords.get('latitude') and coords.get('longitude'):
                    regiao = self.get_regiao_por_coordenadas(
                        coords.get('latitude', 0),
                        coords.get('longitude', 0)
                    )
                
                cidade_info = {
                    'codigo_ibge': str(cidade['id']),
                    'nome': cidade['nome'],
                    'regiao': regiao,
                    'latitude': coords.get('latitude'),
                    'longitude': coords.get('longitude'),
                    'populacao': coords.get('populacao', 0),
                    'fonte': 'ibge'
                }
                cidades_processadas.append(cidade_info)
                
                # Pequena pausa para não sobrecarregar a API
                time.sleep(0.1)
            
            logging.info(f"Encontradas {len(cidades_processadas)} cidades de SC")
            return cidades_processadas
            
        except requests.RequestException as e:
            logging.error(f"Erro ao buscar cidades online: {e}")
            return []
        except Exception as e:
            logging.error(f"Erro inesperado ao buscar cidades: {e}")
            return []
    
    def _get_coordenadas_cidade(self, codigo_ibge: int) -> Dict:
        """Obtém coordenadas e população de uma cidade específica"""
        try:
            # API do IBGE para dados da cidade
            url = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{codigo_ibge}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                cidade_data = response.json()
                
                # Tentar obter coordenadas do centro da cidade
                if 'centroide' in cidade_data:
                    return {
                        'latitude': cidade_data['centroide']['lat'],
                        'longitude': cidade_data['centroide']['lon']
                    }
                
                # Fallback: coordenadas aproximadas por região
                return self._get_coordenadas_aproximadas(cidade_data.get('nome', ''))
            
        except Exception as e:
            logging.warning(f"Erro ao obter coordenadas para cidade {codigo_ibge}: {e}")
        
        return {'latitude': 0, 'longitude': 0, 'populacao': 0}
    
    def _get_coordenadas_aproximadas(self, nome_cidade: str) -> Dict:
        """Retorna coordenadas aproximadas baseadas no nome da cidade"""
        # Coordenadas aproximadas para cidades principais
        coordenadas_aproximadas = {
            'Florianópolis': {'lat': -27.5969, 'lon': -48.5495},
            'Joinville': {'lat': -26.3044, 'lon': -48.8463},
            'Blumenau': {'lat': -26.9189, 'lon': -49.0661},
            'Criciúma': {'lat': -28.6775, 'lon': -49.3697},
            'Itajaí': {'lat': -26.9077, 'lon': -48.6618},
            'Chapecó': {'lat': -27.0969, 'lon': -52.6189},
            'Lages': {'lat': -27.8156, 'lon': -50.3264},
            'Balneário Camboriú': {'lat': -26.9922, 'lon': -48.6353},
            'Palhoça': {'lat': -27.6444, 'lon': -48.6678},
            'São José': {'lat': -27.6136, 'lon': -48.6366},
            'Tubarão': {'lat': -28.4717, 'lon': -49.0083},
            'Canoinhas': {'lat': -26.1769, 'lon': -50.3908},
            'Mafra': {'lat': -26.1111, 'lon': -49.8056},
            'Rio do Sul': {'lat': -27.2156, 'lon': -49.6433},
            'Jaraguá do Sul': {'lat': -26.4856, 'lon': -49.0717},
            'Brusque': {'lat': -27.0978, 'lon': -48.9167},
            'Navegantes': {'lat': -26.8989, 'lon': -48.6547},
            'Penha': {'lat': -26.7708, 'lon': -48.6467},
            'Piçarras': {'lat': -26.7639, 'lon': -48.6717},
            'Porto Belo': {'lat': -27.1589, 'lon': -48.5497},
            'Tijucas': {'lat': -27.2417, 'lon': -48.6333},
            'Biguaçu': {'lat': -27.4917, 'lon': -48.6583},
            'São João Batista': {'lat': -27.2750, 'lon': -48.8472},
            'Gaspar': {'lat': -26.9333, 'lon': -48.9583},
            'Guabiruba': {'lat': -27.0833, 'lon': -48.9833},
            'Indaial': {'lat': -26.9000, 'lon': -49.2333},
            'Pomerode': {'lat': -26.7389, 'lon': -49.1789},
            'Rodeio': {'lat': -26.9222, 'lon': -49.3667},
            'Doutor Pedrinho': {'lat': -26.7167, 'lon': -49.4833},
            'Benedito Novo': {'lat': -26.7833, 'lon': -49.3667},
            'Botuverá': {'lat': -27.2000, 'lon': -49.0667},
            'Major Gercino': {'lat': -27.4167, 'lon': -48.9500},
            'Nova Trento': {'lat': -27.2833, 'lon': -48.9333},
            'Leoberto Leal': {'lat': -27.5000, 'lon': -49.2833},
            'Angelina': {'lat': -27.5667, 'lon': -48.9833},
            'Rancho Queimado': {'lat': -27.6833, 'lon': -49.0167},
            'Anitápolis': {'lat': -27.9000, 'lon': -49.1333},
            'Capinzal': {'lat': -27.3406, 'lon': -51.6117},
            'Ouro': {'lat': -27.3333, 'lon': -51.6167},
            'Lacerdópolis': {'lat': -27.2500, 'lon': -51.5500},
            'Herval d\'Oeste': {'lat': -27.2000, 'lon': -51.5000},
            'Fraiburgo': {'lat': -27.0167, 'lon': -50.9167},
            'Videira': {'lat': -27.0167, 'lon': -51.1500},
            'Tangará': {'lat': -27.1000, 'lon': -51.2333},
            'Pinheiro Preto': {'lat': -27.0500, 'lon': -51.2333},
            'Salto Veloso': {'lat': -26.9000, 'lon': -51.4000},
            'Treze Tílias': {'lat': -27.0000, 'lon': -51.4000},
            'Vargem Bonita': {'lat': -27.0167, 'lon': -51.7333},
            'Monte Carlo': {'lat': -27.2167, 'lon': -50.9833},
            'Lebon Régis': {'lat': -26.9333, 'lon': -50.7000},
            'Brunópolis': {'lat': -27.3000, 'lon': -49.8000},
            'Curitibanos': {'lat': -27.2833, 'lon': -50.5833},
            'Campos Novos': {'lat': -27.4000, 'lon': -49.6333},
            'Abelardo Luz': {'lat': -26.5667, 'lon': -52.3333},
            'Coronel Martins': {'lat': -26.5167, 'lon': -52.6667},
            'Entre Rios': {'lat': -26.7167, 'lon': -52.5667},
            'Galvão': {'lat': -26.4500, 'lon': -52.6833},
            'Ipuaçu': {'lat': -26.6333, 'lon': -52.4500},
            'Jupiá': {'lat': -26.4000, 'lon': -52.7333},
            'Lacerdópolis': {'lat': -27.2500, 'lon': -51.5500},
            'Lajeado Grande': {'lat': -26.8500, 'lon': -52.5667},
            'Marema': {'lat': -26.8000, 'lon': -52.6167},
            'Ouro Verde': {'lat': -26.7000, 'lon': -52.3167},
            'Passos Maia': {'lat': -26.7833, 'lon': -52.0667},
            'Vargeão': {'lat': -26.8667, 'lon': -52.1500},
            'Xanxerê': {'lat': -26.8833, 'lon': -52.4000},
            'Xaxim': {'lat': -26.9667, 'lon': -52.5333},
            'Águas de Chapecó': {'lat': -27.0667, 'lon': -52.9833},
            'Águas Frias': {'lat': -26.8833, 'lon': -52.8667},
            'Bandeirante': {'lat': -26.7667, 'lon': -53.6333},
            'Barra Bonita': {'lat': -26.6500, 'lon': -53.4333},
            'Belmonte': {'lat': -26.8333, 'lon': -53.5833},
            'Bom Jesus do Oeste': {'lat': -26.7167, 'lon': -53.1000},
            'Caibi': {'lat': -27.0667, 'lon': -53.2500},
            'Campo Erê': {'lat': -26.4000, 'lon': -53.1000},
            'Caxambu do Sul': {'lat': -27.1667, 'lon': -52.8833},
            'Chapecó': {'lat': -27.0969, 'lon': -52.6189},
            'Cordilheira Alta': {'lat': -26.9833, 'lon': -52.6000},
            'Cunha Porã': {'lat': -26.8833, 'lon': -53.1667},
            'Cunhataí': {'lat': -26.9667, 'lon': -53.1000},
            'Dionísio Cerqueira': {'lat': -26.2500, 'lon': -53.6333},
            'Flor do Sertão': {'lat': -26.7833, 'lon': -53.3500},
            'Formosa do Sul': {'lat': -26.6500, 'lon': -52.6667},
            'Guatambu': {'lat': -27.1333, 'lon': -52.7833},
            'Guaraciaba': {'lat': -26.6000, 'lon': -53.5167},
            'Guarujá do Sul': {'lat': -26.3833, 'lon': -53.5333},
            'Irati': {'lat': -26.6500, 'lon': -52.9000},
            'Iraceminha': {'lat': -26.8167, 'lon': -53.2833},
            'Itapiranga': {'lat': -27.1667, 'lon': -53.7167},
            'Jardinópolis': {'lat': -26.7167, 'lon': -52.8500},
            'Joaçaba': {'lat': -27.1667, 'lon': -49.7833},
            'Maravilha': {'lat': -26.7667, 'lon': -53.1667},
            'Mondaí': {'lat': -27.1000, 'lon': -53.4000},
            'Modelo': {'lat': -26.7833, 'lon': -53.0500},
            'Nova Erechim': {'lat': -26.9000, 'lon': -52.9000},
            'Nova Itaberaba': {'lat': -26.9500, 'lon': -52.8000},
            'Nova Veneza': {'lat': -28.6333, 'lon': -49.5000},
            'Palmitos': {'lat': -27.0667, 'lon': -53.1667},
            'Paraíso': {'lat': -26.6167, 'lon': -53.6833},
            'Peritiba': {'lat': -27.0667, 'lon': -52.7333},
            'Pinhalzinho': {'lat': -26.8500, 'lon': -52.9833},
            'Pinheiro Preto': {'lat': -27.0500, 'lon': -51.2333},
            'Planalto Alegre': {'lat': -27.0667, 'lon': -52.8667},
            'Quilombo': {'lat': -26.7333, 'lon': -52.7167},
            'Rio das Antas': {'lat': -26.9000, 'lon': -49.7833},
            'Riqueza': {'lat': -27.0667, 'lon': -53.3333},
            'Romelândia': {'lat': -26.6833, 'lon': -53.3167},
            'Saltinho': {'lat': -26.6000, 'lon': -53.0500},
            'Santa Terezinha do Progresso': {'lat': -26.6167, 'lon': -52.9667},
            'Santiago do Sul': {'lat': -26.6333, 'lon': -52.6833},
            'São Bernardino': {'lat': -26.4667, 'lon': -52.9667},
            'São Carlos': {'lat': -27.0667, 'lon': -53.0000},
            'São Domingos': {'lat': -26.5500, 'lon': -52.5333},
            'São João do Oeste': {'lat': -27.1000, 'lon': -53.6000},
            'São José do Cedro': {'lat': -26.4500, 'lon': -53.5000},
            'São Lourenço do Oeste': {'lat': -26.3667, 'lon': -52.8500},
            'São Miguel da Boa Vista': {'lat': -26.9500, 'lon': -53.2500},
            'São Miguel do Oeste': {'lat': -26.7167, 'lon': -53.5167},
            'Saudades': {'lat': -26.9167, 'lon': -53.0000},
            'Serra Alta': {'lat': -26.7167, 'lon': -53.0500},
            'Sul Brasil': {'lat': -26.7333, 'lon': -52.9667},
            'Tigrinhos': {'lat': -26.6833, 'lon': -53.1500},
            'Tunápolis': {'lat': -26.9667, 'lon': -53.6333},
            'União do Oeste': {'lat': -26.7667, 'lon': -52.8500},
            'Vidal Ramos': {'lat': -27.3833, 'lon': -49.3667}
        }
        
        for nome, coords in coordenadas_aproximadas.items():
            if nome.lower() in nome_cidade.lower():
                return {'latitude': coords['lat'], 'longitude': coords['lon'], 'populacao': 0}
        
        return {'latitude': 0, 'longitude': 0, 'populacao': 0}
    
    def sincronizar_cidades(self, forcar_atualizacao: bool = False) -> bool:
        """Sincroniza cidades locais com dados online"""
        try:
            # Verificar se precisa atualizar
            if not forcar_atualizacao and not self._precisa_atualizar():
                logging.info("Cache de cidades ainda válido")
                return True
            
            # Buscar cidades online
            cidades_online = self.buscar_cidades_online()
            if not cidades_online:
                logging.warning("Não foi possível obter cidades online")
                return False
            
            # Atualizar banco local
            self._atualizar_cidades_locais(cidades_online)
            
            logging.info("Cidades sincronizadas com sucesso")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao sincronizar cidades: {e}")
            return False
    
    def _precisa_atualizar(self) -> bool:
        """Verifica se o cache de cidades precisa ser atualizado"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*) FROM cidades_sc 
                    WHERE ultima_atualizacao > ?
                """, (datetime.now() - self.cache_duration,))
                
                count = cursor.fetchone()[0]
                return count == 0
                
        except Exception as e:
            logging.error(f"Erro ao verificar cache: {e}")
            return True
    
    def _atualizar_cidades_locais(self, cidades: List[Dict]):
        """Atualiza as cidades no banco local"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Limpar cidades antigas
                cursor.execute("DELETE FROM cidades_sc")
                
                # Inserir novas cidades
                for cidade in cidades:
                    cursor.execute("""
                        INSERT INTO cidades_sc 
                        (codigo_ibge, nome, regiao, latitude, longitude, populacao, fonte, ultima_atualizacao)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        cidade['codigo_ibge'],
                        cidade['nome'],
                        cidade['regiao'],
                        cidade['latitude'],
                        cidade['longitude'],
                        cidade['populacao'],
                        cidade['fonte'],
                        datetime.now()
                    ))
                
                conn.commit()
                logging.info(f"{len(cidades)} cidades atualizadas no banco local")
                
        except Exception as e:
            logging.error(f"Erro ao atualizar cidades locais: {e}")
            raise
    
    def get_cidades_por_regiao(self, regiao: str = None) -> List[Dict]:
        """Retorna cidades filtradas por região"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if regiao and regiao != "Todas as regiões":
                    cursor.execute("""
                        SELECT nome, regiao, latitude, longitude, populacao
                        FROM cidades_sc 
                        WHERE regiao = ?
                        ORDER BY nome
                    """, (regiao,))
                else:
                    cursor.execute("""
                        SELECT nome, regiao, latitude, longitude, populacao
                        FROM cidades_sc 
                        ORDER BY nome
                    """)
                
                cidades = []
                for row in cursor.fetchall():
                    cidades.append({
                        'nome': row[0],
                        'regiao': row[1],
                        'latitude': row[2],
                        'longitude': row[3],
                        'populacao': row[4]
                    })
                
                return cidades
                
        except Exception as e:
            logging.error(f"Erro ao buscar cidades por região: {e}")
            return []
    
    def get_todas_cidades(self) -> List[str]:
        """Retorna lista de todas as cidades ordenadas alfabeticamente"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nome FROM cidades_sc ORDER BY nome")
                
                return [row[0] for row in cursor.fetchall()]
                
        except Exception as e:
            logging.error(f"Erro ao buscar todas as cidades: {e}")
            return []
    
    def get_regioes_disponiveis(self) -> List[str]:
        """Retorna lista de regiões disponíveis"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT regiao FROM cidades_sc ORDER BY regiao")
                
                return [row[0] for row in cursor.fetchall()]
                
        except Exception as e:
            logging.error(f"Erro ao buscar regiões: {e}")
            return []
    
    def buscar_cidade_por_nome(self, nome: str) -> Optional[Dict]:
        """Busca uma cidade específica por nome"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT nome, regiao, latitude, longitude, populacao
                    FROM cidades_sc 
                    WHERE nome LIKE ?
                    LIMIT 1
                """, (f"%{nome}%",))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'nome': row[0],
                        'regiao': row[1],
                        'latitude': row[2],
                        'longitude': row[3],
                        'populacao': row[4]
                    }
                
                return None
                
        except Exception as e:
            logging.error(f"Erro ao buscar cidade por nome: {e}")
            return None
    
    def get_estatisticas(self) -> Dict:
        """Retorna estatísticas das cidades"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total de cidades
                cursor.execute("SELECT COUNT(*) FROM cidades_sc")
                total_cidades = cursor.fetchone()[0]
                
                # Cidades por região
                cursor.execute("""
                    SELECT regiao, COUNT(*) 
                    FROM cidades_sc 
                    GROUP BY regiao 
                    ORDER BY regiao
                """)
                cidades_por_regiao = dict(cursor.fetchall())
                
                # Última atualização
                cursor.execute("""
                    SELECT MAX(ultima_atualizacao) 
                    FROM cidades_sc
                """)
                ultima_atualizacao = cursor.fetchone()[0]
                
                return {
                    'total_cidades': total_cidades,
                    'cidades_por_regiao': cidades_por_regiao,
                    'ultima_atualizacao': ultima_atualizacao,
                    'fonte': 'ibge'
                }
                
        except Exception as e:
            logging.error(f"Erro ao obter estatísticas: {e}")
            return {}
