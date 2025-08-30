#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicativo de Negociação de Imóveis
Calcula preços-alvo e margens com base na localização e ajusta % de lucro do credor
"""

import sys
import logging
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSplitter, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor, QIcon

from models.database import DatabaseManager
from ui.filtros_widget import FiltrosWidget
from ui.tabela_imoveis import TabelaImoveis
from ui.painel_calculo import PainelCalculo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.setup_ui()
        self.setup_connections()
        self.load_data()
        
    def setup_ui(self):
        """Configura a interface principal da aplicação"""
        self.setWindowTitle("🏠 Sistema de Negociação de Imóveis - Santa Catarina")
        self.setMinimumSize(1400, 900)
        
        # Configurar estilo moderno para a janela principal
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
            QLabel {
                color: #495057;
                font-weight: 500;
            }
            QSplitter::handle {
                background-color: #dee2e6;
                border: 1px solid #adb5bd;
            }
            QSplitter::handle:hover {
                background-color: #007bff;
            }
        """)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Cabeçalho
        self.create_header(main_layout)
        
        # Splitter principal para dividir a tela
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setChildrenCollapsible(False)
        main_splitter.setHandleWidth(3)
        
        # Painel esquerdo (filtros)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Widget de filtros
        self.filtros_widget = FiltrosWidget(self.db_manager)
        left_layout.addWidget(self.filtros_widget)
        
        # Adicionar painel esquerdo ao splitter
        main_splitter.addWidget(left_panel)
        main_splitter.setSizes([400, 1000])  # Largura inicial dos painéis
        
        # Painel direito (tabela e cálculos)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)
        
        # Tabela de imóveis
        self.tabela_imoveis = TabelaImoveis(self.db_manager)
        right_layout.addWidget(self.tabela_imoveis)
        
        # Painel de cálculos
        self.painel_calculo = PainelCalculo(self.db_manager)
        right_layout.addWidget(self.painel_calculo)
        
        # Adicionar painel direito ao splitter
        main_splitter.addWidget(right_panel)
        
        # Adicionar splitter ao layout principal
        main_layout.addWidget(main_splitter, 1)
        
        # Status bar
        self.statusBar().showMessage("Sistema carregado com sucesso! 🎉")
        
    def create_header(self, layout):
        """Cria o cabeçalho da aplicação"""
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #007bff, stop:1 #0056b3);
                border-radius: 15px;
                padding: 20px;
            }
        """)
        
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(30, 25, 30, 25)
        
        # Título principal
        title_label = QLabel("🏠 Sistema de Negociação de Imóveis")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                text-align: center;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Santa Catarina - Análise e Cálculo de Investimentos Imobiliários")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #e3f2fd;
                font-size: 16px;
                font-weight: 500;
                font-family: 'Segoe UI', Arial, sans-serif;
                text-align: center;
                margin-top: 5px;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_widget)
        
    def setup_connections(self):
        """Configura as conexões entre os componentes"""
        # Conectar filtros à tabela
        self.filtros_widget.filtros_alterados.connect(self.tabela_imoveis.aplicar_filtros)
        
        # Conectar seleção na tabela ao painel de cálculos
        self.tabela_imoveis.imovel_selecionado.connect(self.painel_calculo.carregar_imovel)
        
    def load_data(self):
        """Carrega dados iniciais"""
        try:
            # Carregar dados dos imóveis
            self.tabela_imoveis.carregar_imoveis()
            
            # Carregar cidades nos filtros
            self.filtros_widget.load_cidades()
            
            self.statusBar().showMessage("Dados carregados com sucesso! 📊")
            
        except Exception as e:
            logging.error(f"Erro ao carregar dados: {e}")
            self.statusBar().showMessage("Erro ao carregar dados! ❌")

def main():
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Criar aplicação
    app = QApplication(sys.argv)
    
    # Configurar estilo da aplicação
    app.setStyle('Fusion')
    
    # Configurar paleta de cores global
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(248, 249, 250))
    palette.setColor(QPalette.WindowText, QColor(73, 80, 87))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(248, 249, 250))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(73, 80, 87))
    palette.setColor(QPalette.Text, QColor(73, 80, 87))
    palette.setColor(QPalette.Button, QColor(255, 255, 255))
    palette.setColor(QPalette.ButtonText, QColor(73, 80, 87))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Link, QColor(0, 123, 255))
    palette.setColor(QPalette.Highlight, QColor(0, 123, 255))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(palette)
    
    # Configurar fonte global
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    # Criar e mostrar janela principal
    window = MainWindow()
    window.show()
    
    # Executar aplicação
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
