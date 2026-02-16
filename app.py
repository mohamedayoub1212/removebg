#!/usr/bin/env python3
"""
App visual para remoção de fundo de imagens.
Interface web com Gradio - arraste imagens, visualize antes/depois e baixe.
Suporta: PNG, JPG, WEBP, HEIC (fotos do iPhone), etc.
"""

import tempfile
from pathlib import Path

import gradio as gr
from PIL import Image

from core import MAX_SIZE, remover_fundo

# Modelos disponíveis
MODELOS = {
    "u2netp": "Leve e rápido",
    "u2net": "Padrão",
    "isnet-general-use": "Alta qualidade",
    "birefnet-general": "Excelente (recomendado)",
    "bria-rmbg": "Máxima qualidade",
    "u2net_human_seg": "Fotos de pessoas",
}


def processar_imagem(
    img: Image.Image | None,
    modelo: str = "u2netp",
    alpha_matting: bool = False,
    cor_fundo: str | None = None,
) -> tuple[Image.Image | None, Image.Image | None, str | None, str]:
    """
    Remove fundo da imagem e retorna (original, resultado, caminho_download, mensagem_erro).
    """
    if img is None:
        return None, None, None, "Nenhuma imagem carregada."

    try:
        # Converter cor de fundo
        bgcolor_tuple = None
        if cor_fundo and cor_fundo.strip():
            hex_color = cor_fundo.strip().lstrip("#")
            if len(hex_color) == 6:
                r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
                bgcolor_tuple = (r, g, b, 255)

        output = remover_fundo(
            img,
            modelo=modelo,
            alpha_matting=alpha_matting,
            bgcolor=bgcolor_tuple,
        )

        # Salvar em arquivo temporário para download
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            output.save(f.name)
            download_path = f.name

        return img, output, download_path, ""
    except Exception as e:
        return img, None, None, f"Erro: {str(e)}"


# Interface Gradio
with gr.Blocks(title="RemoverBG - Remoção de Fundo") as app:
    gr.Markdown(
        """
        # 🖼️ RemoverBG - Remoção de Fundo com IA
        Arraste suas imagens, remova o fundo com alta qualidade e baixe o resultado.
        """
    )

    with gr.Tabs():
        # Aba: Imagem única
        with gr.TabItem("📷 Imagem única"):
            with gr.Row():
                with gr.Column(scale=1):
                    input_img = gr.Image(
                        label="Imagem de entrada (arraste ou use o seletor abaixo para HEIC)",
                        type="pil",
                        height=350,
                    )
                    input_file = gr.File(
                        label="Ou selecione arquivo (HEIC/HEIF do iPhone suportado)",
                        file_types=["image", ".heic", ".heif"],
                    )
                    with gr.Accordion("⚙️ Opções", open=False):
                        modelo = gr.Dropdown(
                            choices=list(MODELOS.keys()),
                            value="u2netp",
                            label="Modelo de IA",
                            info="u2netp = mais rápido | birefnet = melhor qualidade",
                        )
                        alpha_matting = gr.Checkbox(
                            value=False,
                            label="Alpha matting (bordas suaves - mais lento)",
                        )
                        cor_fundo = gr.Textbox(
                            label="Cor de fundo (hex, ex: #FFFFFF)",
                            placeholder="#FFFFFF para branco, vazio = transparente",
                        )

                    btn_processar = gr.Button("✨ Remover fundo", variant="primary")

                with gr.Column(scale=1):
                    with gr.Row():
                        output_original = gr.Image(
                            label="Original",
                            type="pil",
                            height=250,
                            interactive=False,
                        )
                        output_resultado = gr.Image(
                            label="Sem fundo",
                            type="pil",
                            height=250,
                            interactive=False,
                        )
                    download_btn = gr.DownloadButton(
                        "⬇️ Baixar resultado",
                        visible=False,
                    )
                    status_msg = gr.Markdown(visible=False)

            def carregar_arquivo(file):
                """Carrega imagem de arquivo (inclui HEIC)."""
                if file is None:
                    return None
                f = file[0] if isinstance(file, list) else file
                path = getattr(f, "name", getattr(f, "path", f))
                if path and isinstance(path, str):
                    return Image.open(path).convert("RGB")
                return None

            input_file.change(fn=carregar_arquivo, inputs=[input_file], outputs=[input_img])

            def processar_e_mostrar(img, mod, alpha, cor):
                orig, res, path, erro = processar_imagem(img, mod, alpha, cor)
                if erro:
                    return orig, None, gr.update(visible=False), gr.update(value=f"⚠️ {erro}", visible=True)
                if path:
                    return orig, res, gr.update(value=path, visible=True), gr.update(visible=False)
                return orig, res, gr.update(visible=False), gr.update(visible=False)

            btn_processar.click(
                fn=processar_e_mostrar,
                inputs=[input_img, modelo, alpha_matting, cor_fundo],
                outputs=[output_original, output_resultado, download_btn, status_msg],
            )

        # Aba: Lote
        with gr.TabItem("📁 Processar lote"):
            with gr.Row():
                with gr.Column():
                    batch_input = gr.File(
                        label="Selecione várias imagens",
                        file_count="multiple",
                        file_types=["image", ".heic", ".heif"],
                    )
                    batch_modelo = gr.Dropdown(
                        choices=list(MODELOS.keys()),
                        value="u2netp",
                        label="Modelo",
                    )
                    batch_alpha = gr.Checkbox(value=False, label="Alpha matting (mais lento)")
                    btn_batch = gr.Button("✨ Processar todas", variant="primary")

                with gr.Column():
                    batch_gallery = gr.Gallery(
                        label="Resultados (antes → depois)",
                        columns=2,
                        height="auto",
                        object_fit="contain",
                    )

            def run_batch(files, mod, alpha):
                if not files:
                    return None
                resultados = []
                paths = [
                    f if isinstance(f, str) else getattr(f, "name", getattr(f, "path", str(f)))
                    for f in files
                ]
                for path in paths:
                    img = Image.open(path).convert("RGB")
                    out = remover_fundo(img, modelo=mod, alpha_matting=alpha)
                    resultados.append(out)
                return resultados

            btn_batch.click(
                fn=run_batch,
                inputs=[batch_input, batch_modelo, batch_alpha],
                outputs=[batch_gallery],
            )

    gr.Markdown(
        """
        ---
        **Dicas:** Primeira execução baixa o modelo (~50 MB para u2netp). Imagens grandes são redimensionadas para acelerar.
        Para melhor qualidade, use modelo *birefnet-general* e marque *Alpha matting* (mais lento).
        """
    )


def main():
    import os

    # Deploy (HF Spaces, Railway, etc.): PORT e 0.0.0.0 vêm do ambiente
    port = int(os.environ.get("PORT", 7880))
    server_name = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"

    app.launch(
        server_name=server_name,
        server_port=port,
        share=False,
        theme=gr.themes.Soft(primary_hue="teal", secondary_hue="slate"),
    )


if __name__ == "__main__":
    main()
