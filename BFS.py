from State import State
from collections import deque
from utils.utils import reconstructPath

def breadthFirstSearch(initialState):
    counter = 0
    visited = {}
    queue = deque()
    predecessor = None

    queue.append(initialState)
    visited[initialState.fromMatrixString()] = predecessor

    
    while queue:
        current = queue.popleft()
        predecessor = current

        if current.fromMatrixString() == '123456780':
            print(counter)
            return reconstructPath("123456780", visited)

        for element in current.getNeighbors():
            if element.fromMatrixString() not in visited:
                counter += 1
                queue.append(element)
                visited[element.fromMatrixString()] = predecessor.fromMatrixString()



    

    

