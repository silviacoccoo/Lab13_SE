import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.flag = True

    # Punto 1.4 (il primo bottone)
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
                return

            count_bigger, count_smaller= self._model.count_edges(threshold)

            self._view.lista_visualizzazione_2.controls.clear() # RESET
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

        if self.flag:
            self.flag = False
            try:
                threshold = float(self._view.txt_name.value)
                self._model.ricerca_cammino(threshold)
                self._view.lista_visualizzazione_3.controls.clear()
                self._view.lista_visualizzazione_3.controls.append(
                    ft.Text(f"Numero archi percorso più lungo: {len(self._model.soluzione_best)}"))
                self._view.update()

                self._view.lista_visualizzazione_3.controls.append(ft.Text(
                    f"Peso cammino massimo: {str(self._model.compute_weight_path(self._model.soluzione_best))}"))

                for ii in self._model.soluzione_best:
                    self._view.lista_visualizzazione_3.controls.append(ft.Text(
                        f"{ii[0]} --> {ii[1]}: {str(ii[2]['weight'])}"))
            except ValueError:
                self._view.show_alert("Valore numerico non non valido!")

            self._view.update()

        """
        t_str=self._view.txt_name.value
        if t_str is None:
            self._view.show_alert('Selezionare una squadra!')
            return
        t=float(t_str)
        best_path, best_score=self._model.get_best_solution(t)

        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(
            ft.Text(f'Numero archi percorso più lungo: {len(best_path)}')
        )
        self._view.lista_visualizzazione_3.controls.append(
            ft.Text(f'Peso cammino massimo: {best_score}')
        )
        self._view.update()
        """
        # TODO