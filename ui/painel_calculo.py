#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Painel de cálculos com sliders para ajustar percentuais
"""

import logging
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QGroupBox, QLabel, QSlider, QFrame, QScrollArea)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QColor, QPalette

from models.imovel import Imovel
from services.calculo_service import CalculoService

class PainelCalculo(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.calculo_service = CalculoService()
        self.imovel_atual = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do painel de cálculos"""
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
            QSlider::groove:horizontal {
                border: 1px solid #dee2e6;
                height: 8px;
                background: #f8f9fa;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                border: 2px solid #ffffff;
                width: 18px;
                height: 18px;
                border-radius: 9px;
                margin: -5px 0;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0056b3, stop:1 #004085);
            }
            QFrame {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: #f8f9fa;
            }
        """)
        
        # Título do painel
        title_label = QLabel("🧮 Painel de Cálculos")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #495057;
                text-align: center;
                padding: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Scroll area para o conteúdo
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Widget do conteúdo
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        
        # Grupo de informações do imóvel
        self.info_group = QGroupBox("🏠 Informações do Imóvel")
        info_layout = QGridLayout()
        self.info_group.setLayout(info_layout)
        
        # Labels de informação
        self.lbl_endereco = QLabel("Endereço: Nenhum imóvel selecionado")
        self.lbl_endereco.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #007bff;
                padding: 5px;
            }
        """)
        info_layout.addWidget(self.lbl_endereco, 0, 0, 1, 2)
        
        self.lbl_cidade_estado = QLabel("Cidade/Estado: -")
        self.lbl_cidade_estado.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #6c757d;
                padding: 5px;
            }
        """)
        info_layout.addWidget(self.lbl_cidade_estado, 1, 0, 1, 2)
        
        self.lbl_metragem = QLabel("Metragem: -")
        self.lbl_metragem.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #6c757d;
                padding: 5px;
            }
        """)
        info_layout.addWidget(self.lbl_metragem, 2, 0, 1, 2)
        
        content_layout.addWidget(self.info_group)
        
        # Grupo de parâmetros ajustáveis
        self.params_group = QGroupBox("⚙️ Parâmetros Ajustáveis")
        params_layout = QGridLayout()
        self.params_group.setLayout(params_layout)
        
        # Slider para percentual de lucro do credor
        self.lbl_lucro_credor = QLabel("Percentual de Lucro do Credor:")
        params_layout.addWidget(self.lbl_lucro_credor, 0, 0)
        
        self.lucro_credor_slider = QSlider(Qt.Horizontal)
        self.lucro_credor_slider.setRange(8, 25)
        self.lucro_credor_slider.setValue(15)
        self.lucro_credor_slider.setTickPosition(QSlider.TicksBelow)
        self.lucro_credor_slider.setTickInterval(1)
        self.lucro_credor_slider.valueChanged.connect(self.on_parametros_changed)
        params_layout.addWidget(self.lucro_credor_slider, 0, 1)
        
        self.lbl_lucro_credor_valor = QLabel("15%")
        self.lbl_lucro_credor_valor.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #007bff;
                min-width: 40px;
            }
        """)
        params_layout.addWidget(self.lbl_lucro_credor_valor, 0, 2)
        
        # Slider para lucro desejado do investidor
        self.lbl_lucro_investidor = QLabel("Lucro Desejado do Investidor:")
        params_layout.addWidget(self.lbl_lucro_investidor, 1, 0)
        
        self.lucro_investidor_slider = QSlider(Qt.Horizontal)
        self.lucro_investidor_slider.setRange(10, 25)
        self.lucro_investidor_slider.setValue(15)
        self.lucro_investidor_slider.setTickPosition(QSlider.TicksBelow)
        self.lucro_investidor_slider.setTickInterval(1)
        self.lucro_investidor_slider.valueChanged.connect(self.on_parametros_changed)
        params_layout.addWidget(self.lucro_investidor_slider, 1, 1)
        
        self.lbl_lucro_investidor_valor = QLabel("15%")
        self.lbl_lucro_investidor_valor.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #007bff;
                min-width: 40px;
            }
        """)
        params_layout.addWidget(self.lbl_lucro_investidor_valor, 1, 2)
        
        content_layout.addWidget(self.params_group)
        
        # Grupo de resultados dos cálculos
        self.resultados_group = QGroupBox("📊 Resultados dos Cálculos")
        resultados_layout = QGridLayout()
        self.resultados_group.setLayout(resultados_layout)
        
        # Custo total
        self.lbl_custo_total_titulo = QLabel("Custo Total:")
        self.lbl_custo_total_titulo.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #495057;
            }
        """)
        resultados_layout.addWidget(self.lbl_custo_total_titulo, 0, 0)
        
        self.lbl_custo_total_valor = QLabel("R$ 0,00")
        self.lbl_custo_total_valor.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #495057;
                padding: 5px;
                background-color: #f8f9fa;
                border-radius: 4px;
            }
        """)
        resultados_layout.addWidget(self.lbl_custo_total_valor, 0, 1)
        
        # Preço de venda estimado
        self.lbl_preco_estimado_titulo = QLabel("Preço de Venda Estimado:")
        self.lbl_preco_estimado_titulo.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #495057;
            }
        """)
        resultados_layout.addWidget(self.lbl_preco_estimado_titulo, 1, 0)
        
        self.lbl_preco_estimado_valor = QLabel("R$ 0,00")
        self.lbl_preco_estimado_valor.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #495057;
                padding: 5px;
                background-color: #f8f9fa;
                border-radius: 4px;
            }
        """)
        resultados_layout.addWidget(self.lbl_preco_estimado_valor, 1, 1)
        
        # Lucro do credor
        self.lbl_lucro_credor_calc_titulo = QLabel("Lucro do Credor:")
        self.lbl_lucro_credor_calc_titulo.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #495057;
            }
        """)
        resultados_layout.addWidget(self.lbl_lucro_credor_calc_titulo, 2, 0)
        
        self.lbl_lucro_credor_calc_valor = QLabel("R$ 0,00")
        self.lbl_lucro_credor_calc_valor.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #495057;
                padding: 5px;
                background-color: #f8f9fa;
                border-radius: 4px;
            }
        """)
        resultados_layout.addWidget(self.lbl_lucro_credor_calc_valor, 2, 1)
        
        # Lucro do investidor
        self.lbl_lucro_investidor_calc_titulo = QLabel("Lucro do Investidor:")
        self.lbl_lucro_investidor_calc_titulo.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #495057;
            }
        """)
        resultados_layout.addWidget(self.lbl_lucro_investidor_calc_titulo, 3, 0)
        
        self.lbl_lucro_investidor_calc_valor = QLabel("R$ 0,00")
        self.lbl_lucro_investidor_calc_valor.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #495057;
                padding: 5px;
                background-color: #f8f9fa;
                border-radius: 4px;
            }
        """)
        resultados_layout.addWidget(self.lbl_lucro_investidor_calc_valor, 3, 1)
        
        # Preço mínimo
        self.lbl_preco_minimo_titulo = QLabel("Preço Mínimo:")
        self.lbl_preco_minimo_titulo.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #495057;
            }
        """)
        resultados_layout.addWidget(self.lbl_preco_minimo_titulo, 4, 0)
        
        self.lbl_preco_minimo_valor = QLabel("R$ 0,00")
        self.lbl_preco_minimo_valor.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #495057;
                padding: 5px;
                background-color: #f8f9fa;
                border-radius: 4px;
            }
        """)
        resultados_layout.addWidget(self.lbl_preco_minimo_valor, 4, 1)
        
        content_layout.addWidget(self.resultados_group)
        
        # Grupo de indicadores financeiros
        self.indicadores_group = QGroupBox("📈 Indicadores Financeiros")
        indicadores_layout = QGridLayout()
        self.indicadores_group.setLayout(indicadores_layout)
        
        # Margem
        self.lbl_margem_titulo = QLabel("Margem:")
        self.lbl_margem_titulo.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #495057;
            }
        """)
        indicadores_layout.addWidget(self.lbl_margem_titulo, 0, 0)
        
        self.lbl_margem_valor = QLabel("R$ 0,00")
        self.lbl_margem_valor.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #495057;
                padding: 8px;
                border-radius: 6px;
                min-width: 120px;
            }
        """)
        indicadores_layout.addWidget(self.lbl_margem_valor, 0, 1)
        
        # ROI
        self.lbl_roi_titulo = QLabel("ROI (%):")
        self.lbl_roi_titulo.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #495057;
            }
        """)
        indicadores_layout.addWidget(self.lbl_roi_titulo, 1, 0)
        
        self.lbl_roi_valor = QLabel("0,0%")
        self.lbl_roi_valor.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #495057;
                padding: 8px;
                border-radius: 6px;
                min-width: 120px;
            }
        """)
        indicadores_layout.addWidget(self.lbl_roi_valor, 1, 1)
        
        # Payback estimado
        self.lbl_payback_titulo = QLabel("Payback Estimado:")
        self.lbl_payback_titulo.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #495057;
            }
        """)
        indicadores_layout.addWidget(self.lbl_payback_titulo, 2, 0)
        
        self.lbl_payback_valor = QLabel("0 meses")
        self.lbl_payback_valor.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #495057;
                padding: 5px;
                background-color: #f8f9fa;
                border-radius: 4px;
            }
        """)
        indicadores_layout.addWidget(self.lbl_payback_valor, 2, 1)
        
        content_layout.addWidget(self.indicadores_group)
        
        # Adicionar widget de conteúdo ao scroll area
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        
        # Conectar sliders aos labels de valor
        self.lucro_credor_slider.valueChanged.connect(self.atualizar_label_lucro_credor)
        self.lucro_investidor_slider.valueChanged.connect(self.atualizar_label_lucro_investidor)
        
    def atualizar_label_lucro_credor(self, valor):
        """Atualiza o label do valor do lucro do credor"""
        self.lbl_lucro_credor_valor.setText(f"{valor}%")
        self.on_parametros_changed()
        
    def atualizar_label_lucro_investidor(self, valor):
        """Atualiza o label do valor do lucro do investidor"""
        self.lbl_lucro_investidor_valor.setText(f"{valor}%")
        self.on_parametros_changed()
        
    def carregar_imovel(self, imovel):
        """Carrega um imóvel para exibição e cálculo"""
        self.imovel_atual = imovel
        self.atualizar_informacoes()
        self.calcular_e_exibir()
        
    def atualizar_informacoes(self):
        """Atualiza as informações básicas do imóvel"""
        if self.imovel_atual:
            self.lbl_endereco.setText(f"Endereço: {self.imovel_atual.endereco}")
            self.lbl_cidade_estado.setText(f"Cidade/Estado: {self.imovel_atual.cidade}/{self.imovel_atual.estado}")
            self.lbl_metragem.setText(f"Metragem: {self.imovel_atual.metragem:.1f} m²")
        else:
            self.lbl_endereco.setText("Endereço: Nenhum imóvel selecionado")
            self.lbl_cidade_estado.setText("Cidade/Estado: -")
            self.lbl_metragem.setText("Metragem: -")
            
    def calcular_e_exibir(self):
        """Calcula e exibe todos os valores"""
        if not self.imovel_atual:
            self.limpar_valores()
            return
            
        try:
            # Obter valores dos sliders
            percentual_lucro_credor = self.lucro_credor_slider.value() / 100
            lucro_desejado_investidor = self.lucro_investidor_slider.value() / 100
            
            # Calcular valores
            calculos = self.calculo_service.calcular_imovel(
                self.imovel_atual,
                percentual_lucro_credor=percentual_lucro_credor,
                lucro_desejado_investidor=lucro_desejado_investidor
            )
            
            # Exibir resultados
            self.lbl_custo_total_valor.setText(f"R$ {calculos['custo_total']:,.2f}")
            self.lbl_preco_estimado_valor.setText(f"R$ {calculos['preco_venda_estimado']:,.2f}")
            self.lbl_lucro_credor_calc_valor.setText(f"R$ {calculos['lucro_credor']:,.2f}")
            self.lbl_lucro_investidor_calc_valor.setText(f"R$ {calculos['lucro_investidor']:,.2f}")
            self.lbl_preco_minimo_valor.setText(f"R$ {calculos['preco_minimo']:,.2f}")
            
            # Exibir indicadores financeiros
            margem = calculos['margem']
            self.lbl_margem_valor.setText(f"R$ {margem:,.2f}")
            
            # Colorir margem baseada no valor
            if margem > 0:
                self.lbl_margem_valor.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: #ffffff;
                        background-color: #28a745;
                        padding: 8px;
                        border-radius: 6px;
                        min-width: 120px;
                    }
                """)
            elif margem < 0:
                self.lbl_margem_valor.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: #ffffff;
                        background-color: #dc3545;
                        padding: 8px;
                        border-radius: 6px;
                        min-width: 120px;
                    }
                """)
            else:
                self.lbl_margem_valor.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: #ffffff;
                        background-color: #ffc107;
                        padding: 8px;
                        border-radius: 6px;
                        min-width: 120px;
                    }
                """)
            
            roi = calculos['roi']
            self.lbl_roi_valor.setText(f"{roi:.1f}%")
            
            # Colorir ROI baseado no valor
            if roi > 20:
                self.lbl_roi_valor.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: #ffffff;
                        background-color: #28a745;
                        padding: 8px;
                        border-radius: 6px;
                        min-width: 120px;
                    }
                """)
            elif roi > 10:
                self.lbl_roi_valor.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: #ffffff;
                        background-color: #ffc107;
                        padding: 8px;
                        border-radius: 6px;
                        min-width: 120px;
                    }
                """)
            elif roi > 0:
                self.lbl_roi_valor.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: #ffffff;
                        background-color: #fd7e14;
                        padding: 8px;
                        border-radius: 6px;
                        min-width: 120px;
                    }
                """)
            else:
                self.lbl_roi_valor.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: #ffffff;
                        background-color: #dc3545;
                        padding: 8px;
                        border-radius: 6px;
                        min-width: 120px;
                    }
                """)
            
            # Calcular payback estimado
            if margem > 0:
                payback_meses = int((calculos['custo_total'] / margem) * 12)
                if payback_meses < 12:
                    self.lbl_payback_valor.setText(f"{payback_meses} meses")
                else:
                    anos = payback_meses // 12
                    meses = payback_meses % 12
                    if meses == 0:
                        self.lbl_payback_valor.setText(f"{anos} anos")
                    else:
                        self.lbl_payback_valor.setText(f"{anos} anos e {meses} meses")
            else:
                self.lbl_payback_valor.setText("N/A")
                
        except Exception as e:
            logging.error(f"Erro ao calcular valores: {e}")
            self.limpar_valores()
            
    def limpar_valores(self):
        """Limpa todos os valores exibidos"""
        self.lbl_custo_total_valor.setText("R$ 0,00")
        self.lbl_preco_estimado_valor.setText("R$ 0,00")
        self.lbl_lucro_credor_calc_valor.setText("R$ 0,00")
        self.lbl_lucro_investidor_calc_valor.setText("R$ 0,00")
        self.lbl_preco_minimo_valor.setText("R$ 0,00")
        self.lbl_margem_valor.setText("R$ 0,00")
        self.lbl_roi_valor.setText("0,0%")
        self.lbl_payback_valor.setText("0 meses")
        
        # Resetar cores
        self.lbl_margem_valor.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #495057;
                padding: 8px;
                border-radius: 6px;
                min-width: 120px;
            }
        """)
        
        self.lbl_roi_valor.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #495057;
                padding: 8px;
                border-radius: 6px;
                min-width: 120px;
            }
        """)
        
    def on_parametros_changed(self):
        """Chamado quando os parâmetros são alterados"""
        if self.imovel_atual:
            self.calcular_e_exibir()
