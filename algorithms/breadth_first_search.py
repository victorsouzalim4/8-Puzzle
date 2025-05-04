import time
from collections import deque
from typing import Tuple, Dict, List, Deque, Optional, Set

from utils.state import State, reconstruct_path


def breadth_first_search(initial_state: State) -> Tuple[Deque[str], float, int]:
    """Implementa o algoritmo de busca em largura para encontrar um caminho para o estado objetivo.
    
    A busca em largura explora todos os estados na mesma profundidade antes de avançar,
    garantindo encontrar o caminho com menor número de movimentos.
    
    Args:
        initial_state: Estado inicial do puzzle
        
    Returns:
        Tuple contendo:
            - Deque[str]: Caminho da solução (sequência de estados)
            - float: Tempo de execução em segundos
            - int: Número de estados expandidos
    """
    start_time = time.perf_counter() 

    # Contador de estados expandidos
    expanded_nodes = 0
    
    # Conjunto para verificar rapidamente se um estado já foi visitado
    visited_set: Set[State] = set()
    
    # Dicionário para rastrear predecessores (para reconstrução do caminho)
    # Usamos a representação em string para compatibilidade com a função reconstruct_path
    predecessors: Dict[str, Optional[str]] = {}
    
    # Fila para a busca em largura
    queue = deque()
    
    # Adiciona o estado inicial à fila
    queue.append(initial_state)
    
    # Marca o estado inicial como visitado
    visited_set.add(initial_state)
    predecessors[initial_state.from_matrix_string()] = None

    # Estado objetivo em formato de string
    goal_state = '123456780'
    
    while queue:
        # Obtém o próximo estado da fila
        current = queue.popleft()
        current_str = current.from_matrix_string()

        # Verifica se atingimos o estado objetivo
        if current_str == goal_state:
            exec_time = time.perf_counter() - start_time
            return reconstruct_path(goal_state, predecessors), exec_time, expanded_nodes

        # Explora todos os vizinhos do estado atual
        for neighbor in current.get_neighbors():
            # Verifica se este vizinho já foi visitado usando o conjunto
            if neighbor not in visited_set:
                expanded_nodes += 1
                
                # Marca o vizinho como visitado
                visited_set.add(neighbor)
                
                # Adiciona o vizinho à fila
                queue.append(neighbor)
                
                # Atualiza o predecessor deste vizinho
                predecessors[neighbor.from_matrix_string()] = current_str
    
    # Se não encontrou solução
    return deque(), time.perf_counter() - start_time, expanded_nodes
