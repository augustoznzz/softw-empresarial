#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste básico para o Sistema de Negociação de Imóveis
"""

import sys
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    print("🧪 Testando importações...")
    
    try:
        # Testar modelos
        from models.database import DatabaseManager
        print("  ✅ models.database - OK")
        
        from models.imovel import Imovel
        print("  ✅ models.imovel - OK")
        
        from models.localizacao import LocalizacaoIndice
        print("  ✅ models.localizacao - OK")
        
        from models.parametros import ParametrosGlobais
        print("  ✅ models.parametros - OK")
        
        # Testar serviços
        from services.calculo_service import CalculoService
        print("  ✅ services.calculo_service - OK")
        
        from services.export_service import ExportService
        print("  ✅ services.export_service - OK")
        
        # Testar UI
        from ui.imovel_form import ImovelForm
        print("  ✅ ui.imovel_form - OK")
        
        from ui.filtros_widget import FiltrosWidget
        print("  ✅ ui.filtros_widget - OK")
        
        from ui.tabela_imoveis import TabelaImoveis
        print("  ✅ ui.tabela_imoveis - OK")
        
        from ui.painel_calculo import PainelCalculo
        print("  ✅ ui.painel_calculo - OK")
        
        print("✅ Todas as importações funcionaram!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_database():
    """Testa a criação e funcionamento do banco de dados"""
    print("\n🗄️ Testando banco de dados...")
    
    try:
        from models.database import DatabaseManager
        
        # Criar banco de teste com nome único
        import uuid
        test_db_path = f"test_imoveis_{uuid.uuid4().hex[:8]}.db"
        db = DatabaseManager(test_db_path)
        print("  ✅ Banco de dados criado com sucesso")
        
        # Testar conexão
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"  ✅ Tabelas criadas: {len(tables)}")
        
        # Verificar tabelas específicas
        table_names = [table[0] for table in tables]
        expected_tables = ['imoveis', 'localizacao_indices', 'parametros_globais']
        
        for expected in expected_tables:
            if expected in table_names:
                print(f"    ✅ Tabela {expected} - OK")
            else:
                print(f"    ❌ Tabela {expected} - Faltando")
                return False
        
        # Fechar conexão e cursor
        cursor.close()
        conn.close()
        
        # Limpar banco de teste
        try:
            if os.path.exists(test_db_path):
                os.remove(test_db_path)
                print("  ✅ Banco de teste removido")
        except Exception as e:
            print(f"  ⚠️ Não foi possível remover o banco de teste: {e}")
        
        print("✅ Banco de dados funcionando perfeitamente!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False

def test_calculos():
    """Testa os cálculos financeiros"""
    print("\n🧮 Testando cálculos financeiros...")
    
    try:
        from models.imovel import Imovel
        from services.calculo_service import CalculoService
        
        # Criar imóvel de teste
        imovel_teste = Imovel(
            endereco="Rua Teste, 123",
            cidade="Capinzal",
            estado="SC",
            metragem=100.0,
            padrao_acabamento="medio",
            custo_aquisicao=300000.0,
            custos_reforma=50000.0,
            custos_transacao=15000.0,
            percentual_lucro_credor=10.0
        )
        print("  ✅ Imóvel de teste criado")
        
        # Testar cálculos
        calculo_service = CalculoService()
        resultado = calculo_service.calcular_tudo(imovel_teste)
        
        # Verificar resultados
        if resultado:
            print(f"  ✅ Cálculos executados:")
            print(f"    - Preço estimado: R$ {resultado.get('preco_venda_estimado', 0):,.2f}")
            print(f"    - Custo total: R$ {resultado.get('custo_total', 0):,.2f}")
            print(f"    - Margem: R$ {resultado.get('margem', 0):,.2f}")
            print(f"    - ROI: {resultado.get('roi', 0):.1f}%")
        else:
            print("  ❌ Cálculos falharam")
            return False
        
        print("✅ Cálculos financeiros funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro nos cálculos: {e}")
        return False

def test_export_service():
    """Testa o serviço de exportação"""
    print("\n📊 Testando serviço de exportação...")
    
    try:
        from services.export_service import ExportService
        
        export_service = ExportService()
        formatos = export_service.get_export_formats()
        
        print(f"  ✅ Formatos disponíveis: {', '.join(formatos)}")
        
        if 'PDF' in formatos:
            print("    ✅ Exportação PDF - Disponível")
        else:
            print("    ⚠️ Exportação PDF - Não disponível (ReportLab)")
            
        if 'Excel' in formatos:
            print("    ✅ Exportação Excel - Disponível")
        else:
            print("    ⚠️ Exportação Excel - Não disponível (OpenPyXL)")
        
        print("✅ Serviço de exportação funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no serviço de exportação: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes do Sistema de Negociação de Imóveis")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("main.py"):
        print("❌ Erro: Execute este script no diretório raiz do projeto")
        return False
    
    # Executar testes
    testes = [
        test_imports,
        test_database,
        test_calculos,
        test_export_service
    ]
    
    resultados = []
    for teste in testes:
        try:
            resultado = teste()
            resultados.append(resultado)
        except Exception as e:
            print(f"❌ Erro inesperado no teste {teste.__name__}: {e}")
            resultados.append(False)
    
    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES")
    print("=" * 60)
    
    total_testes = len(resultados)
    testes_passaram = sum(resultados)
    
    for i, (teste, resultado) in enumerate(zip(testes, resultados), 1):
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{i:2d}. {teste.__name__:20s} - {status}")
    
    print(f"\n📊 Resultado: {testes_passaram}/{total_testes} testes passaram")
    
    if testes_passaram == total_testes:
        print("\n🎉 Todos os testes passaram! O sistema está funcionando corretamente.")
        print("💡 Você pode agora executar 'python main.py' para iniciar a aplicação.")
        return True
    else:
        print(f"\n⚠️ {total_testes - testes_passaram} teste(s) falharam.")
        print("🔧 Verifique os erros acima e corrija antes de executar a aplicação.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
