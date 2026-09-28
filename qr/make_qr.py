# -*- coding: utf-8 -*-
"""「好惠修 · 口碑文案助手」扫码物料：可打印卡片(A6) + 方形版(1080) + 纯二维码。"""
import segno
from PIL import Image, ImageDraw, ImageFont

URL  = "https://lili3221623902-source.github.io/koubei/"
SHOP = "好惠修 家庭维修"
LOGO = "../assets/logo-on-light.png"

# 色板取自 好惠修 logo：主橙 / 亮橙 / 深蓝黑
BRAND = (243, 88, 3)
BRAND2 = (252, 154, 43)
DARK  = (27, 33, 47)
GREY  = (120, 130, 145)
LINE  = (231, 234, 240)

FONT = "/System/Library/Fonts/PingFang.ttc"
f = lambda size, weight=0: ImageFont.truetype(FONT, size, index=weight)

qr = segno.make(URL, error="h")
matrix = list(qr.matrix)
n = len(matrix)
logo = Image.open(LOGO)

def draw_qr(d, x0, y0, mod, quiet=3):
    for r, row in enumerate(matrix):
        for c, v in enumerate(row):
            if v:
                px, py = x0 + (c + quiet) * mod, y0 + (r + quiet) * mod
                d.rectangle([px, py, px + mod - 1, py + mod - 1], fill=DARK)
    return (n + quiet * 2) * mod

# ---------- A6 打印卡片：只有 logo + 二维码 ----------
W, H = 1240, 1748
im = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(im)
d.rectangle([0, 0, W, 14], fill=BRAND)

lh = 230
lg = logo.resize((int(logo.width * lh / logo.height), lh), Image.LANCZOS)
im.paste(lg, ((W - lg.width) // 2, 205), lg)

SIDE = draw_qr(d, (W - (n + 6) * 18) // 2, 565, 18)
d.rounded_rectangle([(W - SIDE) // 2 - 30, 535, (W + SIDE) // 2 + 30, 565 + SIDE + 30], 30, outline=LINE, width=3)
im.save("扫码卡片.png", dpi=(300, 300))
im.resize((W // 3, H // 3), Image.LANCZOS).save("扫码卡片_预览.png")

# ---------- 1080 方形版：只有 logo + 二维码 ----------
S = 1080
sq = Image.new("RGB", (S, S), "white")
sd = ImageDraw.Draw(sq)
sd.rectangle([0, 0, S, 12], fill=BRAND)

slh = 150
slg = logo.resize((int(logo.width * slh / logo.height), slh), Image.LANCZOS)
sq.paste(slg, ((S - slg.width) // 2, 84), slg)

SIDE2 = draw_qr(sd, (S - (n + 6) * 14) // 2, 304, 14)
sd.rounded_rectangle([(S - SIDE2) // 2 - 26, 278, (S + SIDE2) // 2 + 26, 304 + SIDE2 + 26], 26, outline=LINE, width=3)
sq.resize((S // 2, S // 2), Image.LANCZOS).save("方形版_预览.png")
sq.save("方形版_1080.png", dpi=(300, 300))

# ---------- 纯二维码 ----------
pure = Image.new("RGB", ((n + 8) * 24, (n + 8) * 24), "white")
pd = ImageDraw.Draw(pure)
for r, row in enumerate(matrix):
    for c, v in enumerate(row):
        if v:
            pd.rectangle([(c + 4) * 24, (r + 4) * 24, (c + 5) * 24 - 1, (r + 5) * 24 - 1], fill="black")
pure.save("二维码_纯图.png", dpi=(300, 300))
print("URL:", URL, "| 模块:", n, "| 版本:", qr.version)
