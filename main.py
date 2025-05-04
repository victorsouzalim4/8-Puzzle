import numpy as np
from typing import List, Deque, Optional

from utils.state import State
from algorithms.breadth_first_search import breadth_first_search
from algorithms.greedy_search import greedy_best_first_search
from algorithms.astar_search import astar_search


def print_formatted(state_str: str) -> None:
    """Imprime o estado do puzzle em formato de matriz 3x3.
    
    Args:
        state_str: Representação do estado como string (ex: '123456780')
    """
    for i in range(9):
        print(f"{state_str[i]} ", end="")
        if (i+1) % 3 == 0: 
            print()
        


def run_and_print_results(algorithm_name: str, algorithm_fn, initial_state: State, heuristic: Optional[str] = None) -> None:
    """Executa um algoritmo de busca e imprime os resultados.
    
    Args:
        algorithm_name: Nome do algoritmo para exibição
        algorithm_fn: Função do algoritmo a ser executada
        initial_state: Estado inicial do puzzle
    """
    print(f"\n{'-'*50}")
    print(f"Executando {algorithm_name}...")
    print(f"{'-'*50}")
    
    if heuristic != None:
        path, exec_time, expanded_nodes = algorithm_fn(initial_state, heuristic)
    else:
        path, exec_time, expanded_nodes = algorithm_fn(initial_state) 
    
    
    print(f"Comprimento do caminho da solução: {len(path) - 1} movimentos")
    print(f"Tempo de execução: {exec_time:.4f}s")
    print(f"Número de estados expandidos: {expanded_nodes}")
    
    # Descomente para visualizar o caminho da solução
    # print("\nCaminho da solução:")
    # while path:
    #     print_formatted(path.pop())
    #     print()


def main() -> None:
    """Função principal que configura e executa os algoritmos de busca."""
    # Estado inicial do puzzle
    matriz = np.array([
        [8, 6, 7],
        [2, 5, 4],
        [3, 0, 1]
    ])
    
    initial_state = State(matriz)
    print("Estado inicial:")
    initial_state.print_state()
    
    # Executa os algoritmos de busca
    run_and_print_results("Busca em Largura", breadth_first_search, initial_state)
    run_and_print_results("Busca Gulosa", greedy_best_first_search, initial_state)
    run_and_print_results("A* - Manhattan", astar_search, initial_state)
    run_and_print_results("A* - ManhattanPenality", astar_search, initial_state, "heuristic2")


if __name__ == "__main__":
    main()
