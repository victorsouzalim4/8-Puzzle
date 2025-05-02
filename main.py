import numpy as np
from State import State
from BFS import breadthFirstSearch
from GBFS import greedyBestFirstSearch
from aStarSearch import aStarSearch

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

stack, execTime, expandedNodes = aStarSearch(st)
print(f"Solution path lenght: {len(stack) - 1}")
print(f"Execution time: {execTime:.4f}s")
print(f"Number of visited states: {expandedNodes}")

# while stack:
#     printFormatted(stack.pop())
#     print()
