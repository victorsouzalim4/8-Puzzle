import timeit

from collections import deque
from typing import Deque, Dict, Optional, Set, Tuple

from utils.priority_queue import PriorityQueue
from utils.state import State, reconstruct_path


def astar_search(initial_state: State, heuristic = "heuristic") -> Tuple[Deque[str], float, int]:
    """Implementa o algoritmo A* para encontrar o caminho mais curto para o estado objetivo.
    
    O algoritmo A* combina a busca de melhor primeiro com uma heurística admissível
    para encontrar o caminho ótimo até o estado objetivo ('123456780').
    
    Args:
        initial_state: Estado inicial do puzzle
        
    Returns:
        Tuple contendo:
            - Deque[str]: Caminho da solução (sequência de estados)
            - float: Tempo de execução em segundos
            - int: Número de estados expandidos
    """
    start_time = timeit.default_timer() 

    # Contador de estados expandidos
    expanded_nodes = 0
    
    # Conjunto de estados fechados (já explorados completamente)
    closed_set: Set[State] = set()
    
    # Dicionário para rastrear predecessores (para reconstrução do caminho)
    predecessors: Dict[str, Optional[str]] = {}
    
    # Fila de prioridade personalizada para o algoritmo A*
    open_set = PriorityQueue()
    
    # Dicionário para armazenar o custo g (custo real) para cada estado
    g_score: Dict[State, int] = {initial_state: 0}

    # Selecionar heuristica desejada
    heuristic_attr = {
        "manhattan": "heuristic",
        "manhattanPenality": "heuristic2",
        "euclidean": "heuristic_euclidean"
    }.get(heuristic, "heuristic")  # Default para Manhattan se não encontrado
    
    # Adiciona o estado inicial à fila de prioridade com f_score = h_score
    heuristic_value = getattr(initial_state, heuristic_attr)
    open_set.push(initial_state, heuristic_value)

    # Marca o estado inicial no dicionário de predecessores
    predecessors[initial_state.from_matrix_string()] = None

    # Estado objetivo em formato de string
    goal_state = '123456780'
    
    while not open_set.empty():
        # Obtém o estado com menor f_score (f = g + h)
        _, current = open_set.pop()
        current_str = current.from_matrix_string()
        
        # Verifica se já exploramos este estado
        if current in closed_set:
            continue
            
        # Adiciona ao conjunto de estados fechados
        closed_set.add(current)

        # Verifica se atingimos o estado objetivo
        if current_str == goal_state:
            exec_time = timeit.default_timer() - start_time
            return reconstruct_path(goal_state, predecessors), exec_time, expanded_nodes

        # Explora todos os vizinhos do estado atual
        for neighbor in current.get_neighbors(): 
            # Pula se o vizinho já foi completamente explorado
            if neighbor in closed_set:
                continue
                
            # Calcula o novo custo g para este vizinho
            tentative_g = g_score[current] + 1
            
            # Verifica se este é um novo estado ou se encontramos um caminho melhor
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                expanded_nodes += 1
                
                # Atualiza o custo g para este vizinho
                g_score[neighbor] = tentative_g

                # Buscar o custo h para este vizinho
                heuristic_value = getattr(neighbor, heuristic_attr)
                
                # Calcula o f_score (f = g + h)
                f_score = tentative_g + heuristic_value
                
                # Atualiza o predecessor deste vizinho
                predecessors[neighbor.from_matrix_string()] = current_str
                
                # Adiciona ou atualiza o vizinho na fila de prioridade
                open_set.push(neighbor, f_score)
    
    # Se não encontrou solução
    return deque(), timeit.default_timer() - start_time, expanded_nodes