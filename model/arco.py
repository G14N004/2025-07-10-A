from dataclasses import dataclass

from model.prodotto import Prodotto


@dataclass
class Arco:
    nodo1:Prodotto
    vendite_nodo1:int
    nodo2:Prodotto
    vendite_nodo2:int
