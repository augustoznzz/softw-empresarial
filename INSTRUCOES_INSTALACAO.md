# 🏠 Sistema de Negociação de Imóveis - Instruções de Instalação e Uso

## 📋 Visão Geral

O **Sistema de Negociação de Imóveis** é uma aplicação desktop desenvolvida em Python com PySide6 para Windows, que permite calcular preços-alvo, margens e ROI de imóveis com base na localização e características da propriedade.

## 🚀 Instalação Rápida

### Opção 1: Executável (Recomendado)
1. Baixe o arquivo `Sistema_Negociacao_Imoveis.exe` da pasta `dist/`
2. Execute o arquivo clicando duas vezes
3. A aplicação abrirá automaticamente

### Opção 2: Código Fonte
1. Instale Python 3.13 ou superior
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute: `python main.py`

## 🔧 Requisitos do Sistema

- **Sistema Operacional**: Windows 10/11
- **Memória RAM**: Mínimo 4GB (Recomendado 8GB)
- **Espaço em Disco**: 100MB livres
- **Python**: 3.13+ (apenas para desenvolvimento)

## 📦 Dependências

```
PySide6>=6.8.0          # Interface gráfica
SQLite3                  # Banco de dados (incluído no Python)
ReportLab>=4.0.7         # Geração de PDF
OpenPyXL>=3.1.2          # Geração de Excel
python-dotenv>=1.0.0     # Configurações
```

## 🎯 Funcionalidades Principais

### 🏘️ Cadastro de Imóveis
- **Campos básicos**: ID, endereço, cidade, estado, CEP
- **Características**: metragem, quartos, banheiros, ano, padrão de acabamento
- **Custos**: aquisição, reforma, transação (ITBI, cartório, corretagem)
- **Status**: em análise, comprado, vendido

### 🗺️ Filtros por Região
- **Regiões de Santa Catarina**: Norte, Sul, Leste, Oeste, Central
- **Filtro dinâmico**: ao selecionar uma região, apenas as cidades daquela região aparecem
- **Cidades incluídas**: Todas as principais cidades de Santa Catarina

### 💰 Cálculos Financeiros
- **Preço estimado**: baseado em m², localização e padrão
- **Margem de lucro**: diferença entre preço estimado e custo total
- **ROI**: retorno sobre investimento
- **Payback**: tempo estimado para recuperar o investimento

### 📊 Relatórios
- **Exportação PDF**: relatórios profissionais com logo e formatação
- **Exportação Excel**: dados estruturados para análise
- **Filtros avançados**: por cidade, status, ROI, margem

## 🎨 Interface Moderna

- **Design responsivo**: adapta-se ao tamanho da janela
- **Cores intuitivas**: verde (positivo), amarelo (neutro), vermelho (negativo)
- **Sliders interativos**: ajuste em tempo real dos percentuais de lucro
- **Tabelas organizadas**: ordenação e filtros avançados

## 📁 Estrutura do Projeto

```
softw-empresarial/
├── main.py                 # Aplicação principal
├── models/                 # Modelos de dados
│   ├── database.py        # Gerenciador do banco
│   ├── imovel.py          # Modelo de imóvel
│   ├── localizacao.py     # Índices de localização
│   └── parametros.py      # Parâmetros globais
├── services/               # Serviços de negócio
│   ├── calculo_service.py # Cálculos financeiros
│   └── export_service.py  # Exportação de relatórios
├── ui/                     # Interface do usuário
│   ├── filtros_widget.py  # Widget de filtros
│   ├── tabela_imoveis.py  # Tabela de imóveis
│   ├── painel_calculo.py  # Painel de cálculos
│   └── imovel_form.py     # Formulário de imóvel
├── utils/                  # Utilitários
│   └── seed_data.py       # Dados de exemplo
├── dist/                   # Executável gerado
│   └── Sistema_Negociacao_Imoveis.exe
└── requirements.txt        # Dependências Python
```

## 🚀 Como Usar

### 1. Primeira Execução
- A aplicação criará automaticamente o banco de dados SQLite
- Execute `python utils/seed_data.py` para carregar dados de exemplo

### 2. Navegação
- **Painel Esquerdo**: Filtros e busca
- **Painel Central**: Tabela de imóveis
- **Painel Direito**: Cálculos detalhados do imóvel selecionado

### 3. Filtros
- **Região**: Selecione uma região para filtrar cidades
- **Cidade**: Escolha uma cidade específica
- **Status**: Filtre por status do imóvel
- **Valores**: Defina faixas de metragem, custo, ROI e margem

### 4. Cálculos
- Selecione um imóvel na tabela
- Ajuste os percentuais de lucro com os sliders
- Visualize margem, ROI e payback em tempo real

### 5. Exportação
- **PDF**: Clique em "Export PDF" para gerar relatório
- **Excel**: Clique em "Export Excel" para dados estruturados

## 🛠️ Desenvolvimento

### Executar Testes
```bash
python test_app.py
```

### Gerar Executável
```bash
python build.py
# ou
pyinstaller --onefile --windowed --name "Sistema_Negociacao_Imoveis" main.py
```

### Estrutura do Código
- **MVC Pattern**: Separação clara entre Model, View e Controller
- **Services Layer**: Lógica de negócio isolada
- **Database Manager**: Abstração do banco de dados
- **Signal/Slot**: Comunicação entre componentes da UI

## 🔍 Solução de Problemas

### Erro: "No module named 'PySide6'"
```bash
pip install PySide6>=6.8.0
```

### Erro: "Database is locked"
- Feche a aplicação completamente
- Verifique se não há outros processos Python rodando

### Erro: "Fator de localização não encontrado"
- Execute `python utils/seed_data.py` para carregar dados
- Verifique se a cidade está cadastrada no banco

### Performance Lenta
- Reduza o número de imóveis na tabela
- Use filtros mais específicos
- Feche outras aplicações pesadas

## 📞 Suporte

Para suporte técnico ou dúvidas:
1. Verifique os logs de erro no console
2. Execute os testes: `python test_app.py`
3. Consulte a documentação do código

## 📝 Changelog

### Versão 1.0.0
- ✅ Interface moderna e responsiva
- ✅ Filtros por região de Santa Catarina
- ✅ Cálculos financeiros em tempo real
- ✅ Exportação PDF e Excel
- ✅ Banco de dados SQLite local
- ✅ Executável standalone para Windows

## 🎉 Conclusão

O Sistema de Negociação de Imóveis está pronto para uso em produção, com todas as funcionalidades solicitadas implementadas e testadas. A aplicação oferece uma interface moderna e intuitiva para análise de investimentos imobiliários em Santa Catarina.

**Status**: ✅ PRONTO PARA USO
**Testes**: ✅ 4/4 PASSARAM
**Executável**: ✅ GERADO COM SUCESSO
