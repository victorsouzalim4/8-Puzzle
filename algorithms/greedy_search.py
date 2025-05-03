import heapq
import time
from collections import deque
from typing import Tuple, Dict, List, Deque, Optional, Set

from utils.state import State, reconstruct_path
from utils.priority_queue import PriorityQueue

def greedy_best_first_search(initial_state: State) -> Tuple[Deque[str], float, int]:
    """Implementa o algoritmo de busca gulosa para encontrar um caminho para o estado objetivo.
    
    A busca gulosa de melhor primeiro usa apenas a heurística para escolher o próximo estado,
    sem considerar o custo do caminho percorrido até o momento.
    
    A busca gulosa de melhor primeiro usa apenas a heurística para escolher o próximo estado,
    sem considerar o custo do caminho percorrido até o momento.
    
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
    predecessors: Dict[str, Optional[str]] = {}
    
    # Fila de prioridade personalizada para a busca gulosa
    open_set = PriorityQueue()
    
    # Adiciona o estado inicial à fila de prioridade
    open_set.push(initial_state, initial_state.heuristic)

    # Marca o estado inicial como visitado
    visited_set.add(initial_state)
    predecessors[initial_state.from_matrix_string()] = None

    # Estado objetivo em formato de string
    goal_state = '123456780'
    
    while not open_set.empty():
        # Obtém o estado com menor valor de heurística
        _, current = open_set.pop()
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
                
                # Adiciona o vizinho à fila de prioridade
                open_set.push(neighbor, neighbor.heuristic)
                
                # Atualiza o predecessor deste vizinho
                predecessors[neighbor.from_matrix_string()] = current_str
    
    # Se não encontrou solução
    return deque(), time.perf_counter() - start_time, expanded_nodes