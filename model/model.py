import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
    def getCountry(self):
        return DAO.getAllCountries()
    def buildGraph(self,country):
        self._graph.clear()

        #CLIENTI X PAESE SELEZIONATO
        customers = DAO.getCustomerByCountry(country)
        for c in customers:
            print (c) # VERIFICA QUANDO RUNNO NEL MAIN

        self._graph.add_nodes_from(customers)

        # CLIENTE CON FATTURATO TOT
        fatturati= DAO.getCustomerbyFatturato(country)
        for cliente,TotFatt in fatturati:
            print(cliente,TotFatt)
        #ASSOCIO AD OGNI CLIENTE IL SUO FATTURATO
        #creo una mappa:
        #chiave(key):customerID
        # valore(item): fatturato totale
        fatturato={}
        for cliente,TotFatt in fatturati:
            #al contrario perchè stiamo costruendo la mappa
            fatturato[cliente]=TotFatt

        #COPPIE CLIENTI CON ARTISTA IN COMUNE
        c1c2= DAO.getCustomer1Customer2(country)
        for c1,c2,artista in c1c2:
            print (c1,c2,artista)
        for c1,c2,artista in c1c2:
            fatturato1= fatturato[c1]
            fatturato2= fatturato[c2]
            print(c1, fatturato1, c2, fatturato2)
        #SCEGLIAMO IL VERSO E AGGIUNGIAMO L'ARCO
        #c1->c2
            if fatturato1>fatturato2:
                self._graph.add_edge(c1,c2,weight=fatturato1+fatturato2)
        #c2->c1
            elif fatturato2>fatturato1:
                self._graph.add_edge(c2,c1,weight=fatturato1+fatturato2)
        #c1->c2 e c2->c1
            else:
                self._graph.add_edge(c1, c2, weight=fatturato1 + fatturato2)
                self._graph.add_edge(c2, c1, weight=fatturato1 + fatturato2)



    # RESTITUISCO IL NUMERO DI NODI DEL GRAFO
    def getNumNodi(self):
            return len(self._graph.nodes())

    def getNumArchi(self):
        return len(self._graph.edges())