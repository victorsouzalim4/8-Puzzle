import numpy as np

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
