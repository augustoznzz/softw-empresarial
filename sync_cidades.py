#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para sincronizar cidades de Santa Catarina com a API do IBGE
"""

import sys
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Função principal para sincronizar cidades"""
    try:
        print("🌐 Iniciando sincronização de cidades de Santa Catarina...")
        print("=" * 60)
        
        # Importar o serviço de cidades
        from services.cidade_service import CidadeService
        
        # Criar instância do serviço
        cidade_service = CidadeService()
        
        print("📡 Conectando com API do IBGE...")
        
        # Sincronizar cidades (forçar atualização)
        sucesso = cidade_service.sincronizar_cidades(forcar_atualizacao=True)
        
        if sucesso:
            print("✅ Cidades sincronizadas com sucesso!")
            
            # Obter estatísticas
            stats = cidade_service.get_estatisticas()
            
            print(f"\n📊 Estatísticas:")
            print(f"   Total de cidades: {stats.get('total_cidades', 0)}")
            print(f"   Fonte: {stats.get('fonte', 'N/A')}")
            print(f"   Última atualização: {stats.get('ultima_atualizacao', 'N/A')}")
            
            if 'cidades_por_regiao' in stats:
                print(f"\n🗺️  Cidades por região:")
                for regiao, count in stats['cidades_por_regiao'].items():
                    print(f"   {regiao}: {count} cidades")
            
            # Mostrar algumas cidades de exemplo
            print(f"\n🏙️  Exemplos de cidades:")
            todas_cidades = cidade_service.get_todas_cidades()
            for i, cidade in enumerate(todas_cidades[:10]):
                print(f"   {i+1:2d}. {cidade}")
            
            if len(todas_cidades) > 10:
                print(f"   ... e mais {len(todas_cidades) - 10} cidades")
                
        else:
            print("❌ Falha na sincronização das cidades")
            return False
            
        print("\n🎉 Sincronização concluída!")
        print("💡 Agora você pode executar a aplicação principal.")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Certifique-se de que todas as dependências estão instaladas:")
        print("   pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        logging.error(f"Erro detalhado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
