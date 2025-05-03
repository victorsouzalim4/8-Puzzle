"""Componentes e lógica da aba 'Board'."""

import tkinter as tk
from tkinter import ttk

from .styles import THEME, FONTS, TILE_SIZE, BOARD_PADDING
from .textures import create_board_texture
from .controls import create_controls_frame

def setup_board_tab(tab_frame, app):
    """Configura o conteúdo da aba 'Tabuleiro Interativo'.

    Args:
        tab_frame: O frame da aba onde o conteúdo será inserido.
        app: A instância principal da aplicação (PuzzleScientificInterface).
    """
    # Frame de conteúdo principal para esta aba
    board_content_frame = ttk.Frame(tab_frame, style="TFrame")
    board_content_frame.pack(fill=tk.BOTH, expand=True)

    # --- Frame para o tabuleiro (Esquerda) --- 
    # O frame container é criado e armazenado no app para referência externa
    app.board_frame_container = ttk.Frame(
        board_content_frame, 
        style="TFrame",
        width=TILE_SIZE * 3 + BOARD_PADDING * 4, # Padding extra visual
        height=TILE_SIZE * 3 + BOARD_PADDING * 4 
    )
    app.board_frame_container.pack(side=tk.LEFT, padx=20, pady=20, anchor='center')
    app.board_frame_container.pack_propagate(False) # Manter tamanho fixo

    # --- Canvas para o tabuleiro (dentro do container) --- 
    # O canvas também é armazenado no app
    app.board_canvas = tk.Canvas(
        app.board_frame_container,
        width=TILE_SIZE * 3 + BOARD_PADDING * 2,
        height=TILE_SIZE * 3 + BOARD_PADDING * 2,
        bg=THEME["board_bg"], 
        highlightthickness=0
    )
    app.board_canvas.pack(expand=True) # Centraliza o canvas no container
    
    # Desenhar a textura de fundo (se existir)
    # A textura é criada/armazenada no app (provavelmente no __init__ ou setup_ui)
    if hasattr(app, 'board_texture') and app.board_texture:
         app.board_canvas.create_image(0, 0, image=app.board_texture, anchor='nw', tags="board_bg")
         # Redesenhar o tabuleiro inicial (se necessário, pode ser chamado externamente) 
         # app.draw_board() 

    # --- Frame para controles (Direita) --- 
    # Chama a função que cria os controles, passando o frame de conteúdo e o app
    create_controls_frame(board_content_frame, app)
