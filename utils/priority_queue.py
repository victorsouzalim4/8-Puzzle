import heapq
from typing import Deque, Dict, Optional, Set, Tuple

class PriorityQueue:
    """Implementação de fila de prioridade com suporte a atualização de prioridade."""
    
    def __init__(self):
        self.elements = []
        self.entry_finder = {}  # Mapeamento de item -> entrada
        self.counter = 0  # Contador único para desempate
    
    def push(self, item, priority):
        """Adiciona um novo item ou atualiza a prioridade de um item existente."""
        if item in self.entry_finder:
            self.remove(item)  # Remove a entrada anterior se existir
        
        # Adiciona nova entrada
        entry = [priority, self.counter, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.elements, entry)
        self.counter += 1
    
    def remove(self, item):
        """Remove um item da fila (marca como removido)."""
        entry = self.entry_finder.pop(item)
        entry[2] = None  # Marca como removido
    
    def pop(self):
        """Remove e retorna o item com menor prioridade. Levanta KeyError se vazio."""
        while self.elements:
            priority, _, item = heapq.heappop(self.elements)
            if item is not None:  # Ignora itens removidos
                del self.entry_finder[item]
                return priority, item
        raise KeyError('pop de uma fila vazia')
    
    def empty(self):
        """Retorna True se a fila estiver vazia."""
        return not self.entry_finder