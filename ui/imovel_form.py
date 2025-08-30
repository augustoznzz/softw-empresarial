#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formulário de cadastro e edição de imóveis
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox,
                               QPushButton, QGroupBox, QMessageBox, QFormLayout)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from models.imovel import Imovel
from models.database import DatabaseManager
import logging

class ImovelForm(QWidget):
    imovel_salvo = Signal(Imovel)
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.imovel_atual = None
        self.modo_edicao = False
        
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """Inicializa a interface do formulário"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Cadastro de Imóvel")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Formulário
        form_group = QGroupBox("Dados do Imóvel")
        form_layout = QFormLayout(form_group)
        
        # Endereço
        self.endereco_edit = QLineEdit()
        self.endereco_edit.setPlaceholderText("Digite o endereço completo")
        form_layout.addRow("Endereço:", self.endereco_edit)
        
        # Cidade
        self.cidade_edit = QLineEdit()
        self.cidade_edit.setPlaceholderText("Digite a cidade")
        form_layout.addRow("Cidade:", self.cidade_edit)
        
        # Estado
        self.estado_combo = QComboBox()
        estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
                  "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
                  "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        self.estado_combo.addItems(estados)
        form_layout.addRow("Estado:", self.estado_combo)
        
        # CEP
        self.cep_edit = QLineEdit()
        self.cep_edit.setPlaceholderText("00000-000")
        self.cep_edit.setInputMask("00000-000")
        form_layout.addRow("CEP:", self.cep_edit)
        
        # Coordenadas
        coords_layout = QHBoxLayout()
        self.lat_edit = QDoubleSpinBox()
        self.lat_edit.setRange(-90, 90)
        self.lat_edit.setDecimals(6)
        self.lat_edit.setSuffix("°")
        coords_layout.addWidget(QLabel("Lat:"))
        coords_layout.addWidget(self.lat_edit)
        
        self.lon_edit = QDoubleSpinBox()
        self.lon_edit.setRange(-180, 180)
        self.lon_edit.setDecimals(6)
        self.lon_edit.setSuffix("°")
        coords_layout.addWidget(QLabel("Lon:"))
        coords_layout.addWidget(self.lon_edit)
        
        form_layout.addRow("Coordenadas:", coords_layout)
        
        # Características físicas
        self.metragem_spin = QDoubleSpinBox()
        self.metragem_spin.setRange(1, 10000)
        self.metragem_spin.setSuffix(" m²")
        form_layout.addRow("Metragem:", self.metragem_spin)
        
        self.quartos_spin = QSpinBox()
        self.quartos_spin.setRange(0, 20)
        form_layout.addRow("Quartos:", self.quartos_spin)
        
        self.banheiros_spin = QSpinBox()
        self.banheiros_spin.setRange(0, 20)
        form_layout.addRow("Banheiros:", self.banheiros_spin)
        
        self.ano_spin = QSpinBox()
        self.ano_spin.setRange(1900, 2030)
        self.ano_spin.setValue(2020)
        form_layout.addRow("Ano:", self.ano_spin)
        
        # Padrão de acabamento
        self.padrao_combo = QComboBox()
        self.padrao_combo.addItems(["baixo", "medio", "alto"])
        form_layout.addRow("Padrão:", self.padrao_combo)
        
        # Custos
        self.custo_aquisicao_spin = QDoubleSpinBox()
        self.custo_aquisicao_spin.setRange(0, 10000000)
        self.custo_aquisicao_spin.setPrefix("R$ ")
        self.custo_aquisicao_spin.setDecimals(2)
        form_layout.addRow("Custo Aquisição:", self.custo_aquisicao_spin)
        
        self.custos_reforma_spin = QDoubleSpinBox()
        self.custos_reforma_spin.setRange(0, 10000000)
        self.custos_reforma_spin.setPrefix("R$ ")
        self.custos_reforma_spin.setDecimals(2)
        form_layout.addRow("Custos Reforma:", self.custos_reforma_spin)
        
        self.custos_transacao_spin = QDoubleSpinBox()
        self.custos_transacao_spin.setRange(0, 1000000)
        self.custos_transacao_spin.setPrefix("R$ ")
        self.custos_transacao_spin.setDecimals(2)
        form_layout.addRow("Custos Transação:", self.custos_transacao_spin)
        
        # Percentual lucro credor
        self.lucro_credor_spin = QDoubleSpinBox()
        self.lucro_credor_spin.setRange(0, 100)
        self.lucro_credor_spin.setValue(10)
        self.lucro_credor_spin.setSuffix(" %")
        form_layout.addRow("Lucro Credor (%):", self.lucro_credor_spin)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["em_analise", "comprado", "vendido"])
        form_layout.addRow("Status:", self.status_combo)
        
        layout.addWidget(form_group)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        self.btn_novo = QPushButton("🆕 Novo")
        self.btn_novo.setStyleSheet("""
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
        buttons_layout.addWidget(self.btn_novo)
        
        self.btn_salvar = QPushButton("💾 Salvar")
        self.btn_salvar.setStyleSheet("""
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
        buttons_layout.addWidget(self.btn_salvar)
        
        self.btn_cancelar = QPushButton("❌ Cancelar")
        self.btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        buttons_layout.addWidget(self.btn_cancelar)
        
        layout.addLayout(buttons_layout)
        
        # Configurar layout
        self.setLayout(layout)
        self.setMaximumWidth(400)
        
    def setup_connections(self):
        """Configura as conexões dos botões"""
        self.btn_novo.clicked.connect(self.novo_imovel)
        self.btn_salvar.clicked.connect(self.salvar_imovel)
        self.btn_cancelar.clicked.connect(self.cancelar_edicao)
        
    def novo_imovel(self):
        """Prepara o formulário para um novo imóvel"""
        self.limpar_formulario()
        self.modo_edicao = False
        self.imovel_atual = None
        self.btn_novo.setEnabled(False)
        self.btn_salvar.setEnabled(True)
        self.btn_cancelar.setEnabled(True)
        
    def limpar_formulario(self):
        """Limpa todos os campos do formulário"""
        self.endereco_edit.clear()
        self.cidade_edit.clear()
        self.estado_combo.setCurrentIndex(0)
        self.cep_edit.clear()
        self.lat_edit.setValue(0)
        self.lon_edit.setValue(0)
        self.metragem_spin.setValue(0)
        self.quartos_spin.setValue(0)
        self.banheiros_spin.setValue(0)
        self.ano_spin.setValue(2020)
        self.padrao_combo.setCurrentIndex(1)  # médio
        self.custo_aquisicao_spin.setValue(0)
        self.custos_reforma_spin.setValue(0)
        self.custos_transacao_spin.setValue(0)
        self.lucro_credor_spin.setValue(10)
        self.status_combo.setCurrentIndex(0)  # em análise
        
    def load_imovel(self, imovel: Imovel):
        """Carrega um imóvel no formulário para edição"""
        if not imovel:
            return
            
        self.imovel_atual = imovel
        self.modo_edicao = True
        
        # Preencher campos
        self.endereco_edit.setText(imovel.endereco)
        self.cidade_edit.setText(imovel.cidade)
        
        # Encontrar índice do estado
        estado_index = self.estado_combo.findText(imovel.estado)
        if estado_index >= 0:
            self.estado_combo.setCurrentIndex(estado_index)
            
        self.cep_edit.setText(imovel.cep or "")
        self.lat_edit.setValue(imovel.latitude or 0)
        self.lon_edit.setValue(imovel.longitude or 0)
        self.metragem_spin.setValue(imovel.metragem)
        self.quartos_spin.setValue(imovel.quartos or 0)
        self.banheiros_spin.setValue(imovel.banheiros or 0)
        self.ano_spin.setValue(imovel.ano or 2020)
        
        # Encontrar índice do padrão
        padrao_index = self.padrao_combo.findText(imovel.padrao_acabamento)
        if padrao_index >= 0:
            self.padrao_combo.setCurrentIndex(padrao_index)
            
        self.custo_aquisicao_spin.setValue(imovel.custo_aquisicao or 0)
        self.custos_reforma_spin.setValue(imovel.custos_reforma or 0)
        self.custos_transacao_spin.setValue(imovel.custos_transacao or 0)
        self.lucro_credor_spin.setValue(imovel.percentual_lucro_credor or 10)
        
        # Encontrar índice do status
        status_index = self.status_combo.findText(imovel.status)
        if status_index >= 0:
            self.status_combo.setCurrentIndex(status_index)
            
        # Configurar botões
        self.btn_novo.setEnabled(True)
        self.btn_salvar.setEnabled(True)
        self.btn_cancelar.setEnabled(True)
        
    def salvar_imovel(self):
        """Salva o imóvel no banco de dados"""
        try:
            # Validar campos obrigatórios
            if not self.endereco_edit.text().strip():
                QMessageBox.warning(self, "Validação", "Endereço é obrigatório")
                return
                
            if not self.cidade_edit.text().strip():
                QMessageBox.warning(self, "Validação", "Cidade é obrigatória")
                return
                
            if self.metragem_spin.value() <= 0:
                QMessageBox.warning(self, "Validação", "Metragem deve ser maior que zero")
                return
                
            if self.custo_aquisicao_spin.value() <= 0:
                QMessageBox.warning(self, "Validação", "Custo de aquisição deve ser maior que zero")
                return
                
            # Criar objeto imóvel
            dados_imovel = {
                'endereco': self.endereco_edit.text().strip(),
                'cidade': self.cidade_edit.text().strip(),
                'estado': self.estado_combo.currentText(),
                'cep': self.cep_edit.text().strip() or None,
                'latitude': self.lat_edit.value() if self.lat_edit.value() != 0 else None,
                'longitude': self.lon_edit.value() if self.lon_edit.value() != 0 else None,
                'metragem': self.metragem_spin.value(),
                'quartos': self.quartos_spin.value() if self.quartos_spin.value() > 0 else None,
                'banheiros': self.banheiros_spin.value() if self.banheiros_spin.value() > 0 else None,
                'ano': self.ano_spin.value() if self.ano_spin.value() > 1900 else None,
                'padrao_acabamento': self.padrao_combo.currentText(),
                'custo_aquisicao': self.custo_aquisicao_spin.value(),
                'custos_reforma': self.custos_reforma_spin.value(),
                'custos_transacao': self.custos_transacao_spin.value(),
                'percentual_lucro_credor': self.lucro_credor_spin.value(),
                'status': self.status_combo.currentText()
            }
            
            if self.modo_edicao and self.imovel_atual:
                # Atualizar imóvel existente
                dados_imovel['id'] = self.imovel_atual.id
                query = """
                    UPDATE imoveis SET
                        endereco = ?, cidade = ?, estado = ?, cep = ?, latitude = ?, longitude = ?,
                        metragem = ?, quartos = ?, banheiros = ?, ano = ?, padrao_acabamento = ?,
                        custo_aquisicao = ?, custos_reforma = ?, custos_transacao = ?,
                        percentual_lucro_credor = ?, status = ?, data_atualizacao = CURRENT_TIMESTAMP
                    WHERE id = ?
                """
                params = (
                    dados_imovel['endereco'], dados_imovel['cidade'], dados_imovel['estado'],
                    dados_imovel['cep'], dados_imovel['latitude'], dados_imovel['longitude'],
                    dados_imovel['metragem'], dados_imovel['quartos'], dados_imovel['banheiros'],
                    dados_imovel['ano'], dados_imovel['padrao_acabamento'],
                    dados_imovel['custo_aquisicao'], dados_imovel['custos_reforma'],
                    dados_imovel['custos_transacao'], dados_imovel['percentual_lucro_credor'],
                    dados_imovel['status'], dados_imovel['id']
                )
                
                self.db_manager.execute_query(query, params)
                QMessageBox.information(self, "Sucesso", "Imóvel atualizado com sucesso!")
                
            else:
                # Inserir novo imóvel
                query = """
                    INSERT INTO imoveis (
                        endereco, cidade, estado, cep, latitude, longitude,
                        metragem, quartos, banheiros, ano, padrao_acabamento,
                        custo_aquisicao, custos_reforma, custos_transacao,
                        percentual_lucro_credor, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    dados_imovel['endereco'], dados_imovel['cidade'], dados_imovel['estado'],
                    dados_imovel['cep'], dados_imovel['latitude'], dados_imovel['longitude'],
                    dados_imovel['metragem'], dados_imovel['quartos'], dados_imovel['banheiros'],
                    dados_imovel['ano'], dados_imovel['padrao_acabamento'],
                    dados_imovel['custo_aquisicao'], dados_imovel['custos_reforma'],
                    dados_imovel['custos_transacao'], dados_imovel['percentual_lucro_credor'],
                    dados_imovel['status']
                )
                
                self.db_manager.execute_query(query, params)
                QMessageBox.information(self, "Sucesso", "Imóvel cadastrado com sucesso!")
                
            # Emitir sinal
            novo_imovel = Imovel(**dados_imovel)
            self.imovel_salvo.emit(novo_imovel)
            
            # Limpar formulário
            self.limpar_formulario()
            self.btn_novo.setEnabled(True)
            self.btn_salvar.setEnabled(False)
            self.btn_cancelar.setEnabled(False)
            
        except Exception as e:
            logging.error(f"Erro ao salvar imóvel: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao salvar imóvel: {str(e)}")
            
    def cancelar_edicao(self):
        """Cancela a edição e limpa o formulário"""
        self.limpar_formulario()
        self.btn_novo.setEnabled(True)
        self.btn_salvar.setEnabled(False)
        self.btn_cancelar.setEnabled(False)
        self.modo_edicao = False
        self.imovel_atual = None
