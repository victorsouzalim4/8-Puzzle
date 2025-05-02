from State import State
from collections import deque

def reconstructPath(initialKey, visitedList):
    stack = deque()
    currentKey = initialKey

    while currentKey is not None:
        stack.append(currentKey)
        currentKey = visitedList[currentKey]

    return stack
    

def breadthFirstSearch(initialState):

    visited = {}
    queue = deque()
    predecessor = None

    queue.append(initialState)
    visited[initialState.fromMatrixString()] = predecessor

    
    while queue:
        current = queue.popleft()
        predecessor = current

        if current.fromMatrixString() == '123456780':
            return reconstructPath("123456780", visited)

        for element in current.getNeighbors(): 
            print("entrei")
            if element.fromMatrixString() not in visited:
                queue.append(element)
                visited[element.fromMatrixString()] = predecessor.fromMatrixString()



    

    

