# Como subir o RemoverBG online

## Opção 1: Hugging Face Spaces (recomendado, gratuito)

A forma mais simples, similar ao GitHub Pages. O app fica online com um link público.

### Passo a passo

1. **Crie uma conta** em [huggingface.co](https://huggingface.co) (gratuito)

2. **Crie um novo Space:**
   - Acesse [huggingface.co/new-space](https://huggingface.co/new-space)
   - Nome: `removerbg` (ou outro)
   - SDK: **Gradio**
   - Hardware: **CPU basic** (gratuito)
   - Clique em "Create Space"

3. **Conecte ao GitHub** (opcional, para atualizar automaticamente):
   - No Space, vá em **Settings** → **Repository**
   - Clique em "Connect to GitHub"
   - Selecione seu repositório

4. **Ou envie os arquivos manualmente:**
   - Faça upload dos arquivos: `app.py`, `core.py`, `requirements.txt`
   - O Space detecta e inicia automaticamente

5. **Pronto!** Seu app estará em:
   ```
   https://huggingface.co/spaces/SEU_USUARIO/removerbg
   ```

### Arquivos necessários no repositório

```
REMOVERBG/
├── app.py          # App principal (Gradio)
├── core.py         # Lógica de remoção
├── requirements.txt
└── README.md       # Descrição do Space
```

### API do Space (para sites externos)

O Hugging Face Spaces com Gradio tem API nativa. Para chamar de outro site:

```javascript
// Usando a API do Gradio
const response = await fetch(
  'https://SEU_USUARIO-removerbg.hf.space/api/predict',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      data: [imageBase64, 'u2netp', false]  // img, modelo, alpha_matting
    })
  }
);
```

Ou use o [Gradio Client](https://gradio.com/guides/getting-started-with-the-js-client) em JavaScript.

---

## Opção 2: Railway (com API completa)

Para rodar a API FastAPI com domínio próprio:

1. Crie conta em [railway.app](https://railway.app)
2. Conecte o repositório GitHub
3. Adicione `Procfile`:
   ```
   web: uvicorn api:app --host 0.0.0.0 --port $PORT
   ```
4. Railway detecta e faz deploy automático

---

## Opção 3: Render

1. Crie conta em [render.com](https://render.com)
2. New → Web Service
3. Conecte o repositório
4. Configurações:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn api:app --host 0.0.0.0 --port $PORT`

---

## Resumo

| Plataforma | Gratuito | Melhor para |
|------------|----------|-------------|
| **Hugging Face** | Sim | App visual (Gradio) |
| **Railway** | 500h/mês | API + App |
| **Render** | Sim (com sleep) | API |

**Recomendação:** Use **Hugging Face Spaces** para o app visual. É gratuito, simples e o link fica permanente.
