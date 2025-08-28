# Instruções para Hospedagem no Netlify

## ⚠️ Importante

O Netlify hospeda apenas sites estáticos (HTML, CSS, JavaScript). Como seu projeto usa Flask (Python), você tem algumas opções:

## Opção 1: Site Estático (Sem Funcionalidade de Busca)

1. Faça upload apenas da pasta `static/` para o Netlify
2. O site ficará bonito mas sem a funcionalidade de busca por CPF
3. O gráfico de estatísticas não funcionará

## Opção 2: Backend + Frontend Separados (Recomendado)

### Para o Backend (Flask):
1. **Railway** (gratuito): https://railway.app/
2. **Heroku** (pago): https://heroku.com/
3. **Render** (gratuito): https://render.com/

### Para o Frontend (Netlify):
1. Modifique as URLs no arquivo `static/index.html`
2. Substitua todas as ocorrências de `/search`, `/statistics`, `/export-pdf` pela URL do seu backend
3. Exemplo: `https://seu-backend.railway.app/search`

## Opção 3: Tudo em Um Serviço

Use um serviço que suporte Python:
- **Railway** (recomendado)
- **Render**
- **Heroku**

## Passos para Railway (Recomendado)

1. Acesse https://railway.app/
2. Conecte sua conta GitHub
3. Faça upload do projeto completo
4. Railway detectará automaticamente que é um projeto Python
5. Seu site ficará disponível em uma URL como: `https://seu-projeto.railway.app`

## Modificações Necessárias para Netlify

Se escolher a Opção 2, edite o arquivo `static/index.html` e substitua:

```javascript
// Linha ~545 - Buscar dados
const response = await fetch('/search', {
// Por:
const response = await fetch('https://SEU-BACKEND.railway.app/search', {

// Linha ~520 - Estatísticas
const response = await fetch('/statistics');
// Por:
const response = await fetch('https://SEU-BACKEND.railway.app/statistics');

// Linha ~620 - Exportar PDF
const response = await fetch('/export-pdf', {
// Por:
const response = await fetch('https://SEU-BACKEND.railway.app/export-pdf', {
```

## Conclusão

Para máxima funcionalidade e facilidade, recomendo usar **Railway** para hospedar o projeto completo. É gratuito e suporta Python/Flask nativamente.

