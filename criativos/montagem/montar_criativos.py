from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).parent
BASES = ROOT.parent / "imagens-base-gemini"
OUT = ROOT.parent / "finais"
OUT.mkdir(exist_ok=True)
W = H = 1080
NAVY = "#203247"
TEAL = "#147C78"
CREAM = "#FFFDF8"
MUTED = "#53636A"
GOLD = "#EAB47B"

FONT = Path(r"C:\Windows\Fonts")
def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(FONT / name), size)

ASSETS = [
    ("imagem-base-01.jfif", "Por onde começar\nno teclado?", "Um guia em PDF com os primeiros passos."),
    ("imagem-base-02.jfif", "Aprende por\nseis etapas", "Notas, dedos, ritmo e uma melodia original."),
    ("imagem-base-03.jfif", "Encontra as notas\npelo padrão", "As teclas pretas ajudam a localizar o Dó."),
    ("imagem-base-04.jfif", "Começa com dedos\ne ritmo", "Pratica uma nota de cada vez."),
]
OUTPUT_NAMES = [
    "criativo-01-primeiros-passos.png",
    "criativo-02-seis-etapas.png",
    "criativo-03-localizar-notas.png",
    "criativo-04-dedos-e-ritmo.png",
]

def fit_cover(src, size):
    im = Image.open(src).convert("RGB")
    im.thumbnail(size, Image.Resampling.LANCZOS)
    return im

def main():
    cover = fit_cover(ROOT.parents[1] / "capas" / "capa-piano-do-zero.png", (160, 240))
    for index, (base_name, headline, support) in enumerate(ASSETS, 1):
        base = Image.open(BASES / base_name).convert("RGB")
        # Square crop and resize to the requested delivery size.
        side = min(base.width, base.height)
        left = (base.width - side) // 2
        top = (base.height - side) // 2
        im = base.crop((left, top, left + side, top + side)).resize((W, H), Image.Resampling.LANCZOS).convert("RGBA")

        # Light translucent text panel, sized to stay inside the quiet upper-left area.
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rounded_rectangle((42, 42, 764, 465), radius=30, fill=(255, 253, 248, 244), outline=(20, 124, 120, 90), width=2)
        # Small product category label.
        od.rounded_rectangle((74, 72, 312, 112), radius=18, fill=TEAL)
        od.text((92, 81), "GUIA DE INICIAÇÃO", font=font(18, True), fill=CREAM)
        # Distinct short headline and supporting line.
        od.multiline_text((74, 132), headline, font=font(52, True), fill=NAVY, spacing=4, stroke_width=0)
        od.text((77, 287), support, font=font(24), fill=MUTED)
        im = Image.alpha_composite(im, overlay)

        # Bottom information card covers the generator's corner mark and carries the real price.
        card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((42, 782, 774, 1035), radius=26, fill=(255, 253, 248, 245), outline=(20, 124, 120, 75), width=2)
        cd.text((76, 811), "Piano do Zero", font=font(29, True), fill=NAVY)
        cd.text((78, 852), "Guia introdutório em PDF", font=font(19), fill=MUTED)
        cd.rounded_rectangle((76, 892, 300, 982), radius=22, fill=TEAL)
        cd.text((188, 937), "2.500 Kz", font=font(32, True), fill=CREAM, anchor="mm")
        cd.rounded_rectangle((322, 892, 520, 982), radius=22, fill=NAVY)
        cd.text((421, 937), "Saiba mais", font=font(22, True), fill=CREAM, anchor="mm")
        im = Image.alpha_composite(im, card)

        # Add the authentic product cover as a small mockup at the lower-right corner.
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle((817, 684, 1034, 1044), radius=25, fill=(20, 32, 45, 85))
        im = Image.alpha_composite(im, shadow.filter(ImageFilter.GaussianBlur(14)))
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fd = ImageDraw.Draw(frame)
        fd.rounded_rectangle((812, 679, 1030, 1038), radius=24, fill=(255, 253, 248, 255), outline=(255,255,255,240), width=4)
        im = Image.alpha_composite(im, frame)
        im.paste(cover, (841, 739))

        # Fine outer keyline helps each asset sit well on a feed background.
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((10, 10, 1069, 1069), radius=25, outline=(255,255,255,210), width=3)
        out = OUT / OUTPUT_NAMES[index - 1]
        im.convert("RGB").save(out, "PNG", optimize=True)
        print(out)

    # A compact contact sheet for reviewing the four finished square assets together.
    thumbs = []
    for i in range(1, 5):
        pic = Image.open(OUT / OUTPUT_NAMES[i - 1]).convert("RGB")
        thumbs.append(pic.resize((540, 540), Image.Resampling.LANCZOS))
    sheet = Image.new("RGB", (1100, 1100), "#E8ECF1")
    sheet.paste(thumbs[0], (10, 10)); sheet.paste(thumbs[1], (550, 10))
    sheet.paste(thumbs[2], (10, 550)); sheet.paste(thumbs[3], (550, 550))
    sheet.save(OUT / "visao-geral-quatro-criativos.png", "PNG", optimize=True)

if __name__ == "__main__":
    main()
