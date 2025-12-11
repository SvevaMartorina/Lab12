import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_grafo(self, e):
        """Callback per il pulsante 'Crea Grafo'."""
        try:
            anno = int(self._view.txt_anno.value)
        except:
            self._view.show_alert("Inserisci un numero valido per l'anno.")
            return
        if anno < 1950 or anno > 2024:
            self._view.show_alert("Anno fuori intervallo (1950-2024).")
            return

        self._model.build_weighted_graph(anno)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {self._model.G.number_of_nodes()} nodi, {self._model.G.number_of_edges()} archi")
        )
        min_p, max_p = self._model.get_edges_weight_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))
        self._view.page.update()

    def handle_conta_archi(self, e):
        """Callback per il pulsante 'Conta Archi'."""
        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        min_p, max_p = self._model.get_edges_weight_min_max()
        if soglia < min_p or soglia > max_p:
            self._view.show_alert(f"Soglia fuori range ({min_p:.2f}-{max_p:.2f})")
            return

        minori, maggiori = self._model.count_edges_by_threshold(soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Archi < {soglia}: {minori}, Archi > {soglia}: {maggiori}"))
        self._view.page.update()

    """Implementare la parte di ricerca del cammino minimo"""
    def handle_cammino_minimo(self, e):
        """
        Callback per il bottone 'Cammino Minimo'.
        - legge la soglia dalla view
        - verifica che il grafo sia stato costruito
        - chiama i due metodi del Model
        - mostra i cammini minimi nella lista_visualizzazione
        """
        soglia_txt = self._view.txt_soglia.value
        try:
            soglia = float(soglia_txt)
        except (TypeError, ValueError):
            self._view.show_alert("Inserisci un numero valido nel campo soglia.")
            return

        # controlla che il grafo esista già
        if self._model.G is None or self._model.G.number_of_nodes() == 0:
            self._view.show_alert("Prima costruisci il grafo (bottone 'Calcola sentieri').")
            return

        #chiamo i metodi dal model
        cammini_nx, peso_nx = self._model.ricerca_cammino_minimo_nx(soglia)
        cammini_dfs, peso_dfs = self._model.ricerca_cammino_minimo_recursion(soglia)

        # pulisco area risultati
        self._view.lista_visualizzazione.controls.clear()

        # nessun cammino trovato
        if not cammini_dfs:
            self._view.lista_visualizzazione.controls.append(
                ft.Text("Nessun cammino valido trovato (peso > soglia e almeno 2 archi).")
            )
            self._view.page.update()
            return

        # opzionale: controllo che i due metodi diano lo stesso risultato
        #if cammini_nx and abs(peso_nx - peso_dfs) > 1e-6:
        if peso_nx != peso_dfs:
            self._view.lista_visualizzazione.controls.append(
                ft.Text(
                    f"ATTENZIONE: i due algoritmi non coincidono "
                    f"(NetworkX={peso_nx:.2f}, DFS={peso_dfs:.2f})"
                    )
                )

        self._view.lista_visualizzazione.controls.append(
            ft.Text("Cammino minimo:"))

        for idx, path in enumerate(cammini_dfs, start=1):
            if len(cammini_dfs) > 1:
                self._view.lista_visualizzazione.controls.append(
                    ft.Text(f"Cammino #{idx}:")
                )
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]

                # peso dell'arco nel grafo
                peso_arco = self._model.G[u][v]["weight"]

                # ADATTA QUI se i campi del rifugio hanno nomi diversi
                testo_riga = (
                        f"[{u.id_rifugio}] {u.nome} ({u.localita}) "
                        f"--> "
                        f"[{v.id_rifugio}] {v.nome} ({v.localita}) "
                        f"[peso: {peso_arco:.1f}]"
                    )

                self._view.lista_visualizzazione.controls.append(
                        ft.Text(testo_riga))

        self._view.page.update()
    # TODO

