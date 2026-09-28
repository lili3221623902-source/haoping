# -*- coding: utf-8 -*-
"""生成「口碑文案助手」扫码卡片（可打印）+ 纯二维码两种图。"""
import segno
from PIL import Image, ImageDraw, ImageFont

URL = "https://lili3221623902-source.github.io/koubei/"
BRAND = (255, 106, 61)
DARK = (28, 30, 34)
GREY = (124, 130, 140)
LINE = (232, 234, 238)

FONT = "/System/Library/Fonts/PingFang.ttc"
def f(size, weight=0):
    return ImageFont.truetype(FONT, size, index=weight)

qr = segno.make(URL, error="h")
matrix = list(qr.matrix)
n = len(matrix)

W, H = 1240, 1748
im = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(im)

def center(text, y, font, fill):
    box = d.textbbox((0, 0), text, font=font)
    d.text(((W - (box[2] - box[0])) / 2, y), text, font=font, fill=fill)
    return box[3] - box[1]

# 顶部品牌条
d.rectangle([0, 0, W, 14], fill=BRAND)
center("口碑文案助手", 118, f(76, 4), DARK)
center("扫码，一分钟写好一条走心的顾客评价", 232, f(34, 0), GREY)

# 二维码（模块对齐整数，保证清晰）
MOD, QUIET = 12, 3            # 每个模块像素、静默区模块数
side = (n + QUIET * 2) * MOD
x0, y0 = (W - side) // 2, 420
d.rounded_rectangle([x0 - 26, y0 - 26, x0 + side + 26, y0 + side + 26], 26, outline=LINE, width=3)
for r, row in enumerate(matrix):
    for c, v in enumerate(row):
        if v:
            px = x0 + (c + QUIET) * MOD
            py = y0 + (r + QUIET) * MOD
            d.rectangle([px, py, px + MOD - 1, py + MOD - 1], fill=DARK)

y = y0 + side + 120
center("微信扫一扫 / 相机扫码", y, f(32, 1), DARK)
y += 74
for t in ["① 打开页面，选好标签生成文案", "② 一键复制，跟着按钮去平台", "③ 到评价框长按粘贴，发出"]:
    center(t, y, f(30, 0), GREY)
    y += 52

d.line([140, H - 150, W - 140, H - 150], fill=LINE, width=3)
center("把二维码打印出来，贴在前台 / 工单 / 名片上", H - 118, f(26, 0), GREY)

im.save("扫码卡片.png", dpi=(300, 300))
im.resize((W // 3, H // 3), Image.LANCZOS).save("扫码卡片_预览.png")

# 纯二维码（贴到设计稿里用）
pure = Image.new("RGB", ((n + 8) * 24, (n + 8) * 24), "white")
pd = ImageDraw.Draw(pure)
for r, row in enumerate(matrix):
    for c, v in enumerate(row):
        if v:
            pd.rectangle([(c + 4) * 24, (r + 4) * 24, (c + 5) * 24 - 1, (r + 5) * 24 - 1], fill="black")
pure.save("二维码_纯图.png", dpi=(300, 300))

# 方形版：发朋友圈 / 群 / 贴在工单上
S = 1080
sq = Image.new("RGB", (S, S), "white")
sd = ImageDraw.Draw(sq)
sd.rectangle([0, 0, S, 12], fill=BRAND)
tf = f(58, 4)
box = sd.textbbox((0, 0), "口碑文案助手", font=tf)
sd.text(((S - (box[2] - box[0])) / 2, 66), "口碑文案助手", font=tf, fill=DARK)
sub = pif = f(26, 0)
box = sd.textbbox((0, 0), "扫码写评价 · 一分钟搞定", font=sub)
sd.text(((S - (box[2] - box[0])) / 2, 146), "扫码写评价 · 一分钟搞定", font=sub, fill=GREY)
MOD2 = 15
side2 = (n + 6) * MOD2
sx = (S - side2) // 2
sy = 226
for r, row in enumerate(matrix):
    for c, v in enumerate(row):
        if v:
            px, py = sx + (c + 3) * MOD2, sy + (r + 3) * MOD2
            sd.rectangle([px, py, px + MOD2 - 1, py + MOD2 - 1], fill=DARK)
box = sd.textbbox((0, 0), "微信扫一扫 / 相机扫码", font=f(26, 1))
sd.text(((S - (box[2] - box[0])) / 2, sy + side2 + 22), "微信扫一扫 / 相机扫码", font=f(26, 1), fill=DARK)
sq.resize((S // 2, S // 2), Image.LANCZOS).save("方形版_预览.png")
sq.save("方形版_1080.png", dpi=(300, 300))
print("URL:", URL, "| 模块数:", n, "| 版本:", qr.version)
print("卡片尺寸: %dx%d (A6 300dpi)" % (W, H))
