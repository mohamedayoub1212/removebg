# Como usar a API do RemoverBG

## URL base

Se o app está no Replit: `https://SEU_REPL.replit.app`

## Endpoints

| Método | URL | Descrição |
|--------|-----|-----------|
| POST | `/api/remove` | Remove fundo da imagem |
| GET | `/api/health` | Status da API |
| GET | `/api/docs` | Documentação interativa |

## Exemplo: cURL

```bash
curl -X POST "https://SEU_REPL.replit.app/api/remove" \
  -F "file=@foto.jpg" \
  -F "modelo=u2netp" \
  -o resultado.png
```

## Exemplo: JavaScript (fetch)

```javascript
const formData = new FormData();
formData.append('file', inputFile.files[0]);
formData.append('modelo', 'u2netp');

const response = await fetch('https://SEU_REPL.replit.app/api/remove', {
  method: 'POST',
  body: formData
});

const blob = await response.blob();
// blob = imagem PNG sem fundo
```

## Parâmetros (form-data)

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| file | arquivo | obrigatório | Imagem (PNG, JPG, HEIC, etc.) |
| modelo | string | u2netp | u2netp, u2net, birefnet-general, etc. |
| alpha_matting | bool | false | Bordas suaves (mais lento) |
| bgcolor | string | - | Cor de fundo hex, ex: FFFFFF |

## Resposta

- **Sucesso (200):** Imagem PNG com fundo removido
- **Erro (4xx/5xx):** JSON com mensagem de erro
