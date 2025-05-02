import heapq
from collections import deque
from utils.utils import reconstructPath

def greedyBestFirstSearch(initialState):
    visited = {}
    heap = []
    predecessor = None
    
    heapq.heappush(heap, (initialState.heuristic, initialState))

    visited[initialState.fromMatrixString()] = predecessor

    
    while heap:
        _, current = heapq.heappop(heap)
        predecessor = current

        if current.fromMatrixString() == '123456780':
            return reconstructPath("123456780", visited)

        for element in current.getNeighbors(): 
            print("entrei")
            if element.fromMatrixString() not in visited:
                heapq.heappush(heap, (element.heuristic, element))
                visited[element.fromMatrixString()] = predecessor.fromMatrixString()