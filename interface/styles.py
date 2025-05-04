"""Define constantes de estilo como THEME, FONTS e tamanhos."""

# Esquema de cores moderno e científico
THEME = {
    "bg_primary": "#2c3e50",         # Azul escuro
    "bg_secondary": "#34495e",      # Azul menos escuro
    "bg_tertiary": "#ecf0f1",       # Quase branco
    "accent": "#2980B9",            # Azul claro
    "accent_hover": "#1F618D",      # Azul médio
    "warning": "#D35400",           # Vermelho
    "success": "#16A085",           # Verde
    "text_light": "#ecf0f1",        # Branco azulado
    "text_dark": "#2c3e50",         # Azul escuro
    "border": "#bdc3c7",            # Cinza claro
    
    # Cores do tabuleiro
    "board_bg": "#8b4513",          # Cor base da madeira
    "board_highlight": "#d2b48c",   # Realce da madeira
    "tile": "#d2b48c",              # Cor das peças
    "tile_text": "#5d4037",         # Cor do texto nas peças
    
    # Cores dos algoritmos para gráficos
    "algorithm": {
        "BFS": "#3498db",           # Azul
        "Greedy": "#e74c3c",        # Vermelho
        "A*": "#2ecc71"             # Verde
    }
}

# Fontes
FONTS = {
    "title": ("Segoe UI", 20, "bold"),
    "subtitle": ("Segoe UI", 16, "bold"),
    "heading": ("Segoe UI", 14, "bold"),
    "normal": ("Segoe UI", 11),
    "small": ("Segoe UI", 9),
    "mono": ("Consolas", 10),
    "tile": ("Segoe UI", 24, "bold")
}

# Tamanhos
TILE_SIZE = 80
BOARD_PADDING = 10
ANIMATION_SPEED = 50  # frames por movimento (maior = mais lento)

def _adjust_color_brightness(hex_color, factor):
    """Ajusta o brilho de uma cor hex.
    
    Args:
        hex_color: String de cor no formato hexadecimal (ex: "#rrggbb")
        factor: Valor para ajustar o brilho (-255 a 255)
        
    Returns:
        String de cor ajustada no formato hexadecimal
    """
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    r = max(0, min(255, r + factor))
    g = max(0, min(255, g + factor))
    b = max(0, min(255, b + factor))
    
    return f'#{r:02x}{g:02x}{b:02x}'
