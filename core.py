#!/usr/bin/env python3
"""
Lógica compartilhada de remoção de fundo.
Usado pelo app Gradio e pela API REST.
"""

from PIL import Image
from rembg import remove, new_session

# Suporte HEIC
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

_sessions = {}
MAX_SIZE = 1024


def get_session(modelo: str):
    if modelo not in _sessions:
        _sessions[modelo] = new_session(modelo)
    return _sessions[modelo]


def remover_fundo(
    img: Image.Image,
    modelo: str = "u2netp",
    alpha_matting: bool = False,
    bgcolor: tuple[int, int, int, int] | None = None,
    max_size: int = MAX_SIZE,
) -> Image.Image:
    """Remove fundo e retorna imagem PNG com transparência."""
    img = img.convert("RGB")

    w, h = img.size
    if max_size and max(w, h) > max_size:
        ratio = max_size / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)

    session = get_session(modelo)
    output = remove(
        img,
        session=session,
        alpha_matting=alpha_matting,
        alpha_matting_foreground_threshold=270,
        alpha_matting_background_threshold=20,
        alpha_matting_erode_size=11,
        post_process_mask=True,
        bgcolor=bgcolor,
    )
    return output
