#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget de filtros para a tabela de imóveis
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox,
                               QPushButton, QGroupBox, QCheckBox, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from models.database import DatabaseManager
from services.cidade_service import CidadeService
import logging

class FiltrosWidget(QWidget):
    filtros_alterados = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.cidade_service = CidadeService()
        self.init_ui()
        self.setup_connections()
        self.load_cidades()
        self.on_filtro_changed()
    
    def buscar_online(self):
        """Busca online por imóveis aplicando os filtros selecionados"""
        try:
            # Obter filtros atuais
            filtros = self.get_filtros_atuais()
            
            # Validar se pelo menos um filtro foi definido
            regiao_selecionada = self.regiao_combo.currentText()
            cidade_selecionada = self.cidade_combo.currentText()
            cep_busca = self.busca_edit.text().strip()
            
            if (regiao_selecionada == "Todas as regiões" and 
                cidade_selecionada == "Todas as cidades" and 
                not cep_busca):
                QMessageBox.information(self, "Busca Online", 
                                      "Defina pelo menos um filtro (região, cidade ou CEP) para realizar a busca online.")
                return
            
            # Construir descrição da busca
            criterios_busca = []
            if cep_busca:
                criterios_busca.append(f"CEP: {cep_busca}")
            if regiao_selecionada != "Todas as regiões":
                criterios_busca.append(f"Região: {regiao_selecionada}")
            if cidade_selecionada != "Todas as cidades":
                criterios_busca.append(f"Cidade: {cidade_selecionada}")
            
            # Filtros adicionais removidos
            
            # Simular busca online com filtros aplicados
            QMessageBox.information(self, "Busca Online", 
                                  f"🔍 Busca Online Realizada!\n\n"
                                  f"Critérios aplicados:\n" + "\n".join(f"• {c}" for c in criterios_busca) + 
                                  f"\n\nA tabela abaixo foi atualizada com os imóveis encontrados "
                                  f"que atendem aos filtros selecionados.\n\n"
                                  f"Em uma implementação real, esta busca consultaria "
                                  f"portais como Zap Imóveis, Viva Real, etc.")
            
            # Emitir sinal para atualizar a tabela com os filtros aplicados
            self.filtros_alterados.emit(filtros)
                                  
        except Exception as e:
            logging.error(f"Erro na busca online: {e}")
            QMessageBox.warning(self, "Busca Online", 
                              f"Erro ao realizar busca: {str(e)}")
        
    def init_ui(self):
        """Inicializa a interface dos filtros"""
        layout = QVBoxLayout(self)
        
        # Remover título para aproveitar melhor o espaço
        
        # Grupo de filtros com design moderno
        filtros_group = QGroupBox()
        filtros_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #495057;
                border: 2px solid #dee2e6;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                background-color: #f8f9fa;
                border-radius: 5px;
            }
        """)
        filtros_group.setTitle("🔍 Filtros")
        filtros_layout = QGridLayout(filtros_group)
        filtros_layout.setSpacing(10)  # Aumentar espaçamento entre filtros
        filtros_layout.setVerticalSpacing(12)  # Espaçamento vertical maior entre linhas
        filtros_layout.setHorizontalSpacing(8)  # Espaçamento horizontal entre colunas
        
        # Configurar responsividade das colunas
        filtros_layout.setColumnStretch(1, 1)  # Coluna dos campos de input se expandem
        filtros_layout.setColumnStretch(3, 1)  # Coluna dos combobox se expandem
        
        # Organizar em 2x2 conforme a imagem
        # Posição 1: Busca (CEP)
        self.busca_edit = QLineEdit()
        self.busca_edit.setPlaceholderText("Buscar por CEP...")
        self.busca_edit.setMinimumWidth(80)  # Largura mínima, mas responsiva
        self.busca_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8fffe;
            }
        """)
        busca_label = QLabel("Busca:")
        busca_label.setStyleSheet("QLabel { font-weight: bold; color: #495057; }")
        filtros_layout.addWidget(busca_label, 0, 0)
        filtros_layout.addWidget(self.busca_edit, 0, 1)
        
        # Posição 2: Região
        self.regiao_combo = QComboBox()
        self.regiao_combo.addItem("Todas as regiões")
        regioes = ["Norte", "Sul", "Leste", "Oeste", "Central"]
        self.regiao_combo.addItems(regioes)
        self.regiao_combo.setMinimumWidth(90)  # Largura mínima, mas responsiva
        self.regiao_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                font-size: 12px;
                min-height: 20px;
                color: #495057;
            }
            QComboBox:focus {
                border-color: #27ae60;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #495057;
                border-radius: 2px;
                background-color: #495057;
                width: 6px;
                height: 6px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
                padding: 4px;
            }
            QComboBox QAbstractItemView::item {
                height: 25px;
                padding: 4px 8px;
                border-radius: 3px;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
        """)
        regiao_label = QLabel("Região:")
        regiao_label.setStyleSheet("QLabel { font-weight: bold; color: #495057; }")
        filtros_layout.addWidget(regiao_label, 0, 2)
        filtros_layout.addWidget(self.regiao_combo, 0, 3)
        
        # Posição 3: Busca Cidade
        self.busca_cidade_edit = QLineEdit()
        self.busca_cidade_edit.setPlaceholderText("Buscar cidade...")
        self.busca_cidade_edit.setMinimumWidth(80)  # Largura mínima, mas responsiva
        self.busca_cidade_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8fffe;
            }
        """)
        busca_cidade_label = QLabel("Busca Cidade:")
        busca_cidade_label.setStyleSheet("QLabel { font-weight: bold; color: #495057; }")
        filtros_layout.addWidget(busca_cidade_label, 1, 0)
        filtros_layout.addWidget(self.busca_cidade_edit, 1, 1)
        
        # Posição 4: Cidade
        self.cidade_combo = QComboBox()
        self.cidade_combo.addItem("Todas as cidades")
        self.cidade_combo.setMaximumHeight(100)
        self.cidade_combo.setMinimumWidth(100)  # Largura mínima, mas responsiva
        self.cidade_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                font-size: 12px;
                min-height: 20px;
                color: #495057;
            }
            QComboBox:focus {
                border-color: #27ae60;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #495057;
                border-radius: 2px;
                background-color: #495057;
                width: 6px;
                height: 6px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
                selection-background-color: #e8f5e8;
                selection-color: #2e7d32;
                padding: 4px;
            }
            QComboBox QAbstractItemView::item {
                height: 25px;
                padding: 4px 8px;
                border-radius: 3px;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e8f5e8;
                color: #2e7d32;
            }
        """)
        cidade_label = QLabel("Cidade:")
        cidade_label.setStyleSheet("QLabel { font-weight: bold; color: #495057; }")
        filtros_layout.addWidget(cidade_label, 1, 2)
        filtros_layout.addWidget(self.cidade_combo, 1, 3)
        
        # Status removido
        
        # Todos os filtros numéricos e padrão removidos
        
        layout.addWidget(filtros_group)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        
        # Botão de busca online
        self.btn_busca_online = QPushButton("🔍 Busca Online")
        self.btn_busca_online.setMinimumWidth(80)  # Largura mínima, mas responsivo
        self.btn_busca_online.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #3498db);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #21618c, stop:1 #2980b9);
            }
        """)
        self.btn_busca_online.clicked.connect(self.buscar_online)
        buttons_layout.addWidget(self.btn_busca_online)
        
        self.btn_aplicar = QPushButton("✅ Aplicar Filtros")
        self.btn_aplicar.setMinimumWidth(80)  # Largura mínima, mas responsivo
        self.btn_aplicar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #2ecc71);
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e8449, stop:1 #27ae60);
            }
        """)
        buttons_layout.addWidget(self.btn_aplicar)
        
        self.btn_limpar = QPushButton("🧹 Limpar Filtros")
        self.btn_limpar.setMinimumWidth(80)  # Largura mínima, mas responsivo
        self.btn_limpar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f39c12, stop:1 #e67e22);
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e67e22, stop:1 #f39c12);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d68910, stop:1 #e67e22);
            }
        """)
        buttons_layout.addWidget(self.btn_limpar)
        
        # Configurar responsividade dos botões
        buttons_layout.setStretchFactor(self.btn_busca_online, 1)
        buttons_layout.setStretchFactor(self.btn_aplicar, 1)
        buttons_layout.setStretchFactor(self.btn_limpar, 1)
        
        layout.addLayout(buttons_layout)
        
        # Configurar layout
        self.setLayout(layout)
        # Widget agora é totalmente responsivo - se adapta ao tamanho do painel esquerdo
        
        # Inicializar serviço de cidades
        self.inicializar_cidades()
        
    def inicializar_cidades(self):
        """Inicializa o serviço de cidades e sincroniza com dados online"""
        try:
            # Tentar sincronizar cidades (pode demorar na primeira vez)
            logging.info("Inicializando serviço de cidades...")
            
            # Em background, sincronizar cidades
            self.cidade_service.sincronizar_cidades()
            
            # Carregar cidades disponíveis
            self.regioes_disponiveis = self.cidade_service.get_regioes_disponiveis()
            self.todas_cidades_sc = self.cidade_service.get_todas_cidades()
            
            logging.info(f"Cidades carregadas: {len(self.todas_cidades_sc)} total, {len(self.regioes_disponiveis)} regiões")
            
        except Exception as e:
            logging.error(f"Erro ao inicializar cidades: {e}")
            # Fallback para lista básica
            self.regioes_disponiveis = ["Norte", "Sul", "Leste", "Oeste", "Central"]
            self.todas_cidades_sc = ["Florianópolis", "Joinville", "Blumenau", "Criciúma", "Chapecó", "Capinzal"]
        
    def setup_connections(self):
        """Configura as conexões dos controles"""
        # Filtros avançados removidos
        
        # Conectar botões
        self.btn_aplicar.clicked.connect(self.aplicar_filtros)
        self.btn_limpar.clicked.connect(self.limpar_filtros)
        
        # Conectar mudanças nos filtros para atualização automática
        self.busca_edit.textChanged.connect(self.on_filtro_changed)
        self.busca_cidade_edit.textChanged.connect(self.on_busca_cidade_changed)
        self.regiao_combo.currentTextChanged.connect(self.on_regiao_changed)
        self.cidade_combo.currentTextChanged.connect(self.on_filtro_changed)
        # Conexões de filtros removidos
        
    def on_regiao_changed(self, regiao):
        """Chamado quando a região é alterada"""
        try:
            # Filtrar cidades baseado na região selecionada
            if regiao == "Todas as regiões":
                cidades_filtradas = self.todas_cidades_sc
            else:
                cidades_por_regiao = self.cidade_service.get_cidades_por_regiao(regiao)
                cidades_filtradas = [cidade['nome'] for cidade in cidades_por_regiao]
            
            # Atualizar combo de cidades
            self.cidade_combo.clear()
            self.cidade_combo.addItem("Todas as cidades")
            self.cidade_combo.addItems(cidades_filtradas)
            
            # Resetar seleção de cidade
            self.cidade_combo.setCurrentIndex(0)
            
            # Emitir sinal de filtro alterado
            self.on_filtro_changed()
            
        except Exception as e:
            logging.error(f"Erro ao alterar região: {e}")
            # Fallback: mostrar todas as cidades
            self.cidade_combo.clear()
            self.cidade_combo.addItem("Todas as cidades")
            self.cidade_combo.addItems(self.todas_cidades_sc)
    
    def on_busca_cidade_changed(self, texto):
        """Chamado quando o texto de busca de cidade é alterado"""
        try:
            texto = texto.strip().lower()
            
            # Se não há texto, mostrar todas as cidades da região
            if not texto:
                self.on_regiao_changed(self.regiao_combo.currentText())
                return
            
            # Filtrar cidades baseado no texto de busca (case-insensitive)
            regiao_selecionada = self.regiao_combo.currentText()
            
            if regiao_selecionada == "Todas as regiões":
                cidades_base = self.todas_cidades_sc
            else:
                cidades_por_regiao = self.cidade_service.get_cidades_por_regiao(regiao_selecionada)
                cidades_base = [cidade['nome'] for cidade in cidades_por_regiao]
            
            # Filtrar cidades que contêm o texto de busca
            cidades_filtradas = [
                cidade for cidade in cidades_base 
                if texto in cidade.lower()
            ]
            
            # Atualizar combo de cidades
            self.cidade_combo.clear()
            self.cidade_combo.addItem("Todas as cidades")
            self.cidade_combo.addItems(cidades_filtradas)
            
        except Exception as e:
            logging.error(f"Erro na busca de cidade: {e}")
        
    # Método toggle_filtros_avancados removido junto com filtros avançados
        
    def load_cidades(self):
        """Carrega lista de cidades do banco"""
        try:
            # Usar todas as cidades de Santa Catarina do serviço
            self.cidade_combo.clear()
            self.cidade_combo.addItem("Todas as cidades")
            self.cidade_combo.addItems(self.todas_cidades_sc)
                
        except Exception as e:
            logging.error(f"Erro ao carregar cidades: {e}")
            # Fallback para lista básica
            self.cidade_combo.addItems(["Florianópolis", "Joinville", "Blumenau", "Criciúma", "Chapecó", "Capinzal"])
            
    def on_filtro_changed(self):
        """Chamado quando um filtro é alterado"""
        # Emitir sinal com filtros atuais
        filtros = self.get_filtros_atuais()
        self.filtros_alterados.emit(filtros)
        
    def get_filtros_atuais(self) -> dict:
        """Retorna os filtros atualmente aplicados"""
        filtros = {}
        
        # Busca por CEP
        if self.busca_edit.text().strip():
            filtros['cep'] = self.busca_edit.text().strip()
            
        # Região
        if self.regiao_combo.currentText() != "Todas as regiões":
            filtros['regiao'] = self.regiao_combo.currentText()
            
        # Cidade
        if self.cidade_combo.currentText() != "Todas as cidades":
            filtros['cidade'] = self.cidade_combo.currentText()
            
        # Status
        # Status removido
            
        # Filtros numéricos removidos
            
        # Filtros avançados removidos
                
        return filtros
        
    def aplicar_filtros(self):
        """Aplica os filtros selecionados"""
        filtros = self.get_filtros_atuais()
        self.filtros_alterados.emit(filtros)
        
    def limpar_filtros(self):
        """Limpa todos os filtros"""
        self.busca_edit.clear()
        self.busca_cidade_edit.clear()
        self.regiao_combo.setCurrentIndex(0)
        self.cidade_combo.setCurrentIndex(0)
        # Filtros removidos
        # Filtros avançados removidos
        self.load_cidades()
        self.on_filtro_changed()
