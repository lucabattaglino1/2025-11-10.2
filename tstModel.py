# tstModel.py
from model.model import Model

mdl = Model()
mdl.buildGraph(5, 'Rowlett Bikes')
print(f"Nodi: {mdl.getNumNodes()}")
print(f"Archi: {mdl.getNumEdges()}")
