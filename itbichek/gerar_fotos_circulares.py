"""
gerar_fotos_circulares.py
--------------------------
Lê diego.jpg e gustavo.jpg da pasta img/,
recorta o rosto em círculo e salva as versões finais no mesmo lugar.

Como usar:
  1. Coloque diego.jpg e gustavo.jpg dentro da pasta  itbichek/img/
  2. Execute:  python gerar_fotos_circulares.py
  3. As fotos serão sobrescritas com as versões circulares prontas para o site.

Requisito:  pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFilter
import os

# --- Configuração de recorte por foto ---
# face_box = (left%, top%, right%, bottom%)  — porcentagem da imagem original
# Ajuste se o rosto não aparecer centralizado corretamente.
CONFIGS = {
    "diego.jpg": {
        "face_box": (0.10, 0.03, 0.90, 0.75),   # retrato de gravata azul
        "output_size": 400,
    },
    "gustavo.jpg": {
        "face_box": (0.15, 0.02, 0.85, 0.65),   # retrato de gravata bordô
        "output_size": 400,
    },
}

IMG_DIR = os.path.join(os.path.dirname(__file__), "img")


def crop_circle(img_path, face_box, output_size):
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size

    # Recorta a região do rosto
    l = int(face_box[0] * w)
    t = int(face_box[1] * h)
    r = int(face_box[2] * w)
    b = int(face_box[3] * h)

    # Garante quadrado perfeito (centraliza)
    side = min(r - l, b - t)
    cx = (l + r) // 2
    cy = (t + b) // 2
    l = cx - side // 2
    t = cy - side // 2
    r = l + side
    b = t + side

    face = img.crop((l, t, r, b)).resize((output_size, output_size), Image.LANCZOS)

    # Máscara circular com borda suave
    mask = Image.new("L", (output_size, output_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, output_size - 1, output_size - 1), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1))

    # Aplica máscara
    result = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))
    result.paste(face, (0, 0))
    result.putalpha(mask)

    # Salva como JPEG com fundo branco (compatível com todos os browsers)
    bg = Image.new("RGB", (output_size, output_size), (255, 255, 255))
    bg.paste(result, mask=result.split()[3])
    return bg


def main():
    for filename, cfg in CONFIGS.items():
        path = os.path.join(IMG_DIR, filename)
        if not os.path.exists(path):
            print(f"  ⚠️  Arquivo não encontrado: {path} — pule e adicione depois.")
            continue

        print(f"  ✂️  Processando {filename}...")
        result = crop_circle(path, cfg["face_box"], cfg["output_size"])
        result.save(path, "JPEG", quality=92, optimize=True)
        print(f"  ✅  {filename} salvo ({cfg['output_size']}×{cfg['output_size']}px)")

    print("\nPronto! Faça o deploy normalmente — as fotos já estão na pasta img/.")


if __name__ == "__main__":
    main()
