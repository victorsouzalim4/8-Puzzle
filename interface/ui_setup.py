"""Funções para configurar a estrutura inicial da UI e estilos."""

import tkinter as tk
from tkinter import ttk

from .styles import THEME, FONTS, TILE_SIZE, BOARD_PADDING, _adjust_color_brightness
from .textures import create_board_texture
from .board_tab import setup_board_tab

def setup_style(app):
    """Configura o estilo dos widgets Ttk para a aplicação."""
    style = ttk.Style(app)
    style.theme_use('clam') # Usar um tema base que permite mais customização

    # --- Configurações Globais do Tema ---
    style.configure('.', 
                    background=THEME["bg_secondary"], 
                    foreground=THEME["text_light"], 
                    font=FONTS["normal"],
                    borderwidth=0,
                    focuscolor=THEME["accent"])

    # --- Frame ---
    style.configure("TFrame", 
                    background=THEME["bg_secondary"])
    style.configure("Light.TFrame", 
                    background=THEME["bg_tertiary"], # Frame claro para resultados
                    borderwidth=1,
                    relief='solid') 

    # --- Label ---
    style.configure("TLabel", 
                    background=THEME["bg_secondary"], 
                    foreground=THEME["text_light"], 
                    font=FONTS["normal"])
    style.configure("Heading.TLabel", 
                    font=FONTS["heading"],
                    anchor='w')
    style.configure("Result.TLabel",
                    background=THEME["bg_tertiary"],
                    foreground=THEME["text_dark"], # Texto escuro no fundo claro
                    font=FONTS["mono"],
                    anchor='nw')

    # --- Botão Padrão (TButton) ---
    style.configure("TButton", 
                    background=THEME["accent"], 
                    foreground=THEME["text_light"], 
                    font=FONTS["normal"],
                    padding=(10, 5),       # Aumentar padding (horizontal, vertical)
                    borderwidth=1,       # Adicionar borda
                    relief="raised")     # Efeito de relevo
    style.map("TButton",
              background=[('active', _adjust_color_brightness(THEME["accent"], -30)), # Mais escuro ao clicar
                          ('hover', _adjust_color_brightness(THEME["accent"], -15))],  # Pouco mais escuro no hover
              foreground=[('active', THEME["text_light"])],
              relief=[('pressed', 'sunken'), 
                      ('!pressed', 'raised')])

    # --- Botão Sucesso (Verde) ---
    style.configure("Success.TButton", 
                    background=THEME["success"],
                    foreground=THEME["text_light"])
    style.map("Success.TButton",
              background=[('active', _adjust_color_brightness(THEME["success"], -30)),
                          ('hover', _adjust_color_brightness(THEME["success"], -15))],
              foreground=[('active', THEME["text_light"])])

    # --- Botão Aviso (Laranja/Vermelho) ---
    style.configure("Warning.TButton", 
                    background=THEME["warning"],
                    foreground=THEME["text_light"])
    style.map("Warning.TButton",
              background=[('active', _adjust_color_brightness(THEME["warning"], -30)),
                          ('hover', _adjust_color_brightness(THEME["warning"], -15))],
              foreground=[('active', THEME["text_light"])])

    # --- Botão Perigo (Vermelho - se necessário) ---
    # style.configure("Danger.TButton", 
    #                 background=THEME["error"],
    #                 foreground=THEME["text_light"])
    # style.map("Danger.TButton",
    #           background=[('active', _adjust_color_brightness(THEME["error"], -30)),
    #                       ('hover', _adjust_color_brightness(THEME["error"], -15))],
    #           foreground=[('active', THEME["text_light"])])

    # --- Radiobutton ---
    style.configure("TRadiobutton", 
                    background=THEME["bg_secondary"], 
                    foreground=THEME["text_light"], 
                    font=FONTS["normal"],
                    indicatorbackground=THEME["bg_tertiary"],
                    indicatormargin=5)
    style.map("TRadiobutton",
              indicatorbackground=[('selected', THEME["accent"])])

    # --- Notebook (Abas) ---
    style.configure("TNotebook", 
                    background=THEME["bg_primary"],
                    borderwidth=0)
    style.configure("TNotebook.Tab", 
                    background=THEME["bg_secondary"], 
                    foreground=THEME["text_light"], 
                    padding=[10, 5],
                    font=FONTS["normal"],
                    borderwidth=1)
    style.map("TNotebook.Tab", 
              background=[("selected", THEME["accent"]), 
                          ("active", _adjust_color_brightness(THEME["bg_secondary"], 15))], # Hover da aba
              foreground=[("selected", THEME["text_light"])])

    # --- Text (Resultados) ---
    # Não há estilo ttk direto, mas podemos definir a cor de fundo/texto ao criar
    # O frame 'Light.TFrame' já define o fundo claro

    # --- Separator ---
    style.configure("TSeparator", 
                    background=THEME["border"])

    # --- Scrollbar ---
    style.configure("Vertical.TScrollbar", 
                    background=THEME["bg_secondary"], 
                    troughcolor=THEME["bg_primary"], 
                    bordercolor=THEME["bg_secondary"],
                    arrowcolor=THEME["text_light"])
    style.map("Vertical.TScrollbar", 
              background=[('active', THEME["accent"])])

def setup_ui(app):
    """Configura os elementos da interface gráfica da aplicação."""
    # Frame principal
    # Note: Os widgets são criados como filhos de 'app' ou de outros frames dentro de 'app'
    main_frame = tk.Frame(app, bg=THEME["bg_primary"])
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Título
    title_label = tk.Label(
        main_frame, 
        text="Puzzle de 8 Peças - Laboratório", # Título ajustado
        font=FONTS["title"],
        bg=THEME["bg_primary"],
        fg=THEME["text_light"]
    )
    title_label.pack(pady=(0, 20))
    
    # Notebook (Abas)
    app.notebook = ttk.Notebook(main_frame, style="TNotebook")
    app.notebook.pack(fill=tk.BOTH, expand=True)
    
    # Criar as abas (Frames como filhos do notebook)
    app.board_tab = ttk.Frame(app.notebook, style="TFrame", padding=10)
    
    app.notebook.add(app.board_tab, text='Tabuleiro')

    
    # --- Configuração da Aba 'Tabuleiro Interativo' --- 
    setup_board_tab(app.board_tab, app) # <<< Chamada para a função do módulo

    # Inicializar o desenho do tabuleiro (pode ser feito aqui ou no __init__ após setup_ui)
    # app.draw_board() # Movido para o final do __init__ provavelmente
