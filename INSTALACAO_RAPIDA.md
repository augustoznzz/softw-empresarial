# 🚀 Instalação Rápida - Sistema de Negociação de Imóveis

## ⚡ Instalação em 3 Passos

### 1️⃣ Baixar e Extrair
- Baixe o arquivo ZIP do projeto
- Extraia em uma pasta (ex: `C:\SistemaImoveis`)
- Abra o PowerShell na pasta extraída

### 2️⃣ Instalar Python (se necessário)
```powershell
# Verificar se Python está instalado
python --version

# Se não estiver instalado, baixe de: https://python.org
# Marque "Add Python to PATH" durante a instalação
```

### 3️⃣ Executar o Sistema
```powershell
# Instalar dependências
python -m pip install -r requirements.txt

# Popular banco com dados de exemplo (opcional)
python utils/seed_data.py

# Executar aplicação
python main.py
```

## 🔧 Solução de Problemas Comuns

### ❌ "python não é reconhecido"
- Reinstale Python marcando "Add Python to PATH"
- Reinicie o PowerShell após instalação

### ❌ "pip não é reconhecido"
```powershell
python -m pip install -r requirements.txt
```

### ❌ "Módulo PySide6 não encontrado"
```powershell
python -m pip install PySide6
```

### ❌ "Erro de banco de dados"
```powershell
# Remover banco corrompido
Remove-Item imoveis.db -ErrorAction SilentlyContinue

# Executar novamente
python main.py
```

## 📱 Primeiro Uso

1. **Sistema inicia automaticamente** com banco vazio
2. **Dados de exemplo** são carregados automaticamente
3. **Interface intuitiva** com 3 painéis principais
4. **Sliders interativos** para ajustar percentuais

## 🎯 Funcionalidades Principais

- ✅ **Cadastro de imóveis** com validação automática
- ✅ **Cálculos em tempo real** de preços e margens
- ✅ **Filtros avançados** por cidade, status, ROI
- ✅ **Exportação** para PDF e Excel
- ✅ **Interface responsiva** com código de cores

## 📞 Suporte

- 📧 Abra uma issue no GitHub
- 📖 Consulte o README.md completo
- 🧪 Execute `python test_app.py` para diagnósticos

---

**⚡ Sistema pronto em menos de 5 minutos!**
