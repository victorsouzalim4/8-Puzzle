import heapq
from collections import deque
import time
from utils.utils import reconstructPath

def aStarSearch(initialState):
    startTime = time.perf_counter() 

    counter = 0
    visited = {}
    heap = []
    predecessor = None
    gScore = {initialState.fromMatrixString(): 0}
    
    heapq.heappush(heap, (initialState.heuristic, 0, initialState))

    visited[initialState.fromMatrixString()] = predecessor

    
    while heap:
        _, currentG, current = heapq.heappop(heap)
        predecessor = current

        if current.fromMatrixString() == '123456780':
            execTime = time.perf_counter() - startTime
            return reconstructPath("123456780", visited), execTime, counter

        for element in current.getNeighbors(): 
            tentativeG = currentG + 1
            if element.fromMatrixString() not in visited and (element.fromMatrixString() not in gScore or tentativeG < gScore[element.fromMatrixString()]):
                counter += 1
                gScore[element.fromMatrixString()] = tentativeG
                f = tentativeG + element.heuristic
                visited[element.fromMatrixString()] = predecessor.fromMatrixString()
                heapq.heappush(heap, (f, tentativeG, element))