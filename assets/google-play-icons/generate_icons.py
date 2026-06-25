from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

OUT = Path(__file__).resolve().parent
SCALE = 4
SIZE = 512
CANVAS = SIZE * SCALE


def font(size, bold=True):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size * SCALE)
    return ImageFont.load_default()


def rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(size, colors, vertical=True):
    axis = Image.new("RGB", (1, size) if vertical else (size, 1), colors[0])
    px = axis.load()
    stops = len(colors) - 1
    for i in range(size):
        p = i / max(size - 1, 1)
        seg = min(int(p * stops), stops - 1)
        local = p * stops - seg
        color = lerp(colors[seg], colors[seg + 1], local)
        if vertical:
            px[0, i] = color
        else:
            px[i, 0] = color
    return axis.resize((size, size), Image.Resampling.BICUBIC)


def rounded_mask(radius):
    mask = Image.new("L", (CANVAS, CANVAS), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, CANVAS - 1, CANVAS - 1], radius=radius * SCALE, fill=255)
    return mask


def icon_base(colors):
    bg = gradient(CANVAS, [rgb(c) for c in colors], vertical=False)
    mask = rounded_mask(112)
    base = Image.new("RGB", (CANVAS, CANVAS), rgb("#0f172a"))
    base.paste(bg, (0, 0), mask)
    return base


def draw_shadow(draw, box, radius=42, offset=18, fill=(0, 0, 0, 80)):
    x1, y1, x2, y2 = [v * SCALE for v in box]
    for i in range(12, 0, -1):
        alpha = int(fill[3] * i / 12)
        spread = i * SCALE
        layer = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle(
            [x1 - spread, y1 + offset * SCALE - spread, x2 + spread, y2 + offset * SCALE + spread],
            radius=(radius + i) * SCALE,
            fill=(fill[0], fill[1], fill[2], alpha),
        )
        draw._image.alpha_composite(layer)


def save_icon(img, name):
    img = img.resize((SIZE, SIZE), Image.Resampling.LANCZOS).convert("RGB")
    img.save(OUT / name, optimize=True, compress_level=9)


def car(draw, cx, cy, scale=1.0, color="#ffffff", dark="#0f172a"):
    c = rgb(color)
    d = rgb(dark)
    s = SCALE * scale
    def p(v): return int(v * s)
    x = int(cx * SCALE)
    y = int(cy * SCALE)
    draw.line([(x - p(86), y + p(12)), (x - p(58), y - p(38)), (x + p(58), y - p(38)), (x + p(86), y + p(12))], fill=c, width=p(16), joint="curve")
    draw.rounded_rectangle([x - p(110), y + p(12), x + p(110), y + p(66)], radius=p(22), fill=c)
    draw.ellipse([x - p(83), y + p(46), x - p(45), y + p(84)], fill=d)
    draw.ellipse([x + p(45), y + p(46), x + p(83), y + p(84)], fill=d)


def shield(draw, cx, cy, scale=1.0, outline="#ffffff", fill=None):
    s = SCALE * scale
    def p(v): return int(v * s)
    x = int(cx * SCALE)
    y = int(cy * SCALE)
    pts = [(x, y - p(94)), (x + p(78), y - p(62)), (x + p(78), y + p(12)), (x, y + p(96)), (x - p(78), y + p(12)), (x - p(78), y - p(62))]
    draw.polygon(pts, fill=rgb(fill) if fill else None, outline=rgb(outline))
    draw.line(pts + [pts[0]], fill=rgb(outline), width=p(15), joint="curve")


def lightning(draw, cx, cy, scale=1.0, color="#ffffff"):
    s = SCALE * scale
    def p(v): return int(v * s)
    x = int(cx * SCALE)
    y = int(cy * SCALE)
    pts = [(x + p(22), y - p(86)), (x - p(48), y + p(8)), (x - p(3), y + p(8)), (x - p(24), y + p(86)), (x + p(52), y - p(22)), (x + p(6), y - p(22))]
    draw.polygon(pts, fill=rgb(color))


def document(draw, cx, cy, scale=1.0, paper="#ffffff", accent="#7c3aed"):
    s = SCALE * scale
    def p(v): return int(v * s)
    x = int(cx * SCALE)
    y = int(cy * SCALE)
    draw.rounded_rectangle([x - p(58), y - p(78), x + p(58), y + p(86)], radius=p(12), fill=rgb(paper))
    draw.polygon([(x + p(20), y - p(78)), (x + p(58), y - p(40)), (x + p(20), y - p(40))], fill=rgb("#e2e8f0"))
    draw.ellipse([x - p(28), y - p(38), x + p(28), y + p(18)], fill=rgb(accent))
    draw.arc([x - p(42), y + p(10), x + p(42), y + p(72)], 200, 340, fill=rgb(accent), width=p(12))
    draw.line([(x - p(31), y + p(50)), (x + p(34), y + p(50))], fill=rgb("#64748b"), width=p(8))


def sparkle(draw, cx, cy, scale=1.0, color="#fbbf24"):
    s = SCALE * scale
    def p(v): return int(v * s)
    x = int(cx * SCALE)
    y = int(cy * SCALE)
    pts = [(x, y - p(44)), (x + p(13), y - p(13)), (x + p(44), y), (x + p(13), y + p(13)), (x, y + p(44)), (x - p(13), y + p(13)), (x - p(44), y), (x - p(13), y - p(13))]
    draw.polygon(pts, fill=rgb(color))


