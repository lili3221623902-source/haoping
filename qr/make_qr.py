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

# ---------- A6 打印卡片 ----------
W, H = 1240, 1748
im = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(im)
ctr = lambda t, y, font, fill: d.text(((W - (d.textbbox((0, 0), t, font=font)[2])) / 2, y), t, font=font, fill=fill)

d.rectangle([0, 0, W, 14], fill=BRAND)
lh = 200
lg = logo.resize((int(logo.width * lh / logo.height), lh), Image.LANCZOS)
im.paste(lg, ((W - lg.width) // 2, 82), lg)
ctr("扫码写评价 · 一分钟搞定", 336, f(38, 1), DARK)

side = draw_qr(d, (W - (n + 6) * 12) // 2, 460, 12)
box = [((W - side) // 2 - 26, 434), ((W + side) // 2 + 26, 460 + side + 26)]
d.rounded_rectangle(box, 26, outline=LINE, width=3)

y = 460 + side + 96
ctr("微信扫一扫 / 相机扫码", y, f(32, 1), DARK); y += 80
for t in ["① 打开页面，选好标签生成文案", "② 一键复制，跟着按钮去平台", "③ 到评价框长按粘贴，发出"]:
    ctr(t, y, f(30, 0), GREY); y += 54
d.line([140, H - 148, W - 140, H - 148], fill=LINE, width=3)
ctr("把二维码打印出来，贴在前台 / 工单 / 名片上", H - 112, f(26, 0), GREY)
im.save("扫码卡片.png", dpi=(300, 300))
im.resize((W // 3, H // 3), Image.LANCZOS).save("扫码卡片_预览.png")

# ---------- 1080 方形版 ----------
S = 1080
sq = Image.new("RGB", (S, S), "white")
sd = ImageDraw.Draw(sq)
sctr = lambda t, y, font, fill: sd.text(((S - (sd.textbbox((0, 0), t, font=font)[2])) / 2, y), t, font=font, fill=fill)
sd.rectangle([0, 0, S, 12], fill=BRAND)
slh = 150
slg = logo.resize((int(logo.width * slh / logo.height), slh), Image.LANCZOS)
sq.paste(slg, ((S - slg.width) // 2, 56), slg)
sctr("扫码写评价 · 一分钟搞定", 232, f(29, 1), DARK)
mod, quiet = 14, 3
x0 = (S - (n + quiet * 2) * mod) // 2
y0 = 290
side2 = draw_qr(sd, x0, y0, mod, quiet)
sctr("微信扫一扫 / 相机扫码", y0 + side2 + 26, f(27, 1), DARK)
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
