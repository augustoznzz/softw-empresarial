# 🏠 Sistema de Negociação de Imóveis

Sistema desktop completo para análise e negociação de imóveis, desenvolvido em Python com interface gráfica PySide6.

## ✨ Funcionalidades

### 📋 Cadastro de Imóveis
- **Dados básicos**: Endereço, cidade, estado, CEP, coordenadas
- **Características**: Metragem, quartos, banheiros, ano, padrão de acabamento
- **Custos**: Aquisição, reforma, transação (ITBI, cartório, corretagem, impostos)
- **Status**: Em análise, comprado, vendido
- **Lucro do credor**: Percentual configurável por imóvel

### 🗺️ Fatores de Localização
- Tabela de índices por bairro/CEP (fator de 0,80 a 1,30)
- Influencia diretamente o preço de venda estimado
- Dados pré-cadastrados para principais cidades brasileiras

### 🧮 Cálculos Automáticos
- **Preço de venda estimado**: Base m² × Metragem × Fator Localização × Fator Padrão
- **Custo total**: Aquisição + Reforma + Transação
- **Lucros**: Credor e investidor (percentuais configuráveis)
- **Margem**: Preço estimado - Preço mínimo
- **ROI**: Retorno sobre investimento
- **Payback**: Tempo estimado de retorno

### 📊 Interface Intuitiva
- **Layout em 3 blocos**: Filtros, Tabela de imóveis, Painel de cálculos
- **Sliders interativos**: Ajuste de percentuais com atualização em tempo real
- **Código de cores**: Verde (positivo), amarelo (limite), vermelho (negativo)
- **Filtros avançados**: Por cidade, bairro, status, ROI, margem, características

### 📈 Relatórios e Exportação
- **PDF**: Relatório completo com tabelas e resumos financeiros
- **Excel**: Dados estruturados com formatação profissional
- **Filtros aplicados**: Incluídos nos relatórios para rastreabilidade

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Windows 10/11 (desenvolvido e testado)

### Instalação Manual

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd softw-empresarial
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o seed do banco (opcional)**
   ```bash
   python utils/seed_data.py
   ```

4. **Execute a aplicação**
   ```bash
   python main.py
   ```

### Instalação via Executável

1. **Baixe o executável** da seção de releases
2. **Execute o instalador** como administrador
3. **Acesse via atalho** na área de trabalho

## 🔧 Build do Executável

### Build Automático
```bash
python build.py
```

### Build Manual com PyInstaller
```bash
# Instalar PyInstaller
pip install pyinstaller

# Criar executável
pyinstaller --onefile --windowed --name=SistemaImoveis main.py

# Executável será gerado em dist/SistemaImoveis.exe
```

## 📖 Como Usar

### 1. Primeiro Acesso
- O sistema cria automaticamente o banco SQLite
- Dados de localização são pré-cadastrados
- Parâmetros globais são configurados com valores padrão

### 2. Cadastro de Imóveis
- Clique em "🆕 Novo Imóvel"
- Preencha os dados obrigatórios (endereço, cidade, metragem, custo)
- Ajuste percentual de lucro do credor se necessário
- Clique em "💾 Salvar"

### 3. Análise e Cálculos
- Selecione um imóvel na tabela
- Use os sliders para ajustar percentuais
- Visualize resultados em tempo real
- Analise a viabilidade do investimento

### 4. Filtros e Busca
- Use filtros por cidade, status, características
- Aplique filtros financeiros (ROI, margem)
- Ordene por diferentes critérios
- Exporte dados filtrados

### 5. Exportação
- **PDF**: Relatório completo para apresentações
- **Excel**: Análise detalhada em planilhas
- Filtros aplicados são incluídos automaticamente

## 🏗️ Arquitetura do Sistema

### Estrutura de Diretórios
```
softw-empresarial/
├── main.py                 # Aplicação principal
├── requirements.txt        # Dependências Python
├── build.py               # Script de build
├── models/                # Modelos de dados
│   ├── database.py        # Gerenciador de banco
│   ├── imovel.py          # Modelo de imóvel
│   ├── localizacao.py     # Índices de localização
│   └── parametros.py      # Parâmetros globais
├── services/              # Lógica de negócio
│   ├── calculo_service.py # Cálculos financeiros
│   └── export_service.py  # Exportação PDF/Excel
├── ui/                    # Interface do usuário
│   ├── main_window.py     # Janela principal
│   ├── imovel_form.py     # Formulário de imóvel
│   ├── filtros_widget.py  # Widget de filtros
│   ├── tabela_imoveis.py  # Tabela de imóveis
│   └── painel_calculo.py  # Painel de cálculos
└── utils/                 # Utilitários
    └── seed_data.py       # Dados de exemplo
```

