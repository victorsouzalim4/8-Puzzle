"""
Interface científica avançada para o Puzzle de 8 peças.
Permite ao usuário selecionar o estado inicial, escolher o algoritmo,
visualizar o processo de solução e analisar métricas de desempenho detalhadas.
"""

import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

from algorithms.astar_search import astar_search
from algorithms.breadth_first_search import breadth_first_search
from algorithms.greedy_search import greedy_best_first_search
from interface.styles import ANIMATION_SPEED, BOARD_PADDING, FONTS, THEME, TILE_SIZE
from interface.textures import create_board_texture, create_tile_textures
from interface.ui_setup import setup_style, setup_ui
from utils.state import State
matplotlib.use('Agg')  # Usar backend não interativo



class PuzzleScientificInterface(tk.Tk):
    """Interface para o Puzzle de 8 peças.
    Fornece ferramentas para análise comparativa de algoritmos de busca,
    visualização de dados e exportação de resultados.
    """
    
    # Esquema de cores, Fontes e Tamanhos movidos para interface/styles.py
    # THEME = { ... } # Removido
    # FONTS = { ... } # Removido
    # TILE_SIZE = 80 # Removido
    # BOARD_PADDING = 10 # Removido
    # ANIMATION_SPEED = 10 # Removido
    
    def __init__(self):
        """Inicializa a interface científica."""
        super().__init__()
        
        # Configurações básicas da janela
        self.title("Puzzle de 8 Peças - Métodos de Busca")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(bg=THEME["bg_primary"])
        self.saved_state = None  # Armazena o estado memorizado
        
        # Estado atual e histórico de estados do puzzle
        self.current_state = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])
        self.state_history = []
        
        # Armazenamento de resultados para comparação
        self.results_data = {
            "BFS": [],
            "Greedy": [],
            "A*": []
        }
        
        # Imagens e recursos visuais
        self.tile_images = create_tile_textures()
        self.board_texture = create_board_texture() # <<< Criar textura aqui

        # Variáveis para controle da solução
        self.solution_path = None
        self.solution_thread = None
        self.animation_frames = []
        self.current_animation_frame = 0
        self.is_solving = False
        self.is_comparing = False

        # --- Adicionar atributos que serão criados por setup_ui --- 
        self.notebook = None
        self.board_tab = None
        self.board_frame_container = None
        self.board_canvas = None
        # self.algorithm_var = tk.StringVar(value="A*") # <<< Inicialização direta
        self.algorithm_var = tk.StringVar(value="A* - Euclidean")  # Ou adicione à lista de opções existente
        self.randomize_button = None
        self.solve_button = None
        self.reset_button = None
        self.results_frame = None
        self.results_text = None
        # --- Fim dos atributos adicionados ---

        # Estado do carregamento
        self.loading_percentage = 0
        self.loading_text = ""
        
        # Configurar Interface gráfica e Estilos usando funções importadas
        setup_style(self) 
        setup_ui(self) 
        
        # Desenhar o tabuleiro inicial após a UI estar pronta
        self.draw_board() # <<< Adicionar chamada aqui
            
    def draw_board(self):
        """Desenha o tabuleiro do puzzle com o estado atual."""
        # Limpar o canvas
        self.board_canvas.delete("tile")
        
        # Desenhar cada peça
        for i in range(3):
            for j in range(3):
                value = self.current_state[i, j]
                if value != 0:  # Não desenhar o espaço vazio
                    x0 = j * TILE_SIZE + BOARD_PADDING
                    y0 = i * TILE_SIZE + BOARD_PADDING
                    x1 = x0 + TILE_SIZE - 2
                    y1 = y0 + TILE_SIZE - 2
                    
                    # Criar retângulo para a peça
                    self.board_canvas.create_rectangle(
                        x0, y0, x1, y1,
                        fill=THEME["tile"],
                        outline=THEME["board_highlight"],
                        width=2,
                        tags="tile"
                    )
                    
                    # Adicionar número
                    self.board_canvas.create_text(
                        (x0 + x1) // 2,
                        (y0 + y1) // 2,
                        text=str(value),
                        font=FONTS["tile"],
                        fill=THEME["tile_text"],
                        tags="tile"
                    )
    
    def randomize_board(self):
        """Embaralha o tabuleiro para um estado aleatório solucionável."""
        if self.is_solving:
            return
            
        # Gerar um estado aleatório
        numbers = list(range(9))  # 0-8
        np.random.shuffle(numbers)
        
        # Verificar se é solucionável
        inversions = 0
        for i in range(9):
            for j in range(i + 1, 9):
                if numbers[i] != 0 and numbers[j] != 0 and numbers[i] > numbers[j]:
                    inversions += 1
        
        # Se o número de inversões for ímpar, o puzzle não é solucionável
        # Nesse caso, trocamos duas peças para torná-lo solucionável
        if inversions % 2 == 1:
            # Encontrar duas peças não-zero para trocar
            idx1, idx2 = 0, 1
            while numbers[idx1] == 0 or numbers[idx2] == 0:
                idx1 = np.random.randint(0, 9)
                idx2 = np.random.randint(0, 9)
                if idx1 == idx2:
                    idx2 = (idx2 + 1) % 9
            
            # Trocar as peças
            numbers[idx1], numbers[idx2] = numbers[idx2], numbers[idx1]
        
        # Converter para matriz 3x3
        self.current_state = np.array(numbers).reshape(3, 3)
        
        # Atualizar o tabuleiro
        self.draw_board()
        
        # Limpar resultados anteriores
        self.clear_results()
    
    def reset_board(self):
        """Reinicia o tabuleiro para o estado objetivo."""
        if self.is_solving:
            return
            
        # Estado objetivo
        self.current_state = np.array([
            [1, 2, 3],
            [8, 0, 4],
            [7, 6, 5]
        ])
        
        # Atualizar o tabuleiro
        self.draw_board()
        
        # Limpar resultados anteriores
        self.clear_results()
    
    def solve_puzzle(self):
        """Inicia a solução do puzzle com o algoritmo selecionado."""
        if self.is_solving:
            return
            
        # Obter o algoritmo selecionado
        algorithm = self.algorithm_var.get()
        
        # Criar um objeto State com o estado atual
        initial_state = State(self.current_state.copy())
        
        # Iniciar thread para resolver o puzzle
        self.is_solving = True
        self.solution_thread = threading.Thread(
            target=self.run_algorithm,
            args=(algorithm, initial_state)
        )
        self.solution_thread.daemon = True
        self.solution_thread.start()
        
        # Desabilitar botões durante a solução
        self.solve_button.config(state=tk.DISABLED)
        self.randomize_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
    
    def run_algorithm(self, algorithm, initial_state):
        """Executa o algoritmo selecionado e processa os resultados."""
        try:
            # Selecionar o algoritmo
            if algorithm == "BFS":
                algorithm_fn = breadth_first_search
                algorithm_name = "Busca em Largura"
            elif algorithm == "Greedy":
                algorithm_fn = greedy_best_first_search
                algorithm_name = "Busca Gulosa"
            elif algorithm == "A* - Manhattan":
                algorithm_fn = astar_search
                algorithm_name = "A* - Manhattan"
            elif algorithm == "A* - ManhattanPenality":
                algorithm_fn = astar_search
                algorithm_name = "A* - ManhattanPenality"
            elif algorithm == "A* - Euclidean":
                algorithm_fn = astar_search
                algorithm_name = "A* - Euclidean"
            else:  # fallback
                algorithm_fn = astar_search
                algorithm_name = "A* - Manhattan"
            
            # Executar o algoritmo
            if algorithm == "A* - Manhattan":
                start_time = time.time()
                path, exec_time, expanded_nodes = algorithm_fn(initial_state, "manhattan")
                total_time = time.time() - start_time
            elif algorithm == "A* - ManhattanPenality":
                start_time = time.time()
                path, exec_time, expanded_nodes = algorithm_fn(initial_state, "manhattanPenality")
                total_time = time.time() - start_time
            elif algorithm == "A* - Euclidean":
                start_time = time.time()
                path, exec_time, expanded_nodes = algorithm_fn(initial_state, "euclidean")
                total_time = time.time() - start_time
            else:
                start_time = time.time()
                path, exec_time, expanded_nodes = algorithm_fn(initial_state)
                total_time = time.time() - start_time
            
            # Verificar se encontrou solução
            if not path:
                self.show_error("Não foi possível encontrar uma solução para este estado inicial.")
                return
            
            # Atualizar resultados
            self.update_results(algorithm_name, path, exec_time, expanded_nodes, total_time)
            
            # Animar a solução
            self.animate_solution(path)
            
        except Exception as e:
            self.show_error(f"Erro ao executar o algoritmo: {str(e)}")
        finally:
            # Reabilitar botões
            self.after(0, self.enable_buttons)
    
    def update_results(self, algorithm_name, path, exec_time, expanded_nodes, total_time):
        """Atualiza o texto de resultados com as informações da solução."""
        # Formatar texto de resultados
        results = (
            f"Algoritmo: {algorithm_name}\n"
            f"Comprimento do caminho: {len(path) - 1} movimentos\n"
            f"Tempo de execução: {exec_time:.4f}s\n"
            f"Tempo total: {total_time:.4f}s\n"
            f"Nós expandidos: {expanded_nodes}\n"
        )
        
        # Atualizar o widget de texto
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, results)
        self.results_text.config(state=tk.DISABLED)
    
    def animate_solution(self, path):
        """Anima a solução mostrando cada passo no tabuleiro."""
        # Converter o caminho de strings para matrizes
        matrices = []
        
        # O caminho está em ordem reversa (do objetivo ao inicial)
        # Vamos inverter para mostrar do inicial ao objetivo
        path_list = list(path)
        path_list.reverse()
        
        for state_str in path_list:
            # Converter string para matriz 3x3
            matrix = np.array([int(c) for c in state_str]).reshape(3, 3)
            matrices.append(matrix)
        
        # Animar cada passo
        self.animate_step(matrices, 0)
    
    def animate_step(self, matrices, index):
        """Anima um passo da solução."""
        if index < len(matrices):
            # Atualizar o estado atual
            self.current_state = matrices[index]
            
            # Redesenhar o tabuleiro
            self.draw_board()
            
            # Agendar o próximo passo
            self.after(ANIMATION_SPEED, self.animate_step, matrices, index + 1)
        else:
            # Animação concluída
            self.is_solving = False
    
    def enable_buttons(self):
        """Reabilita os botões após a conclusão da solução."""
        self.solve_button.config(state=tk.NORMAL)
        self.randomize_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
    
    def clear_results(self):
        """Limpa o texto de resultados."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)

    def save_current_board(self):
        """Memoriza o estado atual do tabuleiro."""
        self.saved_state = self.current_state.copy()
        messagebox.showinfo("Sucesso", "Tabuleiro memorizado com sucesso!")

    def load_saved_board(self):
        """Carrega o estado memorizado."""
        if self.saved_state is None:
            messagebox.showerror("Erro", "Nenhum tabuleiro foi memorizado!")
            return
        
        if self.is_solving:  # Evita carregar durante uma solução
            return
            
        self.current_state = self.saved_state.copy()
        self.draw_board()
        self.clear_results()
    
    def show_error(self, message):
        """Exibe uma mensagem de erro."""
        messagebox.showerror("Erro", message)
        self.is_solving = False

if __name__ == "__main__":    
    app = PuzzleScientificInterface()
    app.mainloop()
