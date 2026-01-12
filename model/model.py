import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        # Punto 1.1: richiede di creare un grafo semplice orientato e pesato
        self.G=nx.DiGraph()
        self._nodes=[]
        self._edges=[]

        self._lista_cromosomi=[]
        self._lista_geni=[]

        self.id_map={}

        self._lista_geni_connessi=[]

        # Inizializzo già i metodi che andrò a definire
        self.load_cromosomi()
        self.load_geni()
        self.load_geni_connessi()

    def load_cromosomi(self):
        self._lista_cromosomi=DAO.get_cromosomi()
        # Questo metodo raccoglie tutti i cromosomi chiamando il DAO, il quale interagisce con il database

    def load_geni(self):
        self._lista_geni=DAO.get_geni() # Lista di oggetti

        self.id_map={} # RESET

        for gene in self._lista_geni:
            self.id_map[gene.id]=gene.cromosoma

    def load_geni_connessi(self):
        self._lista_geni_connessi=DAO.get_geni_connessi()

    def build_graph(self):

        # COME PRIMA AZIONE E' NECESSARIO PULIRE IL GRAFO
        self.G.clear()
        # BISOGNA RESETTARE ANCHE I NODI E GLI ARCHI
        self._nodes=[]
        self._edges=[]

        # Punto 1.1
        for cromosoma in self._lista_cromosomi:
            self._nodes.append(cromosoma) # Ogni cromosoma viene aggiunto alla lista di nodi
        self.G.add_nodes_from(self._nodes)

        # Punto 1.2 e 1.3
        # Abbiamo visto che la lista dei geni connessi contiene il gene1, il gene2, la correlazione che i due hanno,
        # e verifica la condizione che i cromosomi associati siano diversi

        edges={}
        for g1, g2, corr in self._lista_geni_connessi:
            if (self.id_map[g1.id], self.id_map[g2.id]) not in edges:
                edges[(self.id_map[g1.id], self.id_map[g2.id])]=float(corr)
            else:
                edges[(self.id_map[g1.id], self.id_map[g2.id])]+=float(corr)

        for key, value in edges.items():
            self._edges.append((key[0], key[1], value))

        self.G.add_weighted_edges_from(self._edges)

    # Punto 1.4
    def get_num_nodes(self):
        return self.G.number_of_nodes()

    def get_num_edges(self):
        return self.G.number_of_edges()

    def get_nodes(self):
        return self.G.nodes()

    def get_edges(self):
        return list(self.G.edges(data=True))

    def get_min_weight(self):
        return min([x[2]['weight'] for x in self.get_edges()])

    def get_max_weight(self):
        return max([x[2]['weight']for x in self.get_edges()])

    # Punto 1.6
    def count_edges(self, t):
        count_bigger = 0
        count_smaller = 0
        for x in self.get_edges():  # 1. Iterazione
            if x[2]['weight'] > t:  # 2. Confronto Maggiore
                count_bigger += 1
            elif x[2]['weight'] < t:  # 3. Confronto Minore
                count_smaller += 1
        return count_bigger, count_smaller  # 4. Return

