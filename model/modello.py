from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = None
        self._nodelist = []
        self._edgelist = []

    def get_year(self):
        return DAO.get_year()

    def get_shape(self, year):
        return DAO.get_shape(year)

    def crea_grafo(self, year, shape):
        self._grafo = nx.DiGraph()

        self._nodelist = DAO.get_nodes(year, shape)
        self._grafo.add_nodes_from(self._nodelist)

        for n1 in self._grafo.nodes:
            for n2 in self._grafo.nodes:
                if n1 != n2 and n1.state == n2.state:
                    if n1.longitude < n2.longitude and not self._grafo.has_edge(n1, n2):
                        peso = n2.longitude - n1.longitude
                        self._grafo.add_edge(n1, n2, weight=peso)
                        self._edgelist.append((n1.id, n2.id, peso))
                    elif n1.longitude > n2.longitude and not self._grafo.has_edge(n2, n1):
                        peso = n1.longitude - n2.longitude
                        self._grafo.add_edge(n2, n1, weight=peso)
                        self._edgelist.append((n2.id, n1.id, peso))
        print(f"Nodi: {len(self._grafo.nodes)}, Archi: {len(self._grafo.edges)}")
        print("5 archi con peso maggiore:")
        self._edgelist.sort(key=lambda x: x[2], reverse=True)
        for i in range(5):
            print(self._edgelist[i])