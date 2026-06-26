from copy import deepcopy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap={}
        self.best_path=None
        self.best_weight=None
        pass

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategorie(self):
        return DAO.getCategorie()

    def getNodi(self,cate_id):
        return DAO.getNodi(cate_id)

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def buildGrafo(self,cat_id,data_inizio,data_fine):
        self._grafo.clear()
        for nodo in self.getNodi(cat_id):
            self._grafo.add_node(nodo)
            self._idMap[nodo.product_id]=nodo

        archi = DAO.getArchi(cat_id,data_inizio,data_fine,self._idMap)
        for arco in archi:
            vendite1 = arco.vendite_nodo1
            vendite2 = arco.vendite_nodo2
            peso = vendite1+vendite2
            if vendite1 > vendite2:
                self._grafo.add_edge(arco.nodo1,arco.nodo2,weight=peso)
            elif vendite1 == vendite2:
                self._grafo.add_edge(arco.nodo1, arco.nodo2, weight=peso)
                self._grafo.add_edge(arco.nodo2, arco.nodo1, weight=peso)
            else:
                self._grafo.add_edge(arco.nodo2, arco.nodo1, weight=peso)





    def getTop5(self):
        punteggio_nodi = []
        for nodo in self._grafo.nodes():
            peso_uscente = self._grafo.out_degree(nodo,weight='weight')
            peso_entrante = self._grafo.in_degree(nodo,weight='weight')
            punteggio = peso_uscente - peso_entrante
            punteggio_nodi.append((nodo,punteggio))

        punteggio_nodi.sort(key=lambda x : x[1] , reverse=True)
        return punteggio_nodi[:5]

    def cammino_ottimo(self,start,end,lun):
        self.best_path=None
        self.best_weight=-877686786876886586586856856856
        
        # Convertiamo start ed end da ID (stringhe/interi) agli oggetti Prodotto effettivi nel grafo
        from model.prodotto import Prodotto
        #start_node = self._idMap[int(start)] if not isinstance(start, Prodotto) else start
        #end_node = self._idMap[int(end)] if not isinstance(end, Prodotto) else end
        if isinstance(start, Prodotto):
            start_node = start
        else:
            start_node = self._idMap[int(start)]

        if isinstance(end, Prodotto):
            end_node = end
        else:
            end_node = self._idMap[int(end)]
        
        parziale = [start_node]
        self._cerca_ricorsione(parziale,end_node,lun)
        return self.best_path

    def _cerca_ricorsione(self,parziale,end,lun):
        ultimo = parziale[-1]
        #condizione di terminazione
        # Un cammino di lunghezza "lun" (in termini di archi) ha "lun + 1" nodi.
        if len(parziale) == lun + 1:
            if ultimo == end:
                somma = 0
                for i in range(len(parziale) - 1):
                    somma+=self._grafo[parziale[i]][parziale[i+1]]['weight']
                if somma > self.best_weight:
                    self.best_weight = somma
                    self.best_path = deepcopy(parziale)
            return
        
        # Usiamo i successori/vicini del nodo (oggetti Prodotto) e non gli archi (tuple)
        for prossimo in self._grafo.successors(ultimo):
            if prossimo not in parziale:
                parziale.append(prossimo)
                self._cerca_ricorsione(parziale,end,lun)
                parziale.pop()







