# Sistema de Consulta de Processos Jurídicos

## Status do Projeto ✅

**PROJETO TOTALMENTE FUNCIONAL!** Todos os problemas foram resolvidos:

- ✅ **Gráfico de rosca funcionando perfeitamente** - Exibe estatísticas das ações em tempo real
- ✅ **Consulta por CPF funcionando** - Sem erros de conexão
- ✅ **Exportação para PDF funcionando** - Gera relatórios completos
- ✅ **Interface responsiva** - Funciona em desktop e mobile
- ✅ **Dados atualizados automaticamente** - Monitor contínuo da planilha Excel

## Estrutura do Projeto

```
projeto_site_atualizado/
├── src/
│   ├── main.py                 # Servidor Flask principal
│   ├── PROCESSOSCLIENTES.xlsx  # Planilha com dados dos clientes
│   └── LOGO.jpg               # Logo do escritório
├── static/
│   ├── index.html             # Interface web principal
│   └── LOGO.jpg              # Logo para o frontend
├── requirements.txt           # Dependências Python
└── README.md                 # Este arquivo
```

## Funcionalidades Testadas

1. **Gráfico de Estatísticas**: Mostra distribuição das ações (PASEP, TETO, ISB, etc.)
2. **Busca por CPF**: Consulta processos usando CPF com máscara automática
3. **Exibição de Resultados**: Mostra dados do cliente e processos associados
4. **Exportação PDF**: Gera relatório completo com logo e informações de contato
5. **Responsividade**: Interface adaptada para diferentes tamanhos de tela

## Como Hospedar no Netlify

### Opção 1: Deploy do Frontend Estático (Recomendado para Netlify)

Para hospedar no Netlify, você precisará de uma versão estática do site. Como o projeto atual usa Flask (backend), você tem duas opções:

1. **Usar apenas o frontend estático** (sem funcionalidade de busca dinâmica)
2. **Hospedar o backend em outro serviço** (Heroku, Railway, etc.) e o frontend no Netlify

### Opção 2: Deploy Completo (Backend + Frontend)

Para manter todas as funcionalidades, recomendo:

1. **Backend**: Hospedar em Railway, Heroku ou similar
2. **Frontend**: Pode ser hospedado no Netlify apontando para o backend

### Instruções para Netlify (Frontend Estático)

1. Faça upload apenas da pasta `static/` para o Netlify
2. Configure o arquivo `index.html` como página principal
3. As funcionalidades de busca não funcionarão sem o backend

### Instruções para Deploy Completo

1. **Backend (Railway/Heroku)**:
   - Faça upload de todo o projeto
   - Configure as variáveis de ambiente
   - Execute `pip install -r requirements.txt`
   - Execute `python src/main.py`

2. **Frontend (Netlify)**:
   - Atualize as URLs no `index.html` para apontar para seu backend
   - Faça upload da pasta `static/`

## Dependências

- Python 3.11+
- Flask 3.1.1
- Flask-CORS 6.0.0
- Flask-SQLAlchemy 3.1.1
- pandas (para leitura da planilha Excel)
- reportlab (para geração de PDF)
- openpyxl (para arquivos Excel)

## Configuração Local

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Execute o servidor:
   ```bash
   cd src
   python main.py
   ```

3. Acesse: `http://localhost:5001`

## Contato

- **Telefones**: (79) 9.8150-9934 / (79) 9.8833-9003
- **Email**: escritoriojsantosadvocacia@gmail.com
- **Site**: jefersonsantos.godaddysites.com

---

**Desenvolvido para Jeferson Santos Advocacia & Assessoria Jurídica**

