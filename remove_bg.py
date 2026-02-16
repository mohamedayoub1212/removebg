#!/usr/bin/env python3
"""
Script de remoção de fundo de imagens com ALTA QUALIDADE.
Utiliza rembg com alpha matting e modelos de última geração.
Suporta: PNG, JPG, WEBP, HEIC (fotos do iPhone), etc.
"""

import argparse
from pathlib import Path

from PIL import Image

# Suporte a HEIC/HEIF (fotos do iPhone)
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass  # pillow-heif não instalado, HEIC não suportado
from rembg import remove, new_session


# Modelos disponíveis (do mais leve ao de maior qualidade)
MODELOS = {
    "u2netp": "Leve e rápido - boa qualidade",
    "u2net": "Padrão - equilíbrio qualidade/velocidade",
    "isnet-general-use": "Alta qualidade - uso geral",
    "birefnet-general": "Excelente qualidade - recomendado",
    "bria-rmbg": "State-of-the-art - máxima qualidade",
    "u2net_human_seg": "Otimizado para fotos de pessoas",
}


def remover_fundo(
    entrada: str | Path,
    saida: str | Path | None = None,
    modelo: str = "birefnet-general",
    alpha_matting: bool = True,
    post_process: bool = True,
    bgcolor: tuple[int, int, int, int] | None = None,
    session=None,
) -> Image.Image:
    """
    Remove o fundo de uma imagem com alta qualidade.

    Args:
        entrada: Caminho da imagem de entrada
        saida: Caminho para salvar (opcional)
        modelo: Nome do modelo a usar
        alpha_matting: Ativa suavização de bordas (recomendado para alta qualidade)
        post_process: Aplica pós-processamento na máscara
        bgcolor: Cor de fundo (R, G, B, A) - None = transparente
        session: Sessão reutilizável (para processamento em lote)

    Returns:
        Imagem PIL com fundo removido
    """
    entrada = Path(entrada)
    if not entrada.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {entrada}")

    # Carregar imagem
    img = Image.open(entrada).convert("RGB")

    # Criar sessão se não fornecida
    if session is None:
        session = new_session(modelo)

    # Remover fundo com parâmetros de alta qualidade
    output = remove(
        img,
        session=session,
        alpha_matting=alpha_matting,
        alpha_matting_foreground_threshold=270,
        alpha_matting_background_threshold=20,
        alpha_matting_erode_size=11,
        post_process_mask=post_process,
        bgcolor=bgcolor,
    )

    if saida:
        saida = Path(saida)
        saida.parent.mkdir(parents=True, exist_ok=True)
        output.save(saida, "PNG", compress_level=6)  # PNG com compressão balanceada

    return output


def processar_pasta(
    pasta_entrada: Path,
    pasta_saida: Path,
    modelo: str = "birefnet-general",
    extensoes: tuple[str, ...] = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".heic", ".heif"),
) -> int:
    """Processa todas as imagens de uma pasta."""
    pasta_entrada = Path(pasta_entrada)
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)

    arquivos = [
        f for f in pasta_entrada.iterdir()
        if f.suffix.lower() in extensoes and f.is_file()
    ]

    if not arquivos:
        print(f"Nenhuma imagem encontrada em {pasta_entrada}")
        return 0

    print(f"Processando {len(arquivos)} imagem(ns) com modelo '{modelo}'...")
    session = new_session(modelo)

    processados = 0
    for i, arquivo in enumerate(arquivos, 1):
        saida = pasta_saida / f"{arquivo.stem}_sem_fundo.png"
        try:
            remover_fundo(
                arquivo,
                saida,
                modelo=modelo,
                session=session,
            )
            processados += 1
            print(f"  [{i}/{len(arquivos)}] {arquivo.name} -> {saida.name}")
        except Exception as e:
            print(f"  [ERRO] {arquivo.name}: {e}")

    return processados


def main():
    parser = argparse.ArgumentParser(
        description="Remove fundo de imagens com alta qualidade"
    )
    parser.add_argument(
        "entrada",
        nargs="?",
        help="Arquivo ou pasta de imagens",
    )
    parser.add_argument(
        "-o", "--saida",
        help="Arquivo ou pasta de saída (padrão: mesmo nome com sufixo _sem_fundo)",
    )
    parser.add_argument(
        "-m", "--modelo",
        choices=list(MODELOS.keys()),
        default="birefnet-general",
        help=f"Modelo a usar. Padrão: birefnet-general",
    )
    parser.add_argument(
        "--sem-alpha-matting",
        action="store_true",
        help="Desativa alpha matting (mais rápido, bordas menos suaves)",
    )
    parser.add_argument(
        "--sem-post-process",
        action="store_true",
        help="Desativa pós-processamento da máscara",
    )
    parser.add_argument(
        "--listar-modelos",
        action="store_true",
        help="Lista modelos disponíveis e sai",
    )

    args = parser.parse_args()

    if args.listar_modelos:
        print("Modelos disponíveis:\n")
        for nome, desc in MODELOS.items():
            print(f"  {nome:25} - {desc}")
        return

    if not args.entrada:
        parser.error("entrada é obrigatório (ou use --listar-modelos)")

    entrada = Path(args.entrada)
    if not entrada.exists():
        print(f"Erro: '{entrada}' não encontrado.")
        return 1

    if entrada.is_file():
        # Processar arquivo único
        saida = args.saida or entrada.parent / f"{entrada.stem}_sem_fundo.png"
        saida = Path(saida)
        try:
            remover_fundo(
                entrada,
                saida,
                modelo=args.modelo,
                alpha_matting=not args.sem_alpha_matting,
                post_process=not args.sem_post_process,
            )
            print(f"✓ Salvo em: {saida}")
        except Exception as e:
            print(f"Erro: {e}")
            return 1
    else:
        # Processar pasta
        saida = Path(args.saida or str(entrada) + "_output")
        n = processar_pasta(
            entrada,
            saida,
            modelo=args.modelo,
        )
        print(f"\n✓ {n} imagem(ns) processada(s) em {saida}")

    return 0


if __name__ == "__main__":
    exit(main())
