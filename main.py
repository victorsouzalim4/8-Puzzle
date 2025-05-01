import numpy as np
from State import State
from utils.utils import heuristic


matriz = np.array([
    [2, 6, 3],
    [4, 5, 1],
    [7, 8, 0]
])

st = State(matriz)

nb = st.getNeighbors()

# for n in nb:
#     n.printState()