def check(draw, cx, cy, scale=1.0, color="#22c55e"):
    s = SCALE * scale
    def p(v): return int(v * s)
    x = int(cx * SCALE)
    y = int(cy * SCALE)
    draw.line([(x - p(62), y), (x - p(18), y + p(44)), (x + p(72), y - p(58))], fill=rgb(color), width=p(24), joint="curve")


def variant_flowforge():
    img = icon_base(["#0f172a", "#0369a1", "#22c55e"])
    overlay = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle([74*SCALE, 74*SCALE, 438*SCALE, 438*SCALE], radius=88*SCALE, fill=(255, 255, 255, 28))
    car(d, 256, 302, 1.05, "#ffffff", "#0f172a")
    shield(d, 256, 154, 0.72, "#ffffff", fill="#0f172a")
    lightning(d, 256, 159, 0.46, "#22c55e")
    document(d, 365, 157, 0.45, "#ffffff", "#0ea5e9")
    check(d, 284, 383, 0.58, "#22c55e")
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    save_icon(img, "flowforge-apps-google-play.png")


def variant_stack():
    img = icon_base(["#020617", "#1d4ed8", "#7c3aed"])
    overlay = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    tiles = [
        (80, 112, 232, 264, "#14b8a6"),
        (280, 88, 432, 240, "#2563eb"),
        (180, 270, 332, 422, "#db2777"),
    ]
    for box in tiles:
        d.rounded_rectangle([v*SCALE for v in box[:4]], radius=34*SCALE, fill=rgb(box[4]) + (255,))
    car(d, 156, 191, 0.58, "#ffffff", "#0f172a")
    shield(d, 356, 164, 0.44, "#ffffff")
    lightning(d, 356, 168, 0.30, "#ffffff")
    document(d, 256, 346, 0.46, "#ffffff", "#db2777")
    check(d, 375, 363, 0.48, "#22c55e")
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    save_icon(img, "kasyanov-stack-google-play.png")


def variant_secureflow():
    img = icon_base(["#111827", "#1d4ed8", "#0891b2"])
    overlay = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    shield(d, 256, 238, 1.18, "#ffffff", fill="#0f172a")
    d.arc([86*SCALE, 143*SCALE, 426*SCALE, 355*SCALE], 190, 342, fill=rgb("#38bdf8"), width=18*SCALE)
    d.ellipse([108*SCALE, 256*SCALE, 146*SCALE, 294*SCALE], fill=rgb("#ffffff"))
    d.ellipse([370*SCALE, 174*SCALE, 408*SCALE, 212*SCALE], fill=rgb("#ffffff"))
    lightning(d, 256, 222, 0.72, "#38bdf8")
    check(d, 254, 333, 0.72, "#22c55e")
    sparkle(d, 376, 114, 0.55, "#fbbf24")
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    save_icon(img, "secureflow-dev-google-play.png")


def variant_mk_lab():
    img = icon_base(["#0f172a", "#155e75", "#f59e0b"])
    overlay = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle([86*SCALE, 86*SCALE, 426*SCALE, 426*SCALE], radius=82*SCALE, fill=(2, 6, 23, 210), outline=rgb("#38bdf8") + (255,), width=10*SCALE)
    d.text((256*SCALE, 242*SCALE), "MK", anchor="mm", font=font(132), fill=rgb("#f8fafc"))
    d.text((118*SCALE, 248*SCALE), "<", anchor="mm", font=font(92), fill=rgb("#38bdf8"))
    d.text((394*SCALE, 248*SCALE), ">", anchor="mm", font=font(92), fill=rgb("#22c55e"))
    for x, color in [(167, "#14b8a6"), (256, "#2563eb"), (345, "#f59e0b")]:
        d.ellipse([(x-18)*SCALE, 364*SCALE, (x+18)*SCALE, 400*SCALE], fill=rgb(color))
    check(d, 256, 143, 0.50, "#22c55e")
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    save_icon(img, "mk-product-lab-google-play.png")


def variant_triplecheck():
    img = icon_base(["#020617", "#0f766e", "#be185d"])
    overlay = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.ellipse([70*SCALE, 70*SCALE, 442*SCALE, 442*SCALE], outline=rgb("#38bdf8"), width=14*SCALE)
    d.ellipse([97*SCALE, 97*SCALE, 415*SCALE, 415*SCALE], outline=(255, 255, 255, 60), width=4*SCALE)
    d.rounded_rectangle([116*SCALE, 128*SCALE, 218*SCALE, 230*SCALE], radius=26*SCALE, fill=rgb("#14b8a6"))
    d.rounded_rectangle([294*SCALE, 128*SCALE, 396*SCALE, 230*SCALE], radius=26*SCALE, fill=rgb("#2563eb"))
    d.rounded_rectangle([205*SCALE, 276*SCALE, 307*SCALE, 378*SCALE], radius=26*SCALE, fill=rgb("#db2777"))
    car(d, 167, 190, 0.35, "#ffffff", "#0f172a")
    shield(d, 345, 184, 0.31, "#ffffff")
    lightning(d, 345, 187, 0.20, "#ffffff")
    document(d, 256, 327, 0.27, "#ffffff", "#db2777")
    check(d, 334, 337, 0.58, "#22c55e")
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    save_icon(img, "triplecheck-apps-google-play.png")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    variant_flowforge()
    variant_stack()
    variant_secureflow()
    variant_mk_lab()
    variant_triplecheck()


if __name__ == "__main__":
    main()
