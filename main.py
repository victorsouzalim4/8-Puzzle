import numpy as np
from State import State
from BFS import breadthFirstSearch

def printFormatted(str):

    for i in range(9):
        print(f"{str[i]} ", end = "")
        if (i+1) % 3 == 0:
            print()


matriz = np.array([
    [8, 6, 7],
    [2, 5, 4],
    [3, 0, 1]
])

st = State(matriz)

stack = breadthFirstSearch(st)

while stack:
    printFormatted(stack.pop())
    print()
