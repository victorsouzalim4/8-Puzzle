import numpy as np
from collections import deque

def reconstructPath(initialKey, visitedList):
    stack = deque()
    currentKey = initialKey

    while currentKey is not None:
        stack.append(currentKey)
        currentKey = visitedList[currentKey]

    return stack

def heuristic(matrix):

    manhattanDistanceSum = 0
    
    baseMatrix = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ])

    for (row, col), value in np.ndenumerate(matrix):
        rowB, colB = np.where(baseMatrix == value)
        rowB, colB = int(rowB), int(colB)

        manhattanDistanceSum += abs(rowB - row) + abs(colB - col)
    
    return manhattanDistanceSum
