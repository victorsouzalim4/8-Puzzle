import numpy as np
from utils.utils import heuristic

class State:
    def __init__(self, currentState):
        self.currentState = currentState
        self.heuristic = heuristic(currentState)
 
    def printState(self):
        n = 3
        for i in range(n):
            for j in range(n):
                print(f"{self.currentState[i][j]} ", end="")
            print()
        print()

    def fromMatrixString(self):
        state = ""
        for line in self.currentState:
            for element in line:
                state += str(element)
        return state
    
    def getNeighbors(self):

        neighbours = []

        row, col = np.where(self.currentState == 0)
        row, col = int(row), int(col)

        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        for dRow, dCol in directions:
            newRow = dRow + row
            newCol = dCol + col
            
            if 0 <= newRow < 3 and 0 <= newCol < 3:
                newState = self.currentState.copy()
                newState[row, col], newState[newRow, newCol] = newState[newRow, newCol], newState[row, col]
                neighbours.append(State(newState))

        return neighbours
    
    def __lt__(self, other):
        return self.fromMatrixString() < other.fromMatrixString()