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
        """Simula uma busca online por imóveis nas cidades selecionadas"""
        regiao_selecionada = self.regiao_combo.currentText()
        cidade_selecionada = self.cidade_combo.currentText()
        
        if regiao_selecionada == "Todas as regiões" and cidade_selecionada == "Todas as cidades":
            QMessageBox.information(self, "Busca Online", 
                                  "Selecione uma região ou cidade específica para realizar a busca online.")
            return
        
        try:
            # Buscar cidades baseado na seleção
            cidades_busca = []
            if regiao_selecionada != "Todas as regiões":
                cidades_por_regiao = self.cidade_service.get_cidades_por_regiao(regiao_selecionada)
                cidades_busca = [cidade['nome'] for cidade in cidades_por_regiao]
            elif cidade_selecionada != "Todas as cidades":
                cidades_busca = [cidade_selecionada]
            
            if cidades_busca:
                # Simular carregamento de dados online
                QMessageBox.information(self, "Busca Online", 
                                      f"Buscando imóveis online em: {', '.join(cidades_busca[:5])}{'...' if len(cidades_busca) > 5 else ''}\n\n"
                                      f"Total de cidades na busca: {len(cidades_busca)}\n\n"
                                      "Esta funcionalidade simula uma busca online real.\n"
                                      "Em uma implementação real, aqui seria feita uma API call\n"
                                      "para portais de imóveis como Zap Imóveis, Viva Real, etc.")
                
                # Emitir sinal para atualizar a tabela com os resultados da busca
                self.filtros_alterados.emit({})
            else:
                QMessageBox.warning(self, "Busca Online", 
                                  "Nenhuma cidade encontrada para a busca selecionada.")
                                  
        except Exception as e:
            logging.error(f"Erro na busca online: {e}")
            QMessageBox.warning(self, "Busca Online", 
                              f"Erro ao realizar busca: {str(e)}")
        
    def init_ui(self):
        """Inicializa a interface dos filtros"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("🔍 Filtros e Busca")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Grupo de filtros - Layout mais compacto
        filtros_group = QGroupBox("Filtros")
        filtros_layout = QGridLayout(filtros_group)
        filtros_layout.setSpacing(4)  # Reduzir espaçamento
        
        # Busca por texto
        self.busca_edit = QLineEdit()
        self.busca_edit.setPlaceholderText("Buscar endereço...")
        filtros_layout.addWidget(QLabel("Busca:"), 0, 0)
        filtros_layout.addWidget(self.busca_edit, 0, 1)
        
        # Região
        self.regiao_combo = QComboBox()
        self.regiao_combo.addItem("Todas as regiões")
        regioes = ["Norte", "Sul", "Leste", "Oeste", "Central"]
        self.regiao_combo.addItems(regioes)
        filtros_layout.addWidget(QLabel("Região:"), 1, 0)
        filtros_layout.addWidget(self.regiao_combo, 1, 1)
        
        # Busca de cidade com campo de pesquisa
        cidade_container = QVBoxLayout()
        self.busca_cidade_edit = QLineEdit()
        self.busca_cidade_edit.setPlaceholderText("Buscar cidade...")
        self.cidade_combo = QComboBox()
        self.cidade_combo.setMaximumHeight(80)  # Reduzir altura em 30%
        self.cidade_combo.addItem("Todas as cidades")
        cidade_container.addWidget(self.busca_cidade_edit)
        cidade_container.addWidget(self.cidade_combo)
        
        cidade_widget = QWidget()
        cidade_widget.setLayout(cidade_container)
        filtros_layout.addWidget(QLabel("Cidade:"), 2, 0)
        filtros_layout.addWidget(cidade_widget, 2, 1)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItem("Todos os status")
        self.status_combo.addItems(["em_analise", "comprado", "vendido"])
        filtros_layout.addWidget(QLabel("Status:"), 3, 0)
        filtros_layout.addWidget(self.status_combo, 3, 1)
        
        # Padrão de acabamento
        self.padrao_combo = QComboBox()
        self.padrao_combo.addItem("Todos os padrões")
        self.padrao_combo.addItems(["baixo", "medio", "alto"])
        filtros_layout.addWidget(QLabel("Padrão:"), 4, 0)
        filtros_layout.addWidget(self.padrao_combo, 4, 1)
        
        # Filtros numéricos
        self.metragem_min_spin = QDoubleSpinBox()
        self.metragem_min_spin.setRange(0, 10000)
        self.metragem_min_spin.setSuffix(" m²")
        self.metragem_min_spin.setSpecialValueText("Min")
        filtros_layout.addWidget(QLabel("Metragem:"), 3, 2)
        filtros_layout.addWidget(self.metragem_min_spin, 3, 3)
        
        self.metragem_max_spin = QDoubleSpinBox()
        self.metragem_max_spin.setRange(0, 10000)
        self.metragem_max_spin.setSuffix(" m²")
        self.metragem_max_spin.setSpecialValueText("Max")
        filtros_layout.addWidget(QLabel("Metragem Max:"), 4, 0)
        filtros_layout.addWidget(self.metragem_max_spin, 4, 1)
        
        # Filtros financeiros
        self.custo_min_spin = QDoubleSpinBox()
        self.custo_min_spin.setRange(0, 10000000)
        self.custo_min_spin.setPrefix("R$ ")
        self.custo_min_spin.setSpecialValueText("Min")
        filtros_layout.addWidget(QLabel("Custo Total:"), 4, 2)
        filtros_layout.addWidget(self.custo_min_spin, 4, 3)
        
        self.custo_max_spin = QDoubleSpinBox()
        self.custo_max_spin.setRange(0, 10000000)
        self.custo_max_spin.setPrefix("R$ ")
        self.custo_max_spin.setSpecialValueText("Max")
        filtros_layout.addWidget(QLabel("Custo Max:"), 5, 0)
        filtros_layout.addWidget(self.custo_max_spin, 5, 1)
        
        # ROI mínimo
        self.roi_min_spin = QDoubleSpinBox()
        self.roi_min_spin.setRange(-100, 1000)
        self.roi_min_spin.setValue(0)
        self.roi_min_spin.setSuffix(" %")
        filtros_layout.addWidget(QLabel("ROI Mínimo:"), 5, 2)
        filtros_layout.addWidget(self.roi_min_spin, 5, 3)
        
        # Margem mínima
        self.margem_min_spin = QDoubleSpinBox()
        self.margem_min_spin.setRange(-1000000, 10000000)
        self.margem_min_spin.setValue(0)
        self.margem_min_spin.setPrefix("R$ ")
        filtros_layout.addWidget(QLabel("Margem Mínima:"), 6, 0)
        filtros_layout.addWidget(self.margem_min_spin, 6, 1)
        
        # Filtros avançados
        self.filtros_avancados_check = QCheckBox("Filtros Avançados")
        self.filtros_avancados_check.setChecked(False)
        filtros_layout.addWidget(self.filtros_avancados_check, 6, 2, 1, 2)
        
        # Filtros avançados (inicialmente ocultos)
        self.quartos_min_spin = QSpinBox()
        self.quartos_min_spin.setRange(0, 20)
        self.quartos_min_spin.setSpecialValueText("Min")
        filtros_layout.addWidget(QLabel("Quartos:"), 7, 0)
        filtros_layout.addWidget(self.quartos_min_spin, 7, 1)
        
        self.quartos_max_spin = QSpinBox()
        self.quartos_max_spin.setRange(0, 20)
        self.quartos_max_spin.setSpecialValueText("Max")
        filtros_layout.addWidget(QLabel("Quartos Max:"), 7, 2)
        filtros_layout.addWidget(self.quartos_max_spin, 7, 3)
        
        self.banheiros_min_spin = QSpinBox()
        self.banheiros_min_spin.setRange(0, 20)
        self.banheiros_min_spin.setSpecialValueText("Min")
        filtros_layout.addWidget(QLabel("Banheiros:"), 8, 0)
        filtros_layout.addWidget(self.banheiros_min_spin, 8, 1)
        
        self.banheiros_max_spin = QSpinBox()
        self.banheiros_max_spin.setRange(0, 20)
        self.banheiros_max_spin.setSpecialValueText("Max")
        filtros_layout.addWidget(QLabel("Banheiros Max:"), 8, 2)
        filtros_layout.addWidget(self.banheiros_max_spin, 8, 3)
        
        # Ano
        self.ano_min_spin = QSpinBox()
        self.ano_min_spin.setRange(1900, 2030)
        self.ano_min_spin.setValue(1900)
        self.ano_min_spin.setSpecialValueText("Min")
        filtros_layout.addWidget(QLabel("Ano:"), 9, 0)
        filtros_layout.addWidget(self.ano_min_spin, 9, 1)
        
        self.ano_max_spin = QSpinBox()
        self.ano_max_spin.setRange(1900, 2030)
        self.ano_max_spin.setValue(2030)
        self.ano_max_spin.setSpecialValueText("Max")
        filtros_layout.addWidget(QLabel("Ano Max:"), 9, 2)
        filtros_layout.addWidget(self.ano_max_spin, 9, 3)
        
        # Ocultar filtros avançados inicialmente
        self.toggle_filtros_avancados(False)
        
        layout.addWidget(filtros_group)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        
        # Botão de busca online
        self.btn_busca_online = QPushButton("🔍 Busca Online")
        self.btn_busca_online.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.btn_busca_online.clicked.connect(self.buscar_online)
        buttons_layout.addWidget(self.btn_busca_online)
        
        self.btn_aplicar = QPushButton("✅ Aplicar Filtros")
        self.btn_aplicar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        buttons_layout.addWidget(self.btn_aplicar)
        
        self.btn_limpar = QPushButton("🧹 Limpar Filtros")
        self.btn_limpar.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        buttons_layout.addWidget(self.btn_limpar)
        
        layout.addLayout(buttons_layout)
        
        # Configurar layout
        self.setLayout(layout)
        self.setMaximumWidth(250)  # Reduzir em 50% (de 500 para 250)
        
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
        self.filtros_avancados_check.toggled.connect(self.toggle_filtros_avancados)
        
        # Conectar botões
        self.btn_aplicar.clicked.connect(self.aplicar_filtros)
        self.btn_limpar.clicked.connect(self.limpar_filtros)
        
        # Conectar mudanças nos filtros para atualização automática
        self.busca_edit.textChanged.connect(self.on_filtro_changed)
        self.estado_combo.currentTextChanged.connect(self.on_filtro_changed)
        self.regiao_combo.currentTextChanged.connect(self.on_regiao_changed)
        self.cidade_combo.currentTextChanged.connect(self.on_filtro_changed)
        self.status_combo.currentTextChanged.connect(self.on_filtro_changed)
        self.padrao_combo.currentTextChanged.connect(self.on_filtro_changed)
        
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
        
    def toggle_filtros_avancados(self, show: bool):
        """Mostra/oculta filtros avançados"""
        # Quartos
        self.quartos_min_spin.setVisible(show)
        self.quartos_max_spin.setVisible(show)
        
        # Banheiros
        self.banheiros_min_spin.setVisible(show)
        self.banheiros_max_spin.setVisible(show)
        
        # Ano
        self.ano_min_spin.setVisible(show)
        self.ano_max_spin.setVisible(show)
        
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
        
        # Busca por texto
        if self.busca_edit.text().strip():
            filtros['busca'] = self.busca_edit.text().strip()
            
        # Estado
        if self.estado_combo.currentText() != "SC":
            filtros['estado'] = self.estado_combo.currentText()
            
        # Região
        if self.regiao_combo.currentText() != "Todas as regiões":
            filtros['regiao'] = self.regiao_combo.currentText()
            
        # Cidade
        if self.cidade_combo.currentText() != "Todas as cidades":
            filtros['cidade'] = self.cidade_combo.currentText()
            
        # Status
        if self.status_combo.currentText() != "Todos os status":
            filtros['status'] = self.status_combo.currentText()
            
        # Padrão
        if self.padrao_combo.currentText() != "Todos os padrões":
            filtros['padrao'] = self.padrao_combo.currentText()
            
        # Metragem
        if self.metragem_min_spin.value() > 0:
            filtros['metragem_min'] = self.metragem_min_spin.value()
        if self.metragem_max_spin.value() > 0:
            filtros['metragem_max'] = self.metragem_max_spin.value()
            
        # Custo
        if self.custo_min_spin.value() > 0:
            filtros['custo_min'] = self.custo_min_spin.value()
        if self.custo_max_spin.value() > 0:
            filtros['custo_max'] = self.custo_max_spin.value()
            
        # ROI
        if self.roi_min_spin.value() > 0:
            filtros['roi_min'] = self.roi_min_spin.value()
            
        # Margem
        if self.margem_min_spin.value() > 0:
            filtros['margem_min'] = self.margem_min_spin.value()
            
        # Filtros avançados
        if self.filtros_avancados_check.isChecked():
            if self.quartos_min_spin.value() > 0:
                filtros['quartos_min'] = self.quartos_min_spin.value()
            if self.quartos_max_spin.value() > 0:
                filtros['quartos_max'] = self.quartos_max_spin.value()
                
            if self.banheiros_min_spin.value() > 0:
                filtros['banheiros_min'] = self.banheiros_min_spin.value()
            if self.banheiros_max_spin.value() > 0:
                filtros['banheiros_max'] = self.banheiros_max_spin.value()
                
            if self.ano_min_spin.value() > 0:
                filtros['ano_min'] = self.ano_min_spin.value()
            if self.ano_max_spin.value() > 0:
                filtros['ano_max'] = self.ano_max_spin.value()
                
        return filtros
        
    def aplicar_filtros(self):
        """Aplica os filtros selecionados"""
        filtros = self.get_filtros_atuais()
        self.filtros_alterados.emit(filtros)
        
    def limpar_filtros(self):
        """Limpa todos os filtros"""
        self.busca_edit.clear()
        self.regiao_combo.setCurrentIndex(0)
        self.cidade_combo.setCurrentIndex(0)
        self.estado_combo.setCurrentIndex(0)
        self.status_combo.setCurrentIndex(0)
        self.padrao_combo.setCurrentIndex(0)
        self.metragem_min_spin.setValue(0)
        self.metragem_max_spin.setValue(0)
        self.custo_min_spin.setValue(0)
        self.custo_max_spin.setValue(0)
        self.roi_min_spin.setValue(0)
        self.margem_min_spin.setValue(0)
        self.quartos_min_spin.setValue(0)
        self.quartos_max_spin.setValue(0)
        self.banheiros_min_spin.setValue(0)
        self.banheiros_max_spin.setValue(0)
        self.ano_min_spin.setValue(0)
        self.ano_max_spin.setValue(0)
        self.filtros_avancados_check.setChecked(False)
        self.load_cidades()
        self.on_filtro_changed()
