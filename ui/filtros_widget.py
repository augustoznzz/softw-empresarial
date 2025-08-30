#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget de filtros para a tabela de imóveis
"""

import logging
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QGroupBox, QLabel, QLineEdit, QComboBox, QSpinBox, 
                               QDoubleSpinBox, QCheckBox, QPushButton)
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont, QPalette, QColor
from models.database import DatabaseManager

class FiltrosWidget(QWidget):
    filtros_alterados = Signal(dict)
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        self.load_cidades()
        
    def setup_ui(self):
        """Configura a interface do widget de filtros"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Estilo moderno para o widget
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
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
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 8px;
                background-color: white;
                color: #495057;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border-color: #007bff;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6c757d;
                margin-right: 5px;
            }
            QCheckBox {
                color: #495057;
                font-weight: 500;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #007bff;
                border-color: #007bff;
            }
        """)
        
        # Grupo de filtros principais
        filtros_group = QGroupBox("🔍 Filtros de Busca")
        filtros_layout = QGridLayout()
        filtros_group.setLayout(filtros_layout)
        
        # Busca por texto
        self.busca_edit = QLineEdit()
        self.busca_edit.setPlaceholderText("Digite endereço, cidade ou características...")
        self.busca_edit.textChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("🔎 Busca:"), 0, 0)
        filtros_layout.addWidget(self.busca_edit, 0, 1, 1, 3)
        
        # Região
        self.regiao_combo = QComboBox()
        self.regiao_combo.addItems(["Todas as regiões", "Norte", "Sul", "Leste", "Oeste", "Central"])
        self.regiao_combo.currentTextChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("🗺️ Região:"), 1, 0)
        filtros_layout.addWidget(self.regiao_combo, 1, 1)
        
        # Cidade
        self.cidade_combo = QComboBox()
        self.cidade_combo.currentTextChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("🏙️ Cidade:"), 1, 2)
        filtros_layout.addWidget(self.cidade_combo, 1, 3)
        
        # Estado (fixo em SC)
        self.estado_combo = QComboBox()
        self.estado_combo.addItem("SC")
        self.estado_combo.setCurrentText("SC")
        self.estado_combo.setEnabled(False)
        filtros_layout.addWidget(QLabel("🏛️ Estado:"), 2, 0)
        filtros_layout.addWidget(self.estado_combo, 2, 1)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Todos os status", "Em análise", "Comprado", "Vendido"])
        self.status_combo.currentTextChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("📊 Status:"), 2, 2)
        filtros_layout.addWidget(self.status_combo, 2, 3)
        
        # Padrão de acabamento
        self.padrao_combo = QComboBox()
        self.padrao_combo.addItems(["Todos os padrões", "Baixo", "Médio", "Alto"])
        self.padrao_combo.currentTextChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("🏗️ Padrão:"), 3, 0)
        filtros_layout.addWidget(self.padrao_combo, 3, 1)
        
        # Metragem
        self.metragem_min_spin = QDoubleSpinBox()
        self.metragem_min_spin.setRange(0, 10000)
        self.metragem_min_spin.setSuffix(" m²")
        self.metragem_min_spin.setSpecialValueText("Min")
        self.metragem_min_spin.valueChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("📏 Metragem Min:"), 3, 2)
        filtros_layout.addWidget(self.metragem_min_spin, 3, 3)
        
        # Custo mínimo
        self.custo_min_spin = QDoubleSpinBox()
        self.custo_min_spin.setRange(0, 10000000)
        self.custo_min_spin.setPrefix("R$ ")
        self.custo_min_spin.setSpecialValueText("Min")
        self.custo_min_spin.valueChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("💰 Custo Min:"), 4, 0)
        filtros_layout.addWidget(self.custo_min_spin, 4, 1)
        
        self.custo_max_spin = QDoubleSpinBox()
        self.custo_max_spin.setRange(0, 10000000)
        self.custo_max_spin.setPrefix("R$ ")
        self.custo_max_spin.setSpecialValueText("Max")
        self.custo_max_spin.valueChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("💰 Custo Max:"), 4, 2)
        filtros_layout.addWidget(self.custo_max_spin, 4, 3)
        
        # ROI mínimo
        self.roi_min_spin = QDoubleSpinBox()
        self.roi_min_spin.setRange(-100, 1000)
        self.roi_min_spin.setValue(0)
        self.roi_min_spin.setSuffix(" %")
        self.roi_min_spin.valueChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("📈 ROI Mínimo:"), 5, 0)
        filtros_layout.addWidget(self.roi_min_spin, 5, 1)
        
        # Margem mínima
        self.margem_min_spin = QDoubleSpinBox()
        self.margem_min_spin.setRange(-1000000, 10000000)
        self.margem_min_spin.setValue(0)
        self.margem_min_spin.setPrefix("R$ ")
        self.margem_min_spin.valueChanged.connect(self.on_filtro_changed)
        filtros_layout.addWidget(QLabel("💵 Margem Mínima:"), 5, 2)
        filtros_layout.addWidget(self.margem_min_spin, 5, 3)
        
        # Filtros avançados
        self.filtros_avancados_check = QCheckBox("🔧 Filtros Avançados")
        self.filtros_avancados_check.setChecked(False)
        self.filtros_avancados_check.toggled.connect(self.toggle_filtros_avancados)
        filtros_layout.addWidget(self.filtros_avancados_check, 6, 0, 1, 2)
        
        # Filtros avançados (inicialmente ocultos)
        self.quartos_min_spin = QSpinBox()
        self.quartos_min_spin.setRange(0, 20)
        self.quartos_min_spin.setSpecialValueText("Min")
        self.quartos_min_spin.valueChanged.connect(self.on_filtro_changed)
        
        self.quartos_max_spin = QSpinBox()
        self.quartos_max_spin.setRange(0, 20)
        self.quartos_max_spin.setSpecialValueText("Max")
        self.quartos_max_spin.valueChanged.connect(self.on_filtro_changed)
        
        self.banheiros_min_spin = QSpinBox()
        self.banheiros_min_spin.setRange(0, 20)
        self.banheiros_min_spin.setSpecialValueText("Min")
        self.banheiros_min_spin.valueChanged.connect(self.on_filtro_changed)
        
        self.banheiros_max_spin = QSpinBox()
        self.banheiros_max_spin.setRange(0, 20)
        self.banheiros_max_spin.setSpecialValueText("Max")
        self.banheiros_max_spin.valueChanged.connect(self.on_filtro_changed)
        
        # Ano
        self.ano_min_spin = QSpinBox()
        self.ano_min_spin.setRange(1900, 2030)
        self.ano_min_spin.setValue(1900)
        self.ano_min_spin.setSpecialValueText("Min")
        self.ano_min_spin.valueChanged.connect(self.on_filtro_changed)
        
        self.ano_max_spin = QSpinBox()
        self.ano_max_spin.setRange(1900, 2030)
        self.ano_max_spin.setValue(2030)
        self.ano_max_spin.setSpecialValueText("Max")
        self.ano_max_spin.valueChanged.connect(self.on_filtro_changed)
        
        # Criar e armazenar referências aos labels dos filtros avançados
        self.quartos_label = QLabel("🛏️ Quartos:")
        self.banheiros_label = QLabel("🚿 Banheiros:")
        self.ano_label = QLabel("📅 Ano:")
        
        # Adicionar widgets dos filtros avançados ao layout
        filtros_layout.addWidget(self.quartos_label, 7, 0)
        filtros_layout.addWidget(self.quartos_min_spin, 7, 1)
        filtros_layout.addWidget(QLabel("🛏️ Quartos Max:"), 7, 2)
        filtros_layout.addWidget(self.quartos_max_spin, 7, 3)
        
        filtros_layout.addWidget(self.banheiros_label, 8, 0)
        filtros_layout.addWidget(self.banheiros_min_spin, 8, 1)
        filtros_layout.addWidget(QLabel("🚿 Banheiros Max:"), 8, 2)
        filtros_layout.addWidget(self.banheiros_max_spin, 8, 3)
        
        filtros_layout.addWidget(self.ano_label, 9, 0)
        filtros_layout.addWidget(self.ano_min_spin, 9, 1)
        filtros_layout.addWidget(QLabel("📅 Ano Max:"), 9, 2)
        filtros_layout.addWidget(self.ano_max_spin, 9, 3)
        
        # Ocultar filtros avançados inicialmente
        self.toggle_filtros_avancados(False)
        
        layout.addWidget(filtros_group)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        
        self.btn_aplicar = QPushButton("✅ Aplicar Filtros")
        self.btn_aplicar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #2ecc71);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #229954, stop:1 #27ae60);
            }
        """)
        self.btn_aplicar.clicked.connect(self.on_filtro_changed)
        buttons_layout.addWidget(self.btn_aplicar)
        
        self.btn_limpar = QPushButton("🧹 Limpar Filtros")
        self.btn_limpar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f39c12, stop:1 #e67e22);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e67e22, stop:1 #f39c12);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d68910, stop:1 #f39c12);
            }
        """)
        self.btn_limpar.clicked.connect(self.limpar_filtros)
        buttons_layout.addWidget(self.btn_limpar)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
    def toggle_filtros_avancados(self, show: bool):
        """Mostra/oculta filtros avançados"""
        # Quartos
        self.quartos_min_spin.setVisible(show)
        self.quartos_max_spin.setVisible(show)
        self.quartos_label.setVisible(show)
        
        # Banheiros
        self.banheiros_min_spin.setVisible(show)
        self.banheiros_max_spin.setVisible(show)
        self.banheiros_label.setVisible(show)
        
        # Ano
        self.ano_min_spin.setVisible(show)
        self.ano_max_spin.setVisible(show)
        self.ano_label.setVisible(show)
        
    def load_cidades(self):
        """Carrega lista de cidades do banco"""
        try:
            query = "SELECT DISTINCT cidade FROM imoveis ORDER BY cidade"
            results = self.db_manager.execute_query(query)
            
            self.cidade_combo.clear()
            self.cidade_combo.addItem("Todas as cidades")
            
            for row in results:
                self.cidade_combo.addItem(row[0])
                
        except Exception as e:
            logging.error(f"Erro ao carregar cidades: {e}")
            
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
            
        # Região
        if self.regiao_combo.currentText() != "Todas as regiões":
            filtros['regiao'] = self.regiao_combo.currentText()
            
        # Cidade
        if self.cidade_combo.currentText() != "Todas as cidades":
            filtros['cidade'] = self.cidade_combo.currentText()
            
        # Estado
        if self.estado_combo.currentText() != "SC": # Fixo em SC
            filtros['estado'] = self.estado_combo.currentText()
            
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
                
            if self.ano_min_spin.value() > 1900:
                filtros['ano_min'] = self.ano_min_spin.value()
            if self.ano_max_spin.value() < 2030:
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
        self.ano_min_spin.setValue(1900)
        self.ano_max_spin.setValue(2030)
        self.filtros_avancados_check.setChecked(False)
        
        # Emitir sinal com filtros limpos
        self.filtros_alterados.emit({})
