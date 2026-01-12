import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    # Punto 1.4
    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """""
        # Creo il grafo
        self._model.build_graph()

        self._view.lista_visualizzazione_1.controls.clear() # RESET

        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f'Numero di vertici {self._model.get_num_nodes()} Numero archi: {self._model.get_num_edges()}')
        )
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f'Informazioni sui pesi degli archi - valore minimo: {self._model.get_min_weight()} e valore massimo: {self._model.get_max_weight()}')
        )

        self._view.update() # RICORDARSI DI AGGIORNARE
        # TODO

    # Punto 1.5 e 1.6
    def handle_conta_edges(self, e):
        """ Handler per gestire il conteggio degli archi """""
        self._view.lista_visualizzazione_2.controls.clear() # RESET
        try:
            threshold=float(self._view.txt_name.value)

            if threshold < 3 or threshold > 7:
                self._view.show_alert('Valore fuori dalla soglia')

            count_bigger, count_smaller= self._model.count_edges(threshold)

            self._view.lista_visualizzazione_2.controls.append(
                ft.Text(f'Numero archi con peso maggiore della soglia: {count_bigger}')
            )
            self._view.lista_visualizzazione_2.controls.append(
                ft.Text(f'Numero archi con peso minore della soglia: {count_smaller}')
            )
        except ValueError:
            self._view.show_alert('Valore numerico non valido!')

        self._view.update() # AGGIORNARE LA PAGINA
        # TODO

    def handle_ricerca(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """""
        # TODO