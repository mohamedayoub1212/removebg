# RemoverBG - Remoção de Fundo com Alta Qualidade

Script Python para remover o fundo de fotos e imagens com alta qualidade, utilizando a biblioteca **rembg** e modelos de IA de última geração.

## Deploy online (gratuito)

**Hugging Face Spaces** – suba em minutos, como no GitHub:
1. Crie conta em [huggingface.co](https://huggingface.co)
2. [Crie um novo Space](https://huggingface.co/new-space) → SDK: **Gradio**
3. Envie os arquivos `app.py`, `core.py`, `requirements.txt`
4. Pronto! Link público: `https://huggingface.co/spaces/SEU_USUARIO/removerbg`

📖 Guia completo: [DEPLOY.md](DEPLOY.md)

## Características

- **Alta qualidade**: Alpha matting para bordas suaves e naturais
- **Múltiplos modelos**: Do mais rápido ao de máxima qualidade
- **Suporte HEIC**: Fotos do iPhone (formato .heic)
- **Processamento em lote**: Processa pastas inteiras de uma vez
- **PNG com transparência**: Saída em alta resolução

## Instalação

```bash
# Criar ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

**Nota**: Na primeira execução, o modelo será baixado automaticamente (~100-200 MB).

## Uso

### Uma única imagem

```bash
python remove_bg.py foto.jpg
# Gera: foto_sem_fundo.png

# Especificar arquivo de saída
python remove_bg.py foto.jpg -o resultado.png
```

### Pasta inteira

```bash
python remove_bg.py ./minhas_fotos -o ./resultados
```

### Escolher modelo de qualidade

```bash
# Máxima qualidade (recomendado)
python remove_bg.py foto.jpg -m bria-rmbg

# Excelente qualidade, mais rápido
python remove_bg.py foto.jpg -m birefnet-general

# Otimizado para fotos de pessoas
python remove_bg.py retrato.jpg -m u2net_human_seg
```

### Listar modelos disponíveis

```bash
python remove_bg.py --listar-modelos
```

## Modelos Recomendados

| Modelo | Qualidade | Velocidade | Uso |
|--------|-----------|------------|-----|
| `bria-rmbg` | ★★★★★ | ★★☆☆☆ | Máxima qualidade |
| `birefnet-general` | ★★★★☆ | ★★★☆☆ | **Recomendado** - equilíbrio |
| `isnet-general-use` | ★★★★☆ | ★★★☆☆ | Uso geral |
| `u2net_human_seg` | ★★★★☆ | ★★★★☆ | Fotos de pessoas |
| `u2net` | ★★★☆☆ | ★★★★☆ | Padrão |
| `u2netp` | ★★☆☆☆ | ★★★★★ | Mais rápido |

## Uso como Biblioteca

```python
from remove_bg import remover_fundo

# Básico
remover_fundo("entrada.jpg", "saida.png")

# Alta qualidade com modelo específico
remover_fundo(
    "foto.jpg",
    "foto_sem_fundo.png",
    modelo="bria-rmbg",
    alpha_matting=True,
    post_process=True,
)
```

## Opções de Linha de Comando

- `--sem-alpha-matting` - Desativa suavização de bordas (mais rápido)
- `--sem-post-process` - Desativa pós-processamento
- `-m, --modelo` - Escolhe o modelo de IA

## API REST (para sites externos)

Para receber pedidos de sites ou aplicações externas:

```bash
python api.py
```

A API sobe em **http://localhost:8000**

### Endpoint POST /remove

Envia uma imagem e recebe PNG com fundo removido.

**Parâmetros (form-data):**
- `file` (obrigatório): arquivo da imagem
- `modelo`: u2netp, u2net, birefnet-general, etc. (padrão: u2netp)
- `alpha_matting`: true/false (padrão: false)
- `bgcolor`: cor hex para fundo, ex: FFFFFF (opcional)

**Exemplo cURL:**
```bash
curl -X POST "http://localhost:8000/remove" -F "file=@foto.jpg" -o resultado.png
```

**Exemplo JavaScript (site externo):**
```javascript
const formData = new FormData();
formData.append('file', inputFile.files[0]);
formData.append('modelo', 'u2netp');

const response = await fetch('http://SEU_SERVIDOR:8000/remove', {
  method: 'POST',
  body: formData
});
const blob = await response.blob();
// Use blob como imagem ou faça download
```

**Documentação interativa:** http://localhost:8000/docs

## App Visual (Interface Web)

Para usar a interface gráfica no navegador:

```bash
python app.py
```

Acesse **http://127.0.0.1:7880** no navegador. Você pode:
- Arrastar imagens para processar
- Ver comparação antes/depois
- Baixar o resultado
- Processar várias imagens em lote

## Requisitos

- Python 3.11 ou superior
- ~2 GB de RAM (modelos carregados em memória)
- GPU opcional para aceleração (NVIDIA com CUDA)
