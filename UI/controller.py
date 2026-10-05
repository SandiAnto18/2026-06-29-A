import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDCountry(self):
        countries = self._model.getCountry()
        for c in countries:
            self._view._ddCountry.options.append(ft.dropdown.Option(c))

        self._view.update_page()
    def handleCreaGrafo(self, e):
        country= self._view._ddCountry.value
        self._model.buildGraph(country)
        # SVUOTO I RISULTATI PRECEDENTI
        self._view._txt_result.controls.clear()
        # MOSTRO NUMERO DI NODI E ARCHI
        self._view._txt_result.controls.append(
            ft.Text("Grafo correttamente creato:")
        )

        self._view._txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}")
        )

        self._view._txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}")
        )


        self._view.update_page()
    def handleStampaInfo(self,e):
        pass


    def handleSequenza(self,e):
        pass