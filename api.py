#!/usr/bin/env python3
"""
API REST para remoção de fundo.
Recebe pedidos de sites externos via HTTP.
"""

import io
import os
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from PIL import Image

from core import remover_fundo

app = FastAPI(
    title="RemoverBG API",
    description="API para remoção de fundo de imagens. Use em seu site ou aplicação.",
    version="1.0.0",
)

# CORS - permite requisições de sites externos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: liste os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODELOS = ["u2netp", "u2net", "isnet-general-use", "birefnet-general", "bria-rmbg", "u2net_human_seg"]


@app.get("/")
def root():
    """Informações da API."""
    return {
        "api": "RemoverBG",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "POST /remove": "Envie imagem (form-data: file) - retorna PNG sem fundo",
            "GET /health": "Status da API",
        },
    }


@app.get("/health")
def health():
    """Verifica se a API está online."""
    return {"status": "ok"}


@app.post(
    "/remove",
    response_class=Response,
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Imagem PNG com fundo removido",
        }
    },
)
async def remove_background(
    file: UploadFile = File(..., description="Imagem (PNG, JPG, HEIC, etc.)"),
    modelo: str = Form("u2netp", description="Modelo: u2netp, u2net, birefnet-general, etc."),
    alpha_matting: bool = Form(False, description="Bordas suaves (mais lento)"),
    bgcolor: str | None = Form(None, description="Cor de fundo hex, ex: FFFFFF"),
):
    """
    Remove o fundo da imagem e retorna PNG com transparência.

    **Exemplo com cURL:**
    ```bash
    curl -X POST "http://localhost:8000/remove" \\
      -F "file=@foto.jpg" \\
      -F "modelo=u2netp" \\
      -o resultado.png
    ```

    **Exemplo JavaScript (fetch):**
    ```javascript
    const formData = new FormData();
    formData.append('file', arquivoInput.files[0]);
    formData.append('modelo', 'u2netp');

    const response = await fetch('http://localhost:8000/remove', {
      method: 'POST',
      body: formData
    });
    const blob = await response.blob();
    // blob é a imagem PNG
    ```
    """
    if modelo not in MODELOS:
        raise HTTPException(400, f"Modelo inválido. Use: {', '.join(MODELOS)}")

    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(400, f"Imagem inválida: {e}")

    # Cor de fundo opcional
    bgcolor_tuple = None
    if bgcolor and bgcolor.strip():
        hex_color = bgcolor.strip().lstrip("#")
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            bgcolor_tuple = (r, g, b, 255)

    try:
        output = remover_fundo(
            img,
            modelo=modelo,
            alpha_matting=alpha_matting,
            bgcolor=bgcolor_tuple,
        )
    except Exception as e:
        raise HTTPException(500, f"Erro ao processar: {e}")

    buffer = io.BytesIO()
    output.save(buffer, format="PNG")
    buffer.seek(0)

    return Response(
        content=buffer.getvalue(),
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=removed_bg.png"},
    )


def main():
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
