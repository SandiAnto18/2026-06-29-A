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

        # CLIENTE PIù INFLUENTE (INFLUENZA = PESO ARCHI USCENTI - PESO ARCHI ENTRANTI)
        cliente, influenza = self._model.getMostInfluential()

        self._view._txt_result.controls.append(
            ft.Text(
                f"Cliente più influente: {cliente.FirstName} {cliente.LastName} ({cliente.Country}) - (Influenza: {influenza})"
            )
        )
        # RECUPERO I 5 ARCHI CON PESO MAGGIORE
        top5 = self._model.getTop5Edges()

        self._view._txt_result.controls.append(
            ft.Text("Top 5 archi con peso maggiore:")
        )

        # STAMPO I 5 ARCHI
        #mi serve customer come oggetto per recuperare gli attributi nome, cognome e paese
        #Enumero i 5 archi a partire da 1
        for i,(c1, c2, w) in enumerate (top5,1):
            self._view._txt_result.controls.append(
                ft.Text(
                    f"{i}.{c1.FirstName} {c1.LastName} ({c1.Country}) -> "
                    f"{c2.FirstName} {c2.LastName} ({c2.Country}) " 
                    f"(peso:{w['weight']})"
                )
            )


        self._view.update_page()
    def handleSequenza(self,e):
        pass