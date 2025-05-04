import numpy as np
from collections import deque
from typing import List, Dict, Optional, Tuple, Deque
from functools import lru_cache


class State:
    """Representa um estado do puzzle de 8 peças."""
    
    # Matriz objetivo para cálculo da heurística (constante da classe)
    GOAL_MATRIX = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ])
    
    # Dicionário para armazenar as posições dos elementos na matriz objetivo
    GOAL_POSITIONS = {}
    for (r, c), val in np.ndenumerate(GOAL_MATRIX):
        GOAL_POSITIONS[val] = (r, c)
    
    def __init__(self, current_state: np.ndarray):
        """Inicializa um estado com uma matriz 3x3.
        
        Args:
            current_state: Matriz numpy 3x3 representando o estado atual do puzzle
        """
        self.current_state = current_state
        # Pré-calcula e armazena valores frequentemente usados
        self._string_repr = self._calculate_string_repr()
        self.heuristic = self._calculate_heuristic_manhattan()
        self.heuristic2 = self._calculate_heuristic_manhattanPenality()
        self._hash = hash(self._string_repr)
        
    def _calculate_heuristic_manhattan(self) -> int:
        """Calcula a heurística de distância Manhattan para o estado atual.
        
        Returns:
            int: Soma das distâncias Manhattan de cada peça até sua posição final
        """
        manhattan_dist_sum = 0
        
        for (row, col), value in np.ndenumerate(self.current_state):
            if value != 0:  # Ignoramos o espaço vazio (0) no cálculo
                # Usa o dicionário pré-calculado para obter a posição objetivo
                goal_row, goal_col = self.GOAL_POSITIONS[value]
                manhattan_dist_sum += abs(goal_row - row) + abs(goal_col - col)
        
        return manhattan_dist_sum
    
    def _calculate_heuristic_manhattanPenality(self) -> int:
        """
        Calcula a heurística de Manhattan com penalidade por conflitos lineares.
        
        Returns:
            int: Valor heurístico (distância de Manhattan + penalidades)
        """
        manhattan_dist_sum = 0
        linear_conflict_penalty = 0
        board = self.current_state  # Supondo que seja uma matriz NumPy 3x3

        # Calcula a distância Manhattan normal
        for (row, col), value in np.ndenumerate(board):
            if value != 0:  # Ignora espaço vazio
                goal_row, goal_col = self.GOAL_POSITIONS[value]
                manhattan_dist_sum += abs(goal_row - row) + abs(goal_col - col)

        # Verifica conflitos lineares em linhas
        for row in range(3):
            current_row = board[row]
            for i in range(3):
                for j in range(i + 1, 3):
                    val_i = current_row[i]
                    val_j = current_row[j]
                    if val_i != 0 and val_j != 0:
                        # Ambas as peças devem estar nesta mesma linha na meta
                        goal_row_i, goal_col_i = self.GOAL_POSITIONS[val_i]
                        goal_row_j, goal_col_j = self.GOAL_POSITIONS[val_j]
                        if goal_row_i == row and goal_row_j == row:
                            # Se estão invertidas em relação à posição final, há conflito
                            if goal_col_i > goal_col_j:
                                linear_conflict_penalty += 2

        # Verifica conflitos lineares em colunas
        for col in range(3):
            current_col = board[:, col]
            for i in range(3):
                for j in range(i + 1, 3):
                    val_i = current_col[i]
                    val_j = current_col[j]
                    if val_i != 0 and val_j != 0:
                        goal_row_i, goal_col_i = self.GOAL_POSITIONS[val_i]
                        goal_row_j, goal_col_j = self.GOAL_POSITIONS[val_j]
                        if goal_col_i == col and goal_col_j == col:
                            if goal_row_i > goal_row_j:
                                linear_conflict_penalty += 2

        return manhattan_dist_sum + linear_conflict_penalty

    def _calculate_string_repr(self) -> str:
        """Calcula a representação em string do estado atual.
        
        Returns:
            str: Representação do estado como string (ex: '123456780')
        """
        return ''.join(str(self.current_state[i, j]) for i in range(3) for j in range(3))
 
    def print_state(self) -> None:
        """Imprime o estado atual do puzzle em formato de matriz 3x3."""
        n = 3
        for i in range(n):
            for j in range(n):
                print(f"{self.current_state[i][j]} ", end="")
            print()
        print()

    def from_matrix_string(self) -> str:
        """Retorna a representação em string pré-calculada do estado.
        
        Returns:
            str: Representação do estado como string (ex: '123456780')
        """
        return self._string_repr
    
    def get_neighbors(self) -> List['State']:
        """Gera todos os estados vizinhos possíveis movendo o espaço vazio.
        
        Returns:
            List[State]: Lista de estados vizinhos válidos
        """
        neighbours = []

        # Encontra a posição do espaço vazio (0)
        positions = np.where(self.current_state == 0)
        if len(positions[0]) == 0:
            return neighbours  # Retorna lista vazia se não encontrar o espaço vazio
            
        row, col = positions[0][0], positions[1][0]

        # Direções possíveis: cima, baixo, esquerda, direita
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for d_row, d_col in directions:
            new_row = d_row + row
            new_col = d_col + col
            
            # Verifica se a nova posição está dentro dos limites do puzzle
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = self.current_state.copy()
                # Troca o espaço vazio com a peça na nova posição
                new_state[row, col], new_state[new_row, new_col] = new_state[new_row, new_col], new_state[row, col]
                neighbours.append(State(new_state))

        return neighbours
    
    def __hash__(self) -> int:
        """Permite usar o estado como chave em dicionários.
        
        Returns:
            int: Hash único para este estado
        """
        return self._hash
    
    def __eq__(self, other: object) -> bool:
        """Compara se dois estados são iguais.
        
        Args:
            other: Outro objeto para comparação
            
        Returns:
            bool: True se os estados forem iguais
        """
        if not isinstance(other, State):
            return False
        return self._string_repr == other._string_repr
    
    def __lt__(self, other: 'State') -> bool:
        """Comparação para uso em estruturas como heapq.
        
        Args:
            other: Outro estado para comparação
            
        Returns:
            bool: True se este estado for "menor" que o outro
        """
        return self._string_repr < other._string_repr


def reconstruct_path(initial_key: str, visited_list: Dict[str, Optional[str]]) -> Deque[str]:
    """Reconstrói o caminho da solução a partir do dicionário de estados visitados.
    
    Args:
        initial_key: Chave do estado final ('123456780')
        visited_list: Dicionário mapeando estados para seus predecessores
        
    Returns:
        Deque[str]: Pilha contendo o caminho da solução
    """
    stack = deque()
    current_key = initial_key

    while current_key is not None:
        stack.append(current_key)
        current_key = visited_list[current_key]

    return stack
