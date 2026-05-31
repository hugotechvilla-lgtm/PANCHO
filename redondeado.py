from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import numpy as np

# TAMAÑO DE TICKET
ancho, alto = 600, 420
radio = 30  # Radio de las esquinas

# DEGRADADO: #A8E6FF (arriba) → #001020 (abajo)
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

color_top = hex_to_rgb("#00D4FF")
color_bot = hex_to_rgb("#5B0FBE")

gradient = np.zeros((alto, ancho, 3), dtype=np.uint8)
for y in range(alto):
    t = y / alto
    r = int(color_top[0] + (color_bot[0] - color_top[0]) * t)
    g = int(color_top[1] + (color_bot[1] - color_top[1]) * t)
    b = int(color_top[2] + (color_bot[2] - color_top[2]) * t)
    gradient[y, :] = [r, g, b]

ticket = Image.fromarray(gradient, "RGB").convert("RGBA")

# ✅ MÁSCARA PARA REDONDEAR EL FONDO
mask = Image.new("L", (ancho, alto), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.rounded_rectangle([(0, 0), (ancho-1, alto-1)], radius=radio, fill=255)
ticket.putalpha(mask)

draw = ImageDraw.Draw(ticket)

# ✅ MARCO REDONDEADO
draw.rounded_rectangle([(5, 5), (ancho-6, alto-6)], radius=radio, outline="black", width=3)

# FUENTES
try:
    font_title = ImageFont.truetype("PANCHO6.otf", 35)
    font = ImageFont.truetype("PANCHO6.otf", 20)
except:
    font_title = ImageFont.load_default()
    font = ImageFont.load_default()

# LOGO (MARCA DE AGUA)
try:
    logo = Image.open("logo.png").convert("RGBA")
    nuevo_ancho = 400
    nuevo_alto = int(logo.height * (nuevo_ancho / logo.width))
    logo = logo.resize((nuevo_ancho, nuevo_alto))
    alpha = logo.split()[3].point(lambda p: p * 0.1)
    logo.putalpha(alpha)
    pos_x = (ancho - nuevo_ancho) // 2
    pos_y = (alto - nuevo_alto) // 2
    ticket.paste(logo, (pos_x, pos_y), logo)
except:
    print("⚠️ logo.png no encontrado, continuando sin logo...")

# TÍTULO CENTRADO
titulo = "PANCHO"
bbox = draw.textbbox((0, 0), titulo, font=font_title)
pos_x = (ancho - (bbox[2] - bbox[0])) // 2
draw.text((pos_x, 30), titulo, font=font_title, fill="black")

# DATOS DE COMPRA
y = 100
espaciado = 55
lineas = [
    "CLIENTE: HUGO ",
    f"FECHA: {datetime.now().strftime('%d/%m/%Y')}",
    "CONCEPTO: CERVEZAS, MICHELADAS",
]
for linea in lineas:
    draw.text((50, y), linea, font=font, fill="black")
    y += espaciado

draw.text((ancho - 250, y), "TOTAL: 54.000", font=font, fill="black")

# MENSAJES INFERIORES CENTRADOS
for mensaje, pos_y in [("GRACIAS POR SU COMPRA", 350), ("301 343 27 75 NEQUI", 380)]:
    bbox = draw.textbbox((0, 0), mensaje, font=font)
    pos_x = (ancho - (bbox[2] - bbox[0])) // 2
    draw.text((pos_x, pos_y), mensaje, font=font, fill="black")

# ✅ GUARDAR EN PNG (necesario para preservar transparencia)
ticket.save("ticket.png")
print("✅ Ticket redondeado generado con éxito como 'ticket.png'")