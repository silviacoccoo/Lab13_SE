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

        self.soluzione_best=[]
        # self.best_costo=0


    def load_cromosomi(self):
        self._lista_cromosomi=DAO.get_cromosomi()
        # Questo metodo raccoglie tutti i cromosomi chiamando il DAO, il quale interagisce con il database

    def load_geni(self):
        self._lista_geni=DAO.get_geni() # Lista di oggetti

        self.id_map={} # Un dizionario che avrà come chiave l'id del gene e come valore associato il cromosoma

        for gene in self._lista_geni:
            self.id_map[gene.id]=gene.cromosoma # associo al gene il cromosoma

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
            if (self.id_map[g1], self.id_map[g2]) not in edges: # Se non si trova ancora nel dizionario
                edges[(self.id_map[g1], self.id_map[g2])]=float(corr)
                # Associa la tupla dei due id al valore di correlazione
            else:
                edges[(self.id_map[g1], self.id_map[g2])]+=float(corr)


        # Una volta terminato il ciclo aggiungo, sempre con un ciclo, alla lista self._edges le tuple di valori
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
        # t è il valore soglia inserito
        count_bigger = 0
        count_smaller = 0
        for x in self.get_edges():  # 1. Iterazione
            if x[2]['weight'] > t:  # 2. Confronto Maggiore
                count_bigger += 1
            elif x[2]['weight'] < t:  # 3. Confronto Minore
                count_smaller += 1
        return count_bigger, count_smaller  # 4. Return

    # A partire dal grafo calcolato al punto precedente,
    # alla pressione del tasto “Ricerca Cammino”, si avvii una procedura di ricerca ricorsiva per
    # determinare il cammino di vertici (cromosomi) del grafo che
    # massimizza il costo complessivo,
    # calcolato come somma dei costi associati agli archi (o ai vertici)
    # che sia composto esclusivamente da archi di peso >S.
    # Il costo del cammino sarà valutata dalla somma dei pesi degli archi incontrati.
    # Si visualizzi nella GUI la sequenza di cromosomi dal peso massimo così ottenuto.

    def ricerca_cammino(self, t):
        self.soluzione_best.clear()

        for n in self.get_nodes():
            partial = []
            partial_edges = []

            partial.append(n)
            self.ricorsione(partial, partial_edges, t)

        print("final", len(self.soluzione_best), [i[2]["weight"] for i in self.soluzione_best])

    def ricorsione(self, partial_nodes, partial_edges, t):
        n_last = partial_nodes[-1]
        neigh = self._get_admissible_neighbors(n_last, partial_edges, t)

        # stop
        if len(neigh) == 0:
            weight_path = self.compute_weight_path(partial_edges)
            weight_path_best = self.compute_weight_path(self.soluzione_best)
            if weight_path > weight_path_best:
                self.soluzione_best = partial_edges[:]
            return

        for n in neigh:
            print("...")
            partial_nodes.append(n)
            partial_edges.append((n_last, n, self.G.get_edge_data(n_last, n)))
            self.ricorsione(partial_nodes, partial_edges, t)
            partial_nodes.pop()
            partial_edges.pop()

    def _get_admissible_neighbors(self, node, partial_edges, soglia):
        result = []
        for u, v, data in self.G.out_edges(node, data=True):
            if data["weight"] > soglia:
                # controllo SOLO l'arco diretto
                if (u, v) not in [(x[0], x[1]) for x in partial_edges]:
                    result.append(v)
        return result

    @staticmethod
    def compute_weight_path(mylist):
        weight = 0
        for e in mylist:
            weight += e[2]['weight']
        return weight

    """
        def get_best_solution(self,t):
        Prepara i dati e lancia la ricorsione
        self.best_soluzione=[]
        self.best_costo=0

        # Non sappiamo il nodo di partenza, allora proviamo a far partire la ricorsione da ogni nodo del grafo
        for node in self.get_nodes():
            parziale=[node]
            self.ricorsione(parziale,t)

        return self.best_soluzione,self.best_costo

    def ricorsione(self, parziale, t):
        costo_attuale=self.calcola_costo_complessivo(parziale)

        # Controllo se è una soluzione migliore
        if costo_attuale > self.best_costo:
            self.best_costo=costo_attuale
            self.best_soluzione=list(parziale)
        # Caso ricorsivo
        ultimo_nodo=parziale[-1]
        vicini=self.G[ultimo_nodo] #self.G.neighbors(ultimo_nodo)
        for vicino in vicini:
            weight=self.G[ultimo_nodo][vicino]['weight']

            # Condizione 1
            if weight > t:
                # Condizione 2: non devo creare cicli (il vicino non deve essere già in parziale)
                if vicino not in parziale:
                    parziale.append(vicino)
                    self.ricorsione(parziale, t)
                    parziale.pop()


    def calcola_costo_complessivo(self,lista_nodi):
        costo=0.0
        # itero su indici da 0 a penultimo
        for i in range(len(lista_nodi)-1):
            u=lista_nodi[i]
            v=lista_nodi[i+1]
            try:
                peso=self.G[u][v]['weight']
                costo+=peso # somma dei pesi degli archi incontrati
            except KeyError:
                return 0
        return costo
    """
