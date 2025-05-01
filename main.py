import numpy as np
from State import State


matriz = np.array([
    [1, 2, 3],
    [0, 4, 6],
    [7, 8, 1]
])

st = State(matriz)

nb = st.getNeighbors()

for n in nb:
    n.printState()
