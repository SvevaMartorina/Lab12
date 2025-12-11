import math

import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self._connessioni = None
        self._lista_pesi = []
        self._lista_rifugi = []
        self._dizionario_rifugi = {}
        # TODO

    def get_all_rifugio(self):
        rifugio = DAO.getAllRifugio()
        self._lista_rifugi = rifugio #lista con tutti i rifugi del database
        for rifugio in self._lista_rifugi:
            self._dizionario_rifugi[int(rifugio.id_rifugio)] = rifugio


    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # reset strutture
        self.G.clear()
        self._lista_pesi.clear()
        self._connessioni = None

        #carico i rifugi e popolo il dizionario
        self.get_all_rifugio()

        connessioni = DAO.readAllConnection(year)
        self._connessioni = connessioni

        for c in self._connessioni:
            id1 = int(c.id_rifugio1)
            id2 = int(c.id_rifugio2)

            # se l'id non esiste nel dizionario, salta quella connessione
            if id1 not in self._dizionario_rifugi or id2 not in self._dizionario_rifugi:
                print("ID non trovato nel dizionario:", c.id_rifugio1, c.id_rifugio2)
                continue

            u_nodo = self._dizionario_rifugi[id1]
            v_nodo = self._dizionario_rifugi[id2]

            if c.difficolta == 'facile':
                fattore = 1
            elif c.difficolta == 'media':
                fattore = 1.5
            elif c.difficolta == 'difficile':
                fattore = 2
            else:
                fattore = 0

            # peso dell'arco: distanza * fattore_difficolta
            peso_arco = float(c.distanza) * fattore
            self._lista_pesi.append(peso_arco)
            # Aggiungo direttamente l'arco (NetworkX crea i nodi se non ci sono), con il peso calcolato in precedenza
            self.G.add_edge(u_nodo, v_nodo, weight= peso_arco)

        # TODO

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        if not self._lista_pesi:
            return None, None

        min_peso = min(self._lista_pesi)
        max_peso = max(self._lista_pesi)
        return min_peso, max_peso
        # TODO

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: num archi con peso < soglia
        :return maggiori: num archi con peso > soglia
        """
        minori = 0
        maggiori = 0
        for peso in self._lista_pesi:
            if peso < soglia:
                minori += 1
            if peso > soglia:
                maggiori += 1

        return minori, maggiori
        # TODO

    """Implementare la parte di ricerca del cammino minimo"""
    #creo un sottografo con solamente i nodi utilizzabili (peso maggiore della soglia)
    def get_subgraph_over_threshold(self, soglia):
        H = nx.Graph()
        H.add_nodes_from(self.G.nodes())  # stessi nodi del grafo originale

        for u, v, data in self.G.edges(data=True): # data è un dizionario con gli attributi dell'arco
            if data["weight"] > soglia:
                H.add_edge(u, v, weight=data["weight"]) #aggiungo l'arco anche nel sottografo
        return H #grafo filtrato, con solo archi con peso superiore alla soglia

    def ricerca_cammino_minimo_nx(self, soglia):
        #METODO 2: networkx
        """
            Ricerca TUTTI i cammini di peso minimo globale che:
               - sono composti solo da archi con peso > soglia
               - contengono almeno 2 archi (almeno 3 nodi)

            :param soglia: soglia sui pesi degli archi
            :return: (lista_cammini, peso_minimo)
                    lista_cammini = [ [n1, n2, ..., nk], ... ]
                    peso_minimo = float, oppure None se non esiste cammino valido
               """
        #controllo sul grafo originale
        if self.G is None or self.G.number_of_nodes() == 0:
            return [], None

        H = self.get_subgraph_over_threshold(soglia) #sottografo filtrato

        #controllo sul sottografo
        if H.number_of_edges() == 0:
            return [], None

        #inizializzo le variabili
        best_weight = math.inf
        best_paths = []

        # per ogni nodo, faccio Dijkstra su H
        for sorgente in H.nodes:
            try:
                #crea un dizionario che contiene distanza minima e cammino minimo
                lengths, paths = nx.single_source_dijkstra(
                    H, source=sorgente, weight="weight"
                )
                #da una sorgente otteniamo tutti i cammini minimi
                #verso tutti gli altri nodi raggiungibili.
            except nx.NetworkXNoPath:
                continue

            for destinazione, dist in lengths.items():
                if destinazione == sorgente: #lunghezza cammino 0
                    continue

                path = paths[destinazione] #lista di nodi

        # vincolo: almeno 2 archi → almeno 3 nodi
                if len(path) < 3: #se è più conto si ignora
                    continue

                if dist < best_weight: #se il peso del nuovo cammino è minore aggiorno:
                    best_weight = dist #il miglior peso
                    best_paths = [path] #azzero, mettendo solo il cammino appena trovato

                elif dist == best_weight: #è un altro cammino con lo stesso peso
                    best_paths.append(path) #lo aggiungo alla lista


            if best_weight == math.inf:
                return [], None

        #avendo lanciato Dijkstra da tutte le sorgenti, posso avere tuple di cammini duplicati
            cammini_unici = []
            visti = set()
            for p in best_paths:
                forward_ids = tuple(n.id_rifugio for n in p) #tupla originale
                backward_ids = tuple(reversed(forward_ids)) #tupla al contrario che continene gli stessi cammini in n altro ordine
                chiave = min(forward_ids, backward_ids) #ordine lessicografico
                if chiave not in visti: #se il cammino non è stato ancora aggiunto, lo agiungo
                    visti.add(chiave)
                    cammini_unici.append(p)

            return cammini_unici, best_weight


    def ricerca_cammino_minimo_recursion(self, soglia):
        """
        Ricerca TUTTI i cammini di peso minimo globale che:
            - usano solo archi con weight > soglia
            - hanno almeno 2 archi (>= 3 nodi)
            - non contengono cicli (cammini semplici)

            :param soglia: soglia sui pesi degli archi
            :return: (lista_cammini, peso_minimo)
               """
        #controllo sul grafo iniziale
        if self.G is None or self.G.number_of_nodes() == 0:
            return [], None

        H = self.get_subgraph_over_threshold(soglia)

        #controllo sul sottografo
        if H.number_of_edges() == 0:
            return [], None

        #inizializzo le variabili
        best_cost = math.inf
        best_paths = []

        def dfs(nodo, visited, path, costo):
            nonlocal best_cost, best_paths
            #nodo = nodo corrente.
            #visited = insieme dei nodi già visitati in questo cammino (serve per evitare cicli).
            #path = lista dei nodi del cammino corrente.
            #costo = somma dei pesi degli archi percorsi finora

            # Se ho almeno 2 archi (=> 3 nodi), il cammino è candidato
            if len(path) >= 3:
                if costo < best_cost: #se il peso è minore del miglior peso aggiorno:
                    best_cost = costo #peso migliore
                    best_paths = [list(path)] #percorso migliore
                elif costo == best_cost: #è un altro cammino con ugual peso
                    best_paths.append(list(path)) #aggiungo il percorso alla lista
            if costo >= best_cost:
                return

            for vicino in H.neighbors(nodo): #Per ogni nodo vicino che posso raggiungere da nodo
                if vicino in visited: #se ho già visitato il vicino, vado avanti
                    continue
                peso = H[nodo][vicino]["weight"] #distanza tra un nodo e il suo vicino (peso dell'arco)

                visited.add(vicino) #aggiungo il nodo alla lista dei visitati
                path.append(vicino) #aggiungo il nodo al percorso
                # richiamo la funzione
                # vicino diventa il nodo corrente
                # il vicino viene aggiunto ai nodi visitati
                # il cammino (path) viene aggiornato aggiungendo il vicino
                # il costo totale viene aggiornato aggiungendo il peso di questo arco
                dfs(vicino, visited, path, costo + peso)
                #faccio “backtracking”: tolgo il nodo da path e da visited.
                path.pop()
                visited.remove(vicino)

        # lancio la DFS da ogni nodo come sorgente
        for start in H.nodes:
            visited = {start}
            dfs(start, visited, [start], 0.0)

        if best_cost == math.inf:
            return [], None

            #avendo applicato la ricorsione da tutte le sorgenti, posso avere tuple di cammini duplicati
        cammini_unici = []
        visti = set()
        for p in best_paths:
            forward_ids = tuple(n.id_rifugio for n in p)  #tupla percorso originale
            backward_ids = tuple(reversed(forward_ids))  #tupla percorso in un altro ordine
            chiave = min(forward_ids, backward_ids)
            if chiave not in visti: #se non ho ancora aggiunto il percorso
                visti.add(chiave)
                cammini_unici.append(p)

        return cammini_unici, best_cost


    # TODO
