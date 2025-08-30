#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de build para gerar executável com PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def run_command(command, description):
    """Executa um comando e trata erros"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}:")
        print(f"Comando: {command}")
        print(f"Erro: {e.stderr}")
        return False

def clean_build_dirs():
    """Limpa diretórios de build anteriores"""
    print("🧹 Limpando diretórios de build anteriores...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  - Removido: {dir_name}")
            
    # Limpar arquivos .spec
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"  - Removido: {spec_file}")

def install_dependencies():
    """Instala dependências necessárias"""
    print("📦 Instalando dependências...")
    
    if not run_command("pip install -r requirements.txt", "Instalação de dependências"):
        return False
        
    return True

def create_executable():
    """Cria o executável com PyInstaller"""
    print("🔨 Criando executável...")
    
    # Comando PyInstaller
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",  # Arquivo único
        "--windowed",  # Sem console (aplicação GUI)
        "--name=SistemaImoveis",  # Nome do executável
        "--icon=assets/icon.ico" if os.path.exists("assets/icon.ico") else "",  # Ícone se existir
        "--add-data=models;models",  # Incluir modelos
        "--add-data=services;services",  # Incluir serviços
        "--add-data=ui;ui",  # Incluir interface
        "--add-data=utils;utils",  # Incluir utilitários
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui",
        "--hidden-import=PySide6.QtWidgets",
        "main.py"
    ]
    
    # Filtrar comandos vazios
    pyinstaller_cmd = [cmd for cmd in pyinstaller_cmd if cmd]
    
    if not run_command(" ".join(pyinstaller_cmd), "Criação do executável"):
        return False
        
    return True

def create_installer():
    """Cria um instalador simples"""
    print("📦 Criando instalador...")
    
    # Criar diretório de distribuição
    dist_dir = "dist/SistemaImoveis"
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    
    # Copiar arquivos necessários
    files_to_copy = [
        ("dist/SistemaImoveis.exe", "SistemaImoveis.exe"),
        ("README.md", "README.md"),
        ("LICENSE", "LICENSE") if os.path.exists("LICENSE") else None
    ]
    
    for src, dst in files_to_copy:
        if src and os.path.exists(src):
            shutil.copy2(src, os.path.join(dist_dir, dst))
            print(f"  - Copiado: {dst}")
    
    # Criar arquivo de instalação
    install_script = os.path.join(dist_dir, "instalar.bat")
    with open(install_script, 'w', encoding='utf-8') as f:
        f.write("""@echo off
echo Instalando Sistema de Negociacao de Imoveis...
echo.

REM Criar diretório de instalação
set INSTALL_DIR=%PROGRAMFILES%\\SistemaImoveis
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copiar arquivos
copy "SistemaImoveis.exe" "%INSTALL_DIR%\\"
copy "README.md" "%INSTALL_DIR%\\"

REM Criar atalho no desktop
set DESKTOP=%USERPROFILE%\\Desktop
echo @echo off > "%DESKTOP%\\Sistema de Imoveis.bat"
echo cd /d "%INSTALL_DIR%" >> "%DESKTOP%\\Sistema de Imoveis.bat"
echo SistemaImoveis.exe >> "%DESKTOP%\\Sistema de Imoveis.bat"

echo.
echo Instalacao concluida!
echo O atalho foi criado na area de trabalho.
echo.
pause
""")
    
    print(f"✅ Instalador criado em: {dist_dir}")
    return True

def run_tests():
    """Executa testes básicos"""
    print("🧪 Executando testes básicos...")
    
    # Teste de importação
    try:
        import models.database
        import models.imovel
        import services.calculo_service
        print("  ✅ Importações funcionando")
    except ImportError as e:
        print(f"  ❌ Erro de importação: {e}")
        return False
    
    # Teste de criação do banco
    try:
        db = models.database.DatabaseManager("test.db")
        print("  ✅ Banco de dados funcionando")
        
        # Limpar banco de teste
        if os.path.exists("test.db"):
            os.remove("test.db")
            
    except Exception as e:
        print(f"  ❌ Erro no banco de dados: {e}")
        return False
    
    print("✅ Testes básicos passaram!")
    return True

def main():
    """Função principal"""
    print("🚀 Iniciando build do Sistema de Negociação de Imóveis")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("main.py"):
        print("❌ Erro: Execute este script no diretório raiz do projeto")
        return False
    
    # Limpar builds anteriores
    clean_build_dirs()
    
    # Instalar dependências
    if not install_dependencies():
        print("❌ Falha na instalação de dependências")
        return False
    
    # Executar testes
    if not run_tests():
        print("❌ Falha nos testes")
        return False
    
    # Criar executável
    if not create_executable():
        print("❌ Falha na criação do executável")
        return False
    
    # Criar instalador
    if not create_installer():
        print("❌ Falha na criação do instalador")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Build concluído com sucesso!")
    print("\nArquivos gerados:")
    print(f"  📁 Executável: dist/SistemaImoveis.exe")
    print(f"  📁 Instalador: dist/SistemaImoveis/")
    print(f"  📁 Build: build/")
    
    print("\nPara distribuir:")
    print("  1. Copie a pasta 'dist/SistemaImoveis' para o computador de destino")
    print("  2. Execute 'instalar.bat' como administrador")
    print("  3. O sistema será instalado e um atalho será criado na área de trabalho")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
