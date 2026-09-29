import os
import sys
import datetime
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

print("Iniciando script...")

# ==========================================
# 1. URLS CSV DE GOOGLE SHEETS
# ==========================================
URL_MENU = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR6MjZoIrmKCILJjp6Izz0V_bWS-S7EZOVtv6y4rxC5sCIBIMvXChCJMfJY0GofubmujiX9G8jLSVv_/pub?gid=0&single=true&output=csv"
URL_EXTRA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR6MjZoIrmKCILJjp6Izz0V_bWS-S7EZOVtv6y4rxC5sCIBIMvXChCJMfJY0GofubmujiX9G8jLSVv_/pub?gid=1658913824&single=true&output=csv"
URL_AVISOS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR6MjZoIrmKCILJjp6Izz0V_bWS-S7EZOVtv6y4rxC5sCIBIMvXChCJMfJY0GofubmujiX9G8jLSVv_/pub?gid=1611904814&single=true&output=csv"
try:
    # ==========================================
    # 2. CONFIGURACIÓN DE PANTALLA Y COLORES
    # ==========================================
    ANCHO, ALTO = 400, 300
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    ROJO = (220, 20, 60)
    AMARILLO = (255, 215, 0)

    img = Image.new("RGB", (ANCHO, ALTO), BLANCO)
    draw = ImageDraw.Draw(img)

    # Cargar fuentes del sistema
    try:
        font_header = ImageFont.truetype("arial.ttf", 16)
        font_sec = ImageFont.truetype("arialbd.ttf", 13)
        font_text = ImageFont.truetype("arial.ttf", 12)
        font_bold = ImageFont.truetype("arialbd.ttf", 12)
    except:
        font_header = font_sec = font_text = font_bold = ImageFont.load_default()

    # ==========================================
    # 3. FECHA Y DÍA DE LA SEMANA
    # ==========================================
    hoy = datetime.date.today()
    fecha_str = hoy.strftime("%Y-%m-%d")

    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dia_nombre = dias_semana[hoy.weekday()]

    # Cabecera superior
    draw.rectangle([0, 0, ANCHO, 35], fill=AMARILLO)
    draw.text((12, 8), f"HOY: {dia_nombre}, {hoy.strftime('%d/%m/%Y')}", fill=NEGRO, font=font_header)

    # ==========================================
    # 4. LEER Y DIBUJAR MENÚ
    # ==========================================
    print("Leyendo Menú...")
    draw.text((12, 45), "MENÚ DEL COLE", fill=ROJO, font=font_sec)
    draw.line([(12, 63), (185, 63)], fill=ROJO, width=2)

    p1, p2, postre = "Sin datos", "Sin datos", "Sin datos"
    if "http" in URL_MENU:
        try:
            df_menu = pd.read_csv(URL_MENU)
            fila_hoy = df_menu[df_menu["Fecha"].astype(str) == fecha_str]
            if not fila_hoy.empty:
                p1 = str(fila_hoy.iloc[0]["Primer_Plato"])
                p2 = str(fila_hoy.iloc[0]["Segundo_Plato"])
                postre = str(fila_hoy.iloc[0]["Postre"])
        except Exception as e:
            print(f"Error descargando Menú: {e}")
            p1 = "Error cargando menú"

    draw.text((12, 72), "1º Plato:", fill=NEGRO, font=font_bold)
    draw.text((12, 88), p1[:25], fill=NEGRO, font=font_text)

    draw.text((12, 112), "2º Plato:", fill=NEGRO, font=font_bold)
    draw.text((12, 128), p2[:25], fill=NEGRO, font=font_text)

    draw.text((12, 152), "Postre:", fill=NEGRO, font=font_bold)
    draw.text((12, 168), postre[:25], fill=NEGRO, font=font_text)

    # Divisora vertical
    draw.line([(195, 45), (195, 205)], fill=(200, 200, 200), width=1)

    # ==========================================
    # 5. LEER Y DIBUJAR EXTRAESCOLARES
    # ==========================================
    print("Leyendo Extraescolares...")
    draw.text((205, 45), "EXTRAESCOLARES", fill=NEGRO, font=font_sec)
    draw.line([(205, 63), (388, 63)], fill=NEGRO, width=2)

    hijos = ["Em", "Noah", "Gael"]
    pos_y = 72

    if "http" in URL_EXTRA:
        try:
            df_extra = pd.read_csv(URL_EXTRA)
            df_hoy_extra = df_extra[df_extra["Dia"].astype(str).str.strip().str.lower() == dia_nombre.lower()]
            
            for hijo in hijos:
                act_hijo = df_hoy_extra[df_hoy_extra["Hijo"].astype(str).str.strip().str.lower() == hijo.lower()]
                if not act_hijo.empty:
                    act_text = f"{act_hijo.iloc[0]['Actividad']} ({act_hijo.iloc[0]['Horario']})"
                else:
                    act_text = "Sin actividad"
                    
                draw.text((205, pos_y), f"• {hijo}:", fill=NEGRO, font=font_bold)
                draw.text((255, pos_y), act_text[:18], fill=NEGRO, font=font_text)
                pos_y += 30
        except Exception as e:
            print(f"Error descargando Extraescolares: {e}")
            draw.text((205, 72), "Error extraescolares", fill=NEGRO, font=font_text)

    # ==========================================
    # 6. LEER Y DIBUJAR AVISOS
    # ==========================================
    print("Leyendo Avisos...")
    draw.rectangle([10, 215, 390, 288], outline=ROJO, width=2)
    draw.rectangle([10, 215, 390, 235], fill=ROJO)
    draw.text((15, 218), "NOTAS IMPORTANTES", fill=BLANCO, font=font_sec)

    av1, av2 = "", ""
    if "http" in URL_AVISOS:
        try:
            df_avisos = pd.read_csv(URL_AVISOS)
            fila_av = df_avisos[df_avisos["Fecha"].astype(str) == fecha_str]
            if not fila_av.empty:
                av1 = str(fila_av.iloc[0]["Aviso_1"]) if pd.notna(fila_av.iloc[0]["Aviso_1"]) else ""
                av2 = str(fila_av.iloc[0]["Aviso_2"]) if pd.notna(fila_av.iloc[0]["Aviso_2"]) else ""
        except Exception as e:
            print(f"Error descargando Avisos: {e}")
            av1 = "Sin avisos"

    if av1: draw.text((18, 243), f"• {av1[:45]}", fill=NEGRO, font=font_text)
    if av2: draw.text((18, 263), f"• {av2[:45]}", fill=NEGRO, font=font_text)

    # Guardar imagen
    img.save("pantalla.bmp")
    print("¡ÉXITO! Imagen 'pantalla.bmp' generada correctamente en la carpeta.")

except Exception as err:
    print(f"ERROR FATAL: {err}", file=sys.stderr)