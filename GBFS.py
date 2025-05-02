import heapq
from collections import deque
from utils.utils import reconstructPath
import time

def greedyBestFirstSearch(initialState):
    startTime = time.perf_counter() 

    counter = 0
    visited = {}
    heap = []
    predecessor = None
    
    heapq.heappush(heap, (initialState.heuristic, initialState))

    visited[initialState.fromMatrixString()] = predecessor

    
    while heap:
        _, current = heapq.heappop(heap)
        predecessor = current

        if current.fromMatrixString() == '123456780':
            execTime = time.perf_counter() - startTime
            return reconstructPath("123456780", visited), execTime, counter

        for element in current.getNeighbors(): 
            if element.fromMatrixString() not in visited:
                counter += 1
                heapq.heappush(heap, (element.heuristic, element))
                visited[element.fromMatrixString()] = predecessor.fromMatrixString()