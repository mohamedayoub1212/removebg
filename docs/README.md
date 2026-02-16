# RemoverBG - Página Web

Esta pasta é usada para **GitHub Pages**.

## Como ativar o GitHub Pages

1. Envie este projeto para o GitHub (se ainda não fez)
2. No repositório: **Settings** → **Pages**
3. Em "Source": selecione **Deploy from a branch**
4. Branch: **main** | Pasta: **/docs**
5. Salve

Sua página ficará em: `https://mohamadayoub192.github.io/removebg/`

## Importante

O GitHub Pages hospeda **só o frontend** (HTML/CSS/JS). O processamento de imagens precisa de um backend (API).

**Para funcionar completo:**
1. Faça deploy da API em [Render](https://render.com) ou [Railway](https://railway.app)
2. No `index.html`, troque `SEU_LINK_DA_API_AQUI` pela URL da sua API

**Sem API:** A página serve como vitrine/landing. Use o app local: `python app.py`