### Tecnologias Utilizadas
- **Backend**: Python 3.8+
- **Interface**: PySide6 (Qt para Python)
- **Banco**: SQLite com migrações automáticas
- **Relatórios**: ReportLab (PDF), OpenPyXL (Excel)
- **Build**: PyInstaller para executável Windows

## 📊 Modelo de Dados

### Tabela de Imóveis
```sql
CREATE TABLE imoveis (
  id INTEGER PRIMARY KEY,
  endereco TEXT NOT NULL,
  cidade TEXT NOT NULL,
  estado TEXT NOT NULL,
  cep TEXT,
  latitude REAL,
  longitude REAL,
  metragem REAL NOT NULL,
  quartos INTEGER,
  banheiros INTEGER,
  ano INTEGER,
  padrao_acabamento TEXT CHECK(padrao_acabamento IN ('baixo', 'medio', 'alto')),
  custo_aquisicao REAL NOT NULL,
  custos_reforma REAL DEFAULT 0,
  custos_transacao REAL DEFAULT 0,
  percentual_lucro_credor REAL DEFAULT 10.0,
  status TEXT CHECK(status IN ('em_analise', 'comprado', 'vendido')),
  data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Fórmulas de Cálculo
```
Preço Estimado = Preço Base m² × Metragem × Fator Localização × Fator Padrão
Custo Total = Aquisição + Reforma + Transação
Lucro Credor = Custo Total × Percentual Credor
Lucro Investidor = Custo Total × Percentual Investidor
Preço Mínimo = Custo Total + Lucro Credor + Lucro Investidor
Margem = Preço Estimado - Preço Mínimo
ROI = (Margem / Custo Total) × 100
```

## 🧪 Testes

### Executar Testes Básicos
```bash
python -c "
import models.database
import models.imovel
import services.calculo_service
print('✅ Todos os módulos importam corretamente')
"
```

### Teste de Banco
```bash
python -c "
from models.database import DatabaseManager
db = DatabaseManager('test.db')
print('✅ Banco de dados funcionando')
import os; os.remove('test.db') if os.path.exists('test.db') else None
"
```

## 🚨 Solução de Problemas

### Erro de Importação
```bash
# Verificar se está no diretório correto
ls main.py

# Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Erro de Banco de Dados
```bash
# Remover banco corrompido
rm imoveis.db

# Executar novamente (será recriado automaticamente)
python main.py
```

### Erro de Build
```bash
# Limpar cache do PyInstaller
rm -rf build dist __pycache__

# Reinstalar PyInstaller
pip uninstall pyinstaller
pip install pyinstaller

# Tentar build novamente
python build.py
```

## 📝 Configuração

### Parâmetros Globais
- **Preço Base m²**: Valor base para cálculos (padrão: R$ 5.000)
- **Fatores de Padrão**: Baixo (0,9), Médio (1,0), Alto (1,1)
- **Lucro Investidor**: Percentual padrão (padrão: 15%)
- **Lucro Credor**: Percentual padrão (padrão: 10%)

### Personalização
- Edite `models/parametros.py` para alterar valores padrão
- Modifique `utils/seed_data.py` para adicionar mais dados de exemplo
- Ajuste fórmulas em `services/calculo_service.py`

## 🤝 Contribuição

### Desenvolvimento
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

### Padrões de Código
- Python PEP 8
- Docstrings em português
- Tratamento de exceções
- Logging para debug

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🆘 Suporte

### Issues Conhecidos
- Nenhum reportado até o momento

### Como Reportar Bugs
1. Verifique se o problema já foi reportado
2. Use o template de issue
3. Inclua logs de erro e passos para reproduzir

### Contato
- Abra uma issue no GitHub
- Descreva o problema detalhadamente
- Inclua informações do sistema (Windows, Python)

---

**Desenvolvido com ❤️ para facilitar a análise de investimentos imobiliários**

