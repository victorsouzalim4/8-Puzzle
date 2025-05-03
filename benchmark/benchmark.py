"""
Script para benchmarking dos algoritmos de busca do Puzzle de 8 peças.
Registra o desempenho atual em um arquivo de log para comparação futura.
"""
from datetime import datetime
import json
import time

import numpy as np

from algorithms.astar_search import astar_search
from algorithms.breadth_first_search import breadth_first_search
from algorithms.greedy_search import greedy_best_first_search
from utils.state import State


def run_benchmark(algorithm_name, algorithm_fn, initial_state, num_runs=1):
    """Executa um algoritmo várias vezes e retorna estatísticas de desempenho.
    
    Args:
        algorithm_name: Nome do algoritmo
        algorithm_fn: Função do algoritmo
        initial_state: Estado inicial
        num_runs: Número de execuções para calcular a média
        
    Returns:
        dict: Estatísticas de desempenho
    """
    total_time = 0
    total_nodes = 0
    path_lengths = []
    
    for _ in range(num_runs):
        path, exec_time, expanded_nodes = algorithm_fn(initial_state)
        total_time += exec_time
        total_nodes += expanded_nodes
        path_lengths.append(len(path) - 1 if path else 0)
    
    return {
        "algorithm": algorithm_name,
        "avg_time": total_time / num_runs,
        "avg_nodes": total_nodes / num_runs,
        "path_lengths": path_lengths,
        "avg_path_length": sum(path_lengths) / len(path_lengths) if path_lengths else 0
    }


def main():
    # Estado inicial do puzzle
    matriz = np.array([
        [8, 6, 7],
        [2, 5, 4],
        [3, 0, 1]
    ])
    
    initial_state = State(matriz)
    
    # Configuração do benchmark
    algorithms = [
        ("Busca em Largura", breadth_first_search),
        ("Busca Gulosa", greedy_best_first_search),
        ("A*", astar_search)
    ]
    
    # Executa o benchmark
    results = []
    for name, fn in algorithms:
        print(f"Executando benchmark para {name}...")
        result = run_benchmark(name, fn, initial_state)
        results.append(result)
        print(f"  Tempo médio: {result['avg_time']:.4f}s")
        print(f"  Nós expandidos: {result['avg_nodes']:.0f}")
        print(f"  Comprimento do caminho: {result['avg_path_length']:.0f}")
    
    # Salva os resultados em um arquivo de log
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"benchmark_log_{timestamp}.json"
    
    with open(log_file, "w") as f:
        json.dump({
            "timestamp": timestamp,
            "results": results,
            "metadata": {
                "initial_state": initial_state.from_matrix_string(),
                "version": "original"
            }
        }, f, indent=2)
    
    print(f"\nResultados salvos em {log_file}")


if __name__ == "__main__":
    main()
