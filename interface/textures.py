"""Funções para criar texturas visuais (peças, tabuleiro)."""

import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageFont

from .styles import THEME, FONTS, TILE_SIZE, BOARD_PADDING, _adjust_color_brightness

def _get_pil_font(font_tuple):
    """Converte uma tupla de fonte Tkinter para um objeto de fonte PIL."""
    try:
        name, size, *style = font_tuple
        # Tenta encontrar o arquivo .ttf correspondente (pode precisar de ajuste)
        # Para Windows, pode ser necessário buscar em C:\Windows\Fonts
        # ou fornecer o caminho completo se não estiver no padrão.
        # Exemplo simplificado:
        font_path = f"{name.replace(' ', '')}.ttf" # Suposição comum
        if "bold" in style:
            font_path = f"{name.replace(' ', '')}bd.ttf" # Suposição para negrito
            
        # Ajuste para fontes comuns como Segoe UI
        if name == "Segoe UI":
            font_path = "segoeui.ttf"
            if "bold" in style:
                font_path = "segoeuib.ttf"

        # Carrega a fonte usando o caminho
        return ImageFont.truetype(font_path, size)

    except IOError:
        print(f"Aviso: Fonte '{name}' não encontrada. Usando fonte padrão.")
        # Fallback para fonte padrão se não encontrar
        return ImageFont.load_default()
    except Exception as e:
        print(f"Erro ao carregar fonte '{name}': {e}. Usando fonte padrão.")
        return ImageFont.load_default()

def create_tile_textures():
    """Cria texturas realistas para as peças do puzzle (números 1-8)."""
    tile_images = {}
    img_size = TILE_SIZE + 8  # Tamanho com margem para sombra

    for i in range(1, 9):
        img = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        wood_color = THEME["tile"]
        draw.rectangle([4, 4, img_size - 4, img_size - 4], fill=wood_color)
        
        # Veios simulados
        for y in range(4, img_size - 4, 4):
            line_color = _adjust_color_brightness(wood_color, -10 - (y % 20))
            draw.line([4, y, img_size - 4, y], fill=line_color, width=1)
            
        border_color = _adjust_color_brightness(wood_color, -40)
        draw.rectangle([4, 4, img_size - 4, img_size - 4], outline=border_color, width=2)
        
        # Sombra
        shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rectangle([6, 6, img_size - 2, img_size - 2], fill=(0, 0, 0, 50))
        shadow = shadow.filter(ImageFilter.GaussianBlur(3))
        img_with_shadow = Image.alpha_composite(shadow, img)
        
        # Número
        draw = ImageDraw.Draw(img_with_shadow)
        text_font = _get_pil_font(FONTS["tile"])
        text_color = THEME["tile_text"]
        # Sombra do texto (outline simples)
        for offset_x, offset_y in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            draw.text((img_size // 2 + offset_x, img_size // 2 + offset_y),
                      str(i), fill="#ffffff", anchor="mm", font=text_font)
        # Texto principal
        draw.text((img_size // 2, img_size // 2), str(i), fill=text_color, 
                  anchor="mm", font=text_font)
            
        tile_images[i] = ImageTk.PhotoImage(img_with_shadow)
        
    return tile_images

def create_board_texture():
    """Cria uma textura de madeira para o fundo do tabuleiro."""
    board_size = 3 * TILE_SIZE + 2 * BOARD_PADDING
    board_img = Image.new('RGB', (board_size, board_size), THEME["board_bg"])
    draw = ImageDraw.Draw(board_img)

    # Veios simulados
    for y in range(0, board_size, 3):
        for x in range(0, board_size, 80):
            width = np.random.randint(30, 70)
            line_color = _adjust_color_brightness(THEME["board_bg"], 5 + (y % 15))
            draw.line([x, y, x + width, y], fill=line_color, width=2)
            
    # Linhas de grade (sutis)
    for i in range(1, 3):
        pos = BOARD_PADDING + i * TILE_SIZE
        grid_color = _adjust_color_brightness(THEME["board_bg"], -20)
        # Horizontais
        draw.line([BOARD_PADDING, pos, board_size - BOARD_PADDING, pos],
                  fill=grid_color, width=2)
        # Verticais
        draw.line([pos, BOARD_PADDING, pos, board_size - BOARD_PADDING],
                  fill=grid_color, width=2)

    return ImageTk.PhotoImage(board_img)
