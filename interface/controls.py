"""Componentes de controle da interface (botões, seleções, etc.)."""

import tkinter as tk
from tkinter import ttk

from .styles import THEME, FONTS # Importar estilos necessários

def create_controls_frame(parent, app):
    """Cria e configura o frame de controles dentro do frame pai.
    
    Args:
        parent: O widget tk/ttk pai onde o frame de controles será inserido.
        app: A instância principal da aplicação (PuzzleScientificInterface).
    """
    controls_frame = ttk.Frame(parent, style="TFrame")
    controls_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # --- Seleção de algoritmo --- 
    algorithm_frame = ttk.LabelFrame(
        controls_frame, 
        text="Algoritmo de Busca", 
        style="TLabelframe"
    )
    algorithm_frame.pack(fill=tk.X, pady=(0,15))
    
    # A variável app.algorithm_var é criada em ui_setup.py ou no __init__, 
    # aqui apenas a usamos.
    if not hasattr(app, 'algorithm_var') or app.algorithm_var is None:
        app.algorithm_var = tk.StringVar(value="A*") # Fallback, idealmente já existe
        
    algorithms = [
        ("Busca em Largura (BFS)", "BFS"),
        ("Busca Gulosa (Greedy)", "Greedy"),
        ("A* (A-Star)", "A*")
    ]
    
    for text, value in algorithms:
        rb = ttk.Radiobutton(
            algorithm_frame,
            text=text,
            value=value,
            variable=app.algorithm_var, 
            style="TRadiobutton" 
        )
        rb.pack(anchor=tk.W, padx=10, pady=3)
    
    # --- Botões de Ação --- 
    buttons_frame = ttk.Frame(controls_frame, style="TFrame")
    buttons_frame.pack(fill=tk.X, pady=10)
    buttons_frame.columnconfigure((0, 1, 2), weight=1) 
    
    # Os botões são armazenados como atributos de 'app' para acesso posterior
    app.randomize_button = ttk.Button(
        buttons_frame,
        text="Embaralhar",
        command=app.randomize_board, 
        style="TButton",
        width=12
    )
    app.randomize_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    app.solve_button = ttk.Button(
        buttons_frame,
        text="Resolver",
        command=app.solve_puzzle, 
        style="Success.TButton", 
        width=12
    )
    app.solve_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    app.reset_button = ttk.Button(
        buttons_frame,
        text="Reiniciar",
        command=app.reset_board, 
        style="Warning.TButton", 
        width=12
    )
    app.reset_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    # --- Frame de Resultados --- 
    # (Mantido aqui por enquanto, pode ser movido depois)
    app.results_frame = ttk.LabelFrame(
        controls_frame, 
        text="Resultados da Solução", 
        style="TLabelframe"
    )
    app.results_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
    
    app.results_text = tk.Text(
        app.results_frame,
        bg=THEME["bg_tertiary"],
        fg=THEME["text_dark"],
        font=FONTS["mono"],
        height=10,
        width=40, 
        state=tk.DISABLED,
        wrap=tk.WORD, 
        padx=5, pady=5
    )
    app.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Scrollbar para Resultados
    scrollbar = ttk.Scrollbar(app.results_text, orient=tk.VERTICAL, command=app.results_text.yview)
    app.results_text['yscrollcommand'] = scrollbar.set
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    return controls_frame # Retorna o frame criado
