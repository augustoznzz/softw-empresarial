#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tabela de imóveis com filtros e ordenação
"""

import logging
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                               QTableWidgetItem, QHeaderView, QLabel, QPushButton,
                               QGroupBox, QFrame, QMessageBox, QFileDialog)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QColor, QPalette

from models.imovel import Imovel
from models.database import DatabaseManager
from utils.formatacao import formatar_moeda
from services.calculo_service import CalculoService
from services.export_service import ExportService

class TabelaImoveis(QWidget):
    imovel_selecionado = Signal(Imovel)
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.calculo_service = CalculoService()
        self.export_service = ExportService()
        self.imoveis = []
        self.imoveis_filtrados = []
        self.imovel_selecionado_atual = None
        self.setup_ui()
        self.setup_connections()
        self.carregar_imoveis()
        
    def setup_ui(self):
        """Configura a interface da tabela de imóveis"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Estilo moderno para o widget
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #495057;
            }
            QLabel {
                color: #495057;
                font-weight: 500;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0056b3, stop:1 #004085);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #004085, stop:1 #003d7a);
            }
        """)
        
        # Cabeçalho da tabela
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Título
        title_label = QLabel("📋 Lista de Imóveis")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #495057;
            }
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Botões de ação
        self.btn_novo = QPushButton("➕ Novo Imóvel")
        self.btn_novo.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #2ecc71);
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
            }
        """)
        header_layout.addWidget(self.btn_novo)
        
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_editar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f39c12, stop:1 #e67e22);
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e67e22, stop:1 #f39c12);
            }
        """)
        header_layout.addWidget(self.btn_editar)
        
        self.btn_excluir = QPushButton("🗑️ Excluir")
        self.btn_excluir.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c0392b, stop:1 #a93226);
            }
        """)
        header_layout.addWidget(self.btn_excluir)
        
        # Botões de exportação
        self.btn_export_pdf = QPushButton("📄 PDF")
        self.btn_export_excel = QPushButton("📊 Excel")
        
        header_layout.addWidget(self.btn_export_pdf)
        header_layout.addWidget(self.btn_export_excel)
        
        layout.addWidget(header_widget)
        
        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #dee2e6;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #f1f3f4;
            }
            QTableWidget::item:selected {
                background-color: #000000 !important;
                color: #ffffff !important;
            }
            QTableWidget::item:selected:active {
                background-color: #000000 !important;
                color: #ffffff !important;
            }
            QTableWidget::item:hover {
                background-color: #e3f2fd;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                color: #495057;
                padding: 16px 8px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                font-size: 12px;
            }
            QHeaderView::section:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e9ecef, stop:1 #dee2e6);
            }
        """)
        
        # Configurar cabeçalhos - Removido ID e endereço, mantido apenas CEP
        headers = [
            "CEP", "Cidade", "Estado", 
            "Custo Total (R$)", "Preço Estimado (R$)", "Margem (R$)", "ROI (%)"
        ]
        self.tabela.setColumnCount(len(headers))
        self.tabela.setHorizontalHeaderLabels(headers)
        
        # Configurar comportamento da tabela
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.setSortingEnabled(True)
        
        # Configurar altura mínima para mostrar pelo menos 5 linhas
        self.tabela.setMinimumHeight(250)
        self.tabela.verticalHeader().setDefaultSectionSize(50)
        
        # Ajustar tamanhos das colunas - Aumentado em 5%
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # CEP
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Cidade
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Estado
        header.setSectionResizeMode(3, QHeaderView.Fixed)  # Custo Total
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # Preço Estimado
        header.setSectionResizeMode(5, QHeaderView.Fixed)  # Margem
        header.setSectionResizeMode(6, QHeaderView.Fixed)  # ROI (%)
        
        # Definir larguras fixas para as colunas monetárias (aumentadas em 5%)
        header.resizeSection(3, 147)  # Custo Total: 140 + 5% = 147px
        header.resizeSection(4, 158)  # Preço Estimado: 150 + 5% = 158px
        header.resizeSection(5, 126)  # Margem: 120 + 5% = 126px
        header.resizeSection(6, 95)   # ROI: 90 + 5% = 95px
        
        # Conectar sinais
        self.tabela.itemSelectionChanged.connect(self.on_selecao_alterada)
        self.tabela.itemChanged.connect(self.on_item_changed)
        
        # Configurar células editáveis para valores financeiros
        self.tabela.setEditTriggers(QTableWidget.DoubleClicked)
        
        layout.addWidget(self.tabela)
        
        # Status da tabela
        self.status_label = QLabel("Nenhum imóvel carregado")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-style: italic;
                padding: 10px;
                text-align: center;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
    def setup_connections(self):
        """Configura as conexões dos botões"""
        # Conectar botões de ação
        self.btn_novo.clicked.connect(self.novo_imovel)
        self.btn_editar.clicked.connect(self.editar_imovel)
        self.btn_excluir.clicked.connect(self.excluir_imovel)
        
        # Conectar botões de exportação
        self.btn_export_pdf.clicked.connect(self.exportar_pdf)
        self.btn_export_excel.clicked.connect(self.exportar_excel)
        
        # Habilitar/desabilitar botões baseado na seleção
        self.atualizar_botoes()
        
    def carregar_imoveis(self):
        """Carrega todos os imóveis do banco"""
        try:
            query = """
                SELECT id, endereco, cidade, estado, cep, metragem, 
                       custo_aquisicao, custos_reforma, custos_transacao
                FROM imoveis 
                ORDER BY cidade, cep
            """
            results = self.db_manager.execute_query(query)
            
            self.imoveis = []
            for row in results:
                imovel = Imovel(
                    id=row[0], endereco=row[1], cidade=row[2], estado=row[3],
                    cep=row[4], metragem=row[5], quartos=0, banheiros=0,
                    ano=2020, padrao_acabamento="medio", custo_aquisicao=row[6],
                    custos_reforma=row[7], custos_transacao=row[8], status="em_analise"
                )
                self.imoveis.append(imovel)
            
            self.imoveis_filtrados = self.imoveis.copy()
            self.atualizar_tabela()
            self.status_label.setText(f"{len(self.imoveis)} imóveis carregados")
            
        except Exception as e:
            logging.error(f"Erro ao carregar imóveis: {e}")
            self.status_label.setText("Erro ao carregar imóveis")
            
    def atualizar_tabela(self):
        """Atualiza a tabela com os imóveis filtrados"""
        self.tabela.setRowCount(len(self.imoveis_filtrados))
        
        for row, imovel in enumerate(self.imoveis_filtrados):
            # Calcular valores financeiros
            calculos = self.calculo_service.calcular_tudo(imovel)
            
            # CEP (agora na posição 0)
            self.tabela.setItem(row, 0, QTableWidgetItem(imovel.cep))
            
            # Cidade (agora na posição 1)
            self.tabela.setItem(row, 1, QTableWidgetItem(imovel.cidade))
            
            # Estado (agora na posição 2)
            self.tabela.setItem(row, 2, QTableWidgetItem(imovel.estado))
            
            # Custo Total (agora na posição 3)
            custo_total = calculos['custo_total']
            self.tabela.setItem(row, 3, QTableWidgetItem(formatar_moeda(custo_total)))
            
            # Preço Estimado (agora na posição 4)
            preco_estimado = calculos['preco_venda_estimado']
            self.tabela.setItem(row, 4, QTableWidgetItem(formatar_moeda(preco_estimado)))
            
            # Margem (agora na posição 5)
            margem = calculos['margem']
            margem_item = QTableWidgetItem(formatar_moeda(margem))
            if margem > 0:
                margem_item.setBackground(QColor(220, 255, 220))  # Verde claro
            elif margem < 0:
                margem_item.setBackground(QColor(255, 220, 220))  # Vermelho claro
            else:
                margem_item.setBackground(QColor(255, 255, 220))  # Amarelo claro
            self.tabela.setItem(row, 5, margem_item)
            
            # ROI (agora na posição 6)
            roi = calculos['roi']
            roi_item = QTableWidgetItem(f"{roi:.1f}%")
            if roi > 20:
                roi_item.setBackground(QColor(220, 255, 220))  # Verde claro
            elif roi < 0:
                roi_item.setBackground(QColor(255, 220, 220))  # Vermelho claro
            else:
                roi_item.setBackground(QColor(255, 255, 220))  # Amarelo claro
            self.tabela.setItem(row, 6, roi_item)
            
    def aplicar_filtros(self, filtros):
        """Aplica filtros à lista de imóveis"""
        self.imoveis_filtrados = []
        
        for imovel in self.imoveis:
            if self.imovel_atende_filtros(imovel, filtros):
                self.imoveis_filtrados.append(imovel)
        
        self.atualizar_tabela()
        self.status_label.setText(f"{len(self.imoveis_filtrados)} imóveis encontrados")
        
    def imovel_atende_filtros(self, imovel, filtros):
        """Verifica se um imóvel atende aos filtros aplicados"""
        # Busca por CEP
        if 'cep' in filtros and filtros['cep']:
            cep_busca = filtros['cep'].replace('-', '').replace('.', '')
            cep_imovel = imovel.cep.replace('-', '').replace('.', '')
            if cep_busca not in cep_imovel:
                return False
        
        # Filtro por região
        if 'regiao' in filtros and filtros['regiao'] != "Todas as regiões":
            if not self.imovel_pertence_regiao(imovel, filtros['regiao']):
                return False
        
        # Filtro por cidade
        if 'cidade' in filtros and filtros['cidade'] != "Todas as cidades":
            if imovel.cidade != filtros['cidade']:
                return False
        
        # Filtro por estado
        if 'estado' in filtros:
            if imovel.estado != filtros['estado']:
                return False
        
        return True
        
    def imovel_pertence_regiao(self, imovel, regiao):
        """Verifica se um imóvel pertence a uma região específica"""
        # Mapeamento de cidades para regiões em Santa Catarina
        regioes = {
            "Norte": ["Joinville", "São Francisco do Sul", "Itapoá", "Araquari", "Garuva", "Itajaí", "Balneário Camboriú", "Navegantes", "Penha", "Piçarras", "Itapema", "Bombinhas", "Porto Belo", "Tijucas", "Biguaçu", "São José", "Palhoça", "Paulo Lopes", "Garopaba", "Imbituba", "Laguna", "Tubarão", "Criciúma", "Içara", "Urussanga", "Siderópolis", "Nova Veneza", "Forquilhinha", "Meleiro", "Morro da Fumaça", "Cocal do Sul", "Ermo", "Jaguaruna", "Pedras Grandes", "Treze de Maio", "São Ludgero", "Braço do Norte", "Grão Pará", "Orleans", "Lauro Müller", "Urubici", "Bom Jardim da Serra", "São Joaquim", "Bom Retiro", "Ponte Alta", "Urupema", "Lages", "Otacílio Costa", "Bocaina do Sul", "São José do Cerrito", "Ponte Alta do Norte", "Curitibanos", "Ponte Alta do Sul", "Brunópolis", "Campos Novos", "Abelardo Luz", "Coronel Martins", "Entre Rios", "Galvão", "Ipuaçu", "Jupiá", "Lacerdópolis", "Lajeado Grande", "Marema", "Ouro Verde", "Passos Maia", "Vargeão", "Xanxerê", "Xaxim", "Águas de Chapecó", "Águas Frias", "Bandeirante", "Barra Bonita", "Belmonte", "Bom Jesus do Oeste", "Caibi", "Campo Erê", "Caxambu do Sul", "Chapecó", "Cordilheira Alta", "Cunha Porã", "Cunhataí", "Flor do Sertão", "Formosa do Sul", "Guatambu", "Irati", "Jardinópolis", "Maravilha", "Modelo", "Nova Erechim", "Nova Itaberaba", "Palmitos", "Pinhalzinho", "Planalto Alegre", "Quilombo", "Riqueza", "Romelândia", "Saltinho", "Santa Terezinha do Progresso", "Santiago do Sul", "São Bernardino", "São Carlos", "São Lourenço do Oeste", "Saudades", "Serra Alta", "Sul Brasil", "Tigrinhos", "Tunápolis", "União do Oeste", "Vidal Ramos", "Videira", "Arroio Trinta", "Caçador", "Calmon", "Catanduvas", "Erval Velho", "Fraiburgo", "Herval d'Oeste", "Ibiam", "Ibicaré", "Iomerê", "Jaborá", "Lebon Régis", "Lindóia do Sul", "Luzerna", "Macieira", "Matos Costa", "Ouro", "Pinheiro Preto", "Rio das Antas", "Salto Veloso", "Tangará", "Treze Tílias", "Vargem Bonita", "Zortéa"],
            "Sul": ["Araranguá", "Balneário Arroio do Silva", "Balneário Gaivota", "Balneário Rincão", "Balneário Camboriú", "Bombinhas", "Botuverá", "Braço do Norte", "Brusque", "Camboriú", "Criciúma", "Ermo", "Forquilhinha", "Gaspar", "Guabiruba", "Içara", "Imbituba", "Itajaí", "Itapema", "Jaguaruna", "Laguna", "Meleiro", "Morro da Fumaça", "Navegantes", "Nova Veneza", "Orleans", "Palhoça", "Paulo Lopes", "Penha", "Piçarras", "Porto Belo", "Sangão", "São João Batista", "São José", "Siderópolis", "Tijucas", "Tubarão", "Urussanga"],
            "Leste": ["Balneário Camboriú", "Balneário Piçarras", "Bombinhas", "Camboriú", "Garopaba", "Imbituba", "Itajaí", "Itapema", "Laguna", "Navegantes", "Palhoça", "Paulo Lopes", "Penha", "Piçarras", "Porto Belo", "São José", "Tijucas"],
            "Oeste": ["Abelardo Luz", "Águas de Chapecó", "Águas Frias", "Bandeirante", "Barra Bonita", "Belmonte", "Bom Jesus do Oeste", "Caibi", "Campo Erê", "Caxambu do Sul", "Chapecó", "Cordilheira Alta", "Cunha Porã", "Cunhataí", "Dionísio Cerqueira", "Entre Rios", "Flor do Sertão", "Formosa do Sul", "Galvão", "Guatambu", "Guaraciaba", "Guarujá do Sul", "Irati", "Iraceminha", "Itapiranga", "Jardinópolis", "Joaçaba", "Lacerdópolis", "Lajeado Grande", "Marema", "Maravilha", "Mondaí", "Modelo", "Nova Erechim", "Nova Itaberaba", "Nova Veneza", "Ouro Verde", "Palmitos", "Paraíso", "Passos Maia", "Peritiba", "Pinhalzinho", "Pinheiro Preto", "Planalto Alegre", "Quilombo", "Rio das Antas", "Riqueza", "Romelândia", "Saltinho", "Santa Terezinha do Progresso", "Santiago do Sul", "São Bernardino", "São Carlos", "São Domingos", "São João do Oeste", "São José do Cedro", "São Lourenço do Oeste", "São Miguel da Boa Vista", "São Miguel do Oeste", "Saudades", "Serra Alta", "Sul Brasil", "Tigrinhos", "Tunápolis", "União do Oeste", "Vidal Ramos", "Videira", "Xanxerê", "Xaxim", "Zortéa", "Capinzal"],
            "Central": ["Alfredo Wagner", "Anita Garibaldi", "Bom Jardim da Serra", "Bom Retiro", "Botuverá", "Braço do Norte", "Brunópolis", "Campos Novos", "Catanduvas", "Celso Ramos", "Correia Pinto", "Curitibanos", "Erval Velho", "Fraiburgo", "Frei Rogério", "Herval d'Oeste", "Ibiam", "Ibicaré", "Iomerê", "Jaborá", "Lacerdópolis", "Lages", "Lebon Régis", "Lindóia do Sul", "Luzerna", "Macieira", "Matos Costa", "Monte Carlo", "Ouro", "Painel", "Palmeira", "Ponte Alta", "Ponte Alta do Norte", "Ponte Alta do Sul", "Rio Rufino", "Salto Veloso", "Santa Cecília", "São Joaquim", "São José do Cerrito", "Tangará", "Treze Tílias", "Urupema", "Vargem Bonita", "Videira", "Zortéa"]
        }
        
        if regiao in regioes:
            return imovel.cidade in regioes[regiao]
        return False
        
    def on_selecao_alterada(self):
        """Chamado quando a seleção da tabela é alterada"""
        current_row = self.tabela.currentRow()
        if current_row >= 0 and current_row < len(self.imoveis_filtrados):
            imovel_selecionado = self.imoveis_filtrados[current_row]
            self.imovel_selecionado_atual = imovel_selecionado
            self.imovel_selecionado.emit(imovel_selecionado)
        else:
            self.imovel_selecionado_atual = None
        self.atualizar_botoes()
        
    def on_item_changed(self, item):
        """Chamado quando um item da tabela é modificado"""
        if not item:
            return
            
        row = item.row()
        column = item.column()
        
        # Verificar se é uma coluna editável
        if column in [3, 4, 5]:  # Custo Total, Preço Estimado, Margem
            try:
                # Obter o texto digitado
                texto = item.text().strip()
                
                # Remover formatação existente (R$, pontos, espaços)
                texto_limpo = texto.replace('R$', '').replace('.', '').replace(' ', '')
                
                # Converter para número
                if texto_limpo:
                    valor = float(texto_limpo)
                    
                    # Atualizar o imóvel correspondente
                    if row < len(self.imoveis_filtrados):
                        imovel = self.imoveis_filtrados[row]
                        
                        # Aplicar cálculos automáticos baseado na coluna editada
                        if column == 3:  # Custo Total
                            self.calcular_com_custo_total(imovel, valor, row)
                        elif column == 4:  # Preço Estimado
                            self.calcular_com_preco_estimado(imovel, valor, row)
                        elif column == 5:  # Margem
                            self.calcular_com_margem(imovel, valor, row)
                        
            except ValueError:
                # Se não conseguir converter, reverter para o valor anterior
                self.atualizar_linha_calculos(row, self.imoveis_filtrados[row])
                
    def calcular_com_custo_total(self, imovel, novo_custo_total, row):
        """Calcula automaticamente quando o custo total é alterado"""
        try:
            # Calcular proporção para distribuir o novo custo total
            custo_atual = imovel.custo_aquisicao + imovel.custos_reforma + imovel.custos_transacao
            
            if custo_atual > 0:
                proporcao = novo_custo_total / custo_atual
                
                # Atualizar custos proporcionalmente
                novo_custo_aquisicao = imovel.custo_aquisicao * proporcao
                novo_custo_reforma = imovel.custos_reforma * proporcao
                novo_custo_transacao = imovel.custos_transacao * proporcao
                
                # Atualizar no banco
                query = """
                    UPDATE imoveis 
                    SET custo_aquisicao = ?, custos_reforma = ?, custos_transacao = ?
                    WHERE id = ?
                """
                self.db_manager.execute_query(query, (
                    novo_custo_aquisicao, novo_custo_reforma, novo_custo_transacao, imovel.id
                ))
                
                # Atualizar o objeto imóvel
                imovel.custo_aquisicao = novo_custo_aquisicao
                imovel.custos_reforma = novo_custo_reforma
                imovel.custos_transacao = novo_custo_transacao
                
                # Recalcular e atualizar a linha
                self.atualizar_linha_calculos(row, imovel)
                
        except Exception as e:
            logging.error(f"Erro ao calcular com custo total: {e}")
            
    def calcular_com_preco_estimado(self, imovel, novo_preco_estimado, row):
        """Calcula automaticamente quando o preço estimado é alterado"""
        try:
            # Atualizar o preço estimado no banco (se houver campo específico)
            # Por enquanto, vamos recalcular baseado nos custos
            self.atualizar_linha_calculos(row, imovel)
            
        except Exception as e:
            logging.error(f"Erro ao calcular com preço estimado: {e}")
            
    def calcular_com_margem(self, imovel, nova_margem, row):
        """Calcula automaticamente quando a margem é alterada"""
        try:
            # Calcular novo preço estimado baseado na margem desejada
            custo_total = imovel.custo_aquisicao + imovel.custos_reforma + imovel.custos_transacao
            novo_preco_estimado = custo_total + nova_margem
            
            # Calcular novo ROI
            if custo_total > 0:
                novo_roi = (nova_margem / custo_total) * 100
            else:
                novo_roi = 0
                
            # Atualizar a linha com os novos valores
            self.atualizar_linha_calculos(row, imovel)
            
        except Exception as e:
            logging.error(f"Erro ao calcular com margem: {e}")
            
    def atualizar_linha_calculos(self, row, imovel):
        """Atualiza os cálculos de uma linha específica"""
        try:
            # Recalcular valores financeiros
            calculos = self.calculo_service.calcular_tudo(imovel)
            
            # Atualizar Custo Total
            custo_total = calculos['custo_total']
            self.tabela.setItem(row, 3, QTableWidgetItem(formatar_moeda(custo_total)))
            
            # Atualizar Preço Estimado
            preco_estimado = calculos['preco_venda_estimado']
            self.tabela.setItem(row, 4, QTableWidgetItem(formatar_moeda(preco_estimado)))
            
            # Atualizar Margem
            margem = calculos['margem']
            margem_item = QTableWidgetItem(formatar_moeda(margem))
            if margem > 0:
                margem_item.setBackground(QColor(220, 255, 220))  # Verde claro
            elif margem < 0:
                margem_item.setBackground(QColor(255, 220, 220))  # Vermelho claro
            else:
                margem_item.setBackground(QColor(255, 255, 220))  # Amarelo claro
            self.tabela.setItem(row, 5, margem_item)
            
            # Atualizar ROI
            roi = calculos['roi']
            roi_item = QTableWidgetItem(f"{roi:.1f}%")
            if roi > 20:
                roi_item.setBackground(QColor(220, 255, 220))  # Verde claro
            elif roi < 0:
                roi_item.setBackground(QColor(255, 220, 220))  # Vermelho claro
            else:
                roi_item.setBackground(QColor(255, 255, 220))  # Amarelo claro
            self.tabela.setItem(row, 6, roi_item)
            
        except Exception as e:
            logging.error(f"Erro ao atualizar cálculos da linha {row}: {e}")
            
    def atualizar_botoes(self):
        """Atualiza o estado dos botões baseado na seleção"""
        tem_selecao = self.imovel_selecionado_atual is not None
        self.btn_editar.setEnabled(tem_selecao)
        self.btn_excluir.setEnabled(tem_selecao)
        
    def novo_imovel(self):
        """Abre o formulário para criar um novo imóvel"""
        try:
            from ui.imovel_form import ImovelForm
            
            self.form_dialog = ImovelForm()
            self.form_dialog.imovel_salvo.connect(self.on_imovel_salvo)
            self.form_dialog.setWindowTitle("Novo Imóvel")
            self.form_dialog.show()
            
        except Exception as e:
            logging.error(f"Erro ao abrir formulário de novo imóvel: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao abrir formulário: {str(e)}")
            
    def editar_imovel(self):
        """Abre o formulário para editar o imóvel selecionado"""
        if not self.imovel_selecionado_atual:
            QMessageBox.warning(self, "Aviso", "Selecione um imóvel para editar.")
            return
            
        try:
            from ui.imovel_form import ImovelForm
            
            self.form_dialog = ImovelForm()
            self.form_dialog.imovel_salvo.connect(self.on_imovel_salvo)
            self.form_dialog.load_imovel(self.imovel_selecionado_atual)
            self.form_dialog.setWindowTitle(f"Editar Imóvel - {self.imovel_selecionado_atual.cidade}")
            self.form_dialog.show()
            
        except Exception as e:
            logging.error(f"Erro ao abrir formulário de edição: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao abrir formulário: {str(e)}")
            
    def excluir_imovel(self):
        """Exclui o imóvel selecionado"""
        if not self.imovel_selecionado_atual:
            QMessageBox.warning(self, "Aviso", "Selecione um imóvel para excluir.")
            return
            
        # Confirmar exclusão
        resposta = QMessageBox.question(
            self, 
            "Confirmar Exclusão", 
            f"Tem certeza que deseja excluir o imóvel em {self.imovel_selecionado_atual.cidade}?\n\n"
            f"CEP: {self.imovel_selecionado_atual.cep}\n"
            f"Esta ação não pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            try:
                # Excluir do banco
                query = "DELETE FROM imoveis WHERE id = ?"
                self.db_manager.execute_query(query, (self.imovel_selecionado_atual.id,))
                
                # Recarregar tabela
                self.carregar_imoveis()
                
                QMessageBox.information(self, "Sucesso", "Imóvel excluído com sucesso!")
                
            except Exception as e:
                logging.error(f"Erro ao excluir imóvel: {e}")
                QMessageBox.critical(self, "Erro", f"Erro ao excluir imóvel: {str(e)}")
                
    def exportar_pdf(self):
        """Exporta os dados filtrados para PDF"""
        try:
            # Verificar se há dados para exportar
            if not self.imoveis_filtrados:
                QMessageBox.warning(self, "Aviso", "Não há dados para exportar.")
                return
                
            # Selecionar arquivo de destino
            arquivo, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar Relatório PDF",
                f"relatorio_imoveis_{len(self.imoveis_filtrados)}_items.pdf",
                "Arquivos PDF (*.pdf)"
            )
            
            if arquivo:
                # Exportar
                sucesso = self.export_service.export_to_pdf(self.imoveis_filtrados, arquivo)
                
                if sucesso:
                    QMessageBox.information(
                        self, 
                        "Sucesso", 
                        f"Relatório PDF exportado com sucesso!\n\n"
                        f"Arquivo: {arquivo}\n"
                        f"Imóveis: {len(self.imoveis_filtrados)}"
                    )
                else:
                    QMessageBox.critical(self, "Erro", "Erro ao exportar para PDF.")
                    
        except Exception as e:
            logging.error(f"Erro na exportação PDF: {e}")
            QMessageBox.critical(self, "Erro", f"Erro na exportação PDF: {str(e)}")
            
    def exportar_excel(self):
        """Exporta os dados filtrados para Excel"""
        try:
            # Verificar se há dados para exportar
            if not self.imoveis_filtrados:
                QMessageBox.warning(self, "Aviso", "Não há dados para exportar.")
                return
                
            # Selecionar arquivo de destino
            arquivo, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar Planilha Excel",
                f"imoveis_detalhado_{len(self.imoveis_filtrados)}_items.xlsx",
                "Arquivos Excel (*.xlsx)"
            )
            
            if arquivo:
                # Exportar
                sucesso = self.export_service.export_to_excel(self.imoveis_filtrados, arquivo)
                
                if sucesso:
                    QMessageBox.information(
                        self, 
                        "Sucesso", 
                        f"Planilha Excel exportada com sucesso!\n\n"
                        f"Arquivo: {arquivo}\n"
                        f"Imóveis: {len(self.imoveis_filtrados)}"
                    )
                else:
                    QMessageBox.critical(self, "Erro", "Erro ao exportar para Excel.")
                    
        except Exception as e:
            logging.error(f"Erro na exportação Excel: {e}")
            QMessageBox.critical(self, "Erro", f"Erro na exportação Excel: {str(e)}")
            
    def on_imovel_salvo(self, imovel):
        """Chamado quando um imóvel é salvo"""
        # Recarregar a tabela para mostrar as mudanças
        self.carregar_imoveis()
        
        # Fechar o formulário se ele ainda existir
        if hasattr(self, 'form_dialog'):
            self.form_dialog.close()
    
    # Métodos públicos para compatibilidade
    def carregar_imoveis(self):
        """Método público para carregar imóveis"""
        self._carregar_imoveis()
    
    def atualizar_tabela(self):
        """Método público para atualizar a tabela"""
        self._atualizar_tabela()
    
    def aplicar_filtros(self, filtros):
        """Método público para aplicar filtros"""
        self._aplicar_filtros(filtros)
    
    def novo_imovel(self):
        """Método público para criar novo imóvel"""
        self._novo_imovel()
    
    def editar_imovel(self):
        """Método público para editar imóvel"""
        self._editar_imovel()
    
    def excluir_imovel(self):
        """Método público para excluir imóvel"""
        self._excluir_imovel()
    
    def exportar_pdf(self):
        """Método público para exportar PDF"""
        self._exportar_pdf()
    
    def exportar_excel(self):
        """Método público para exportar Excel"""
        self._exportar_excel()
