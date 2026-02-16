#!/usr/bin/env python3
"""
Servidor unificado: API REST + Interface Gradio.
- API: POST /remove, GET /docs
- Interface: /
"""

import os

# Importar antes de criar o Gradio app para evitar import circular
from api import app as api_app

# Importar o Gradio app (Blocks)
from app import app as gradio_app

import gradio as gr

# Montar Gradio na raiz (interface visual em /)
# API fica em: /api/remove, /api/docs, /api/health
api_app = gr.mount_gradio_app(api_app, gradio_app, path="/")


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(api_app, host="0.0.0.0", port=port)
