# Guia Passo a Passo para Publicar no Railway

O Railway é uma plataforma de nuvem que facilita a publicação de projetos como o seu. Siga estes passos para ter seu site permanentemente online.

## Pré-requisitos

1. **Conta no GitHub**: Se você não tiver uma, crie uma em [github.com](https://github.com).
2. **Conta no Railway**: Crie uma conta em [railway.app](https://railway.app), você pode usar sua conta do GitHub para se registrar.

## Passo 1: Prepare seu Projeto para o GitHub

1. **Descompacte o arquivo** `projeto_site_atualizado_FUNCIONANDO.zip` que eu te enviei.
2. **Crie um novo repositório no GitHub**:
   - Vá para [github.com/new](https://github.com/new).
   - Dê um nome ao seu repositório (ex: `meu-site-processos`).
   - Marque como **Público** ou **Privado**.
   - Clique em **Criar repositório**.
3. **Envie seu projeto para o GitHub**:
   - Se você tem `git` instalado, use a linha de comando:
     ```bash
     git init
     git add .
     git commit -m "Primeiro commit"
     git branch -M main
     git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
     git push -u origin main
     ```
   - Se não, você pode usar o **GitHub Desktop** ou a função de **upload de arquivos** do GitHub.

## Passo 2: Crie um Novo Projeto no Railway

1. **Acesse seu painel** no [railway.app](https://railway.app).
2. Clique em **Novo Projeto**.
3. Selecione **Deploy do repositório do GitHub**.
4. **Configure o acesso ao GitHub** se for a primeira vez.
5. **Selecione o repositório** que você acabou de criar (`meu-site-processos`).

## Passo 3: Configure o Projeto no Railway

O Railway é inteligente e deve detectar que é um projeto Python. Ele vai procurar por um arquivo `requirements.txt` e um `Procfile`.

1. **Variáveis de Ambiente**: O Railway vai instalar as dependências do `requirements.txt` automaticamente. Para este projeto, não são necessárias variáveis de ambiente adicionais.

2. **Comando de Início**: Eu já adicionei um arquivo `Procfile` ao seu projeto. Ele diz ao Railway como iniciar seu site. O conteúdo dele é:
   ```
   web: gunicorn --chdir src main:app
   ```
   - `gunicorn` é um servidor web Python mais robusto que o servidor de desenvolvimento do Flask.
   - `--chdir src` diz ao gunicorn para rodar a partir da pasta `src`.
   - `main:app` diz para ele usar o objeto `app` do arquivo `main.py`.

## Passo 4: Deploy e Acesso ao Site

1. **O Railway vai começar o deploy automaticamente**. Você pode acompanhar o progresso na aba **Deploys**.
2. Quando o deploy estiver completo, vá para a aba **Configurações** do seu projeto no Railway.
3. Em **Domínios**, você encontrará a URL pública do seu site (algo como `meu-site-processos-production.up.railway.app`).

**Pronto! Seu site estará permanentemente online nessa URL.**

## Solução de Problemas

- **Erro no Deploy?**: Verifique os logs de deploy no Railway. Eles são muito úteis para identificar problemas, como uma dependência faltando no `requirements.txt`.
- **O site não carrega?**: Verifique os logs da aplicação para ver se há erros no Flask.

Com estes passos, seu site estará funcionando de forma permanente e acessível a todos!

