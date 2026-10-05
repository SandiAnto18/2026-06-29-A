import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._graph = nx.DiGraph()

    def getCountry(self):
        return DAO.getAllCountries()

    def buildGraph(self, country):

        self._graph.clear()

        # Clienti del paese selezionato
        customers = DAO.getCustomerByCountry(country)
        self._graph.add_nodes_from(customers)

        # Mappa: CustomerId -> oggetto Customer
        # Serve per trasformare velocemente l'ID restituito dal DAO.getCustomer1Customer2
        # nell'oggetto Customer corrispondente
        #ci serve per c1 e c2 che sono id e non ancora oggetto
        customerMap = {}

        for c in customers:
            customerMap[c.CustomerId] = c

        # Coppie di clienti con almeno un artista in comune
        c1c2 = DAO.getCustomer1Customer2(country)

        for c1, c2, artista in c1c2:

            cliente1 = customerMap[c1]
            cliente2 = customerMap[c2]
            #accedo all'attributo fatturato
            fatturato1 = cliente1.Fatturato
            fatturato2 = cliente2.Fatturato

            # Cliente con fatturato maggiore -> cliente con fatturato minore
            #c1->c2
            if fatturato1 > fatturato2:
                self._graph.add_edge(
                    cliente1,
                    cliente2,
                    weight=fatturato1 + fatturato2
                )
            #c2->c1
            elif fatturato2 > fatturato1:
                self._graph.add_edge(
                    cliente2,
                    cliente1,
                    weight=fatturato1 + fatturato2
                )
            #fatturato uguale c1->c2 e c2->c1
            else:
                self._graph.add_edge(
                    cliente1,
                    cliente2,
                    weight=fatturato1 + fatturato2
                )
                self._graph.add_edge(
                    cliente2,
                    cliente1,
                    weight=fatturato1 + fatturato2
                )

    def getNumNodi(self):
        return len(self._graph.nodes())

    def getNumArchi(self):
        return len(self._graph.edges())


    def getTop5Edges(self):

        edges = sorted(
            self._graph.edges(data=True),
            key=lambda x: x[2]["weight"],
            reverse=True #ORDINE DECRESCENTE
        )

        return edges[:5]

    def getMostInfluential(self):

        maxInfluenza = None
        clienteInfluente = None

        for cliente in self._graph.nodes():

            pesoUscente = 0
            pesoEntrante = 0

            # Sommo i pesi degli archi uscenti
            #out_edges(nodo, data=True) → (nodo partenza, nodo arrivo, dati arco)
            for arco in self._graph.out_edges(cliente, data=True):
                pesoUscente += arco[2]["weight"]
                #Prendi tutti gli archi che partono da questo cliente e somma i loro pesi.

            # Sommo i pesi degli archi entranti
            for arco in self._graph.in_edges(cliente, data=True):
                pesoEntrante += arco[2]["weight"]

            influenza = pesoUscente - pesoEntrante

            # Tengo il cliente con l'influenza più alta trovata finora
            if maxInfluenza is None or influenza > maxInfluenza:
                maxInfluenza = influenza
                clienteInfluente = cliente

        return clienteInfluente, maxInfluenza

