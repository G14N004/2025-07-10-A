import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillddcategory(self):
        categorie = self._model.getCategorie()
        for cat in categorie:
            self._view._ddcategory.options.append(ft.dropdown.Option(key=cat.category_id , text=cat.category_name))
        self._view.update_page()


    def handleCreaGrafo(self, e):
        try:
            if not self._view._ddcategory.value or not self._view._dp1.value or not self._view._dp2.value:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"selezione una categoria/data"))
                return

            categoria_id = int(self._view._ddcategory.value)
            data1=str(self._view._dp1.value)
            data2=str(self._view._dp2.value)
            data_inizio= min(data1, data2)
            data_fine=max(data1, data2)
            self._model.buildGrafo(categoria_id,data_inizio,data_fine)
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(
                    f"Grafo correttamente creato.\n Nodi: {self._model.getNumNodi()} nodi e {self._model.getNumArchi()} archi ")
            )

            self._view.txt_result.controls.append(ft.Text(f"i 5 prodotti più venduti sono : "))
            for elm in self._model.getTop5():
                self._view.txt_result.controls.append(ft.Text(f"{elm[0]} -- score : {elm[1]}"))
            self._view.update_page()

            self._view._ddProdStart.options.clear()
            self._view._ddProdEnd.options.clear()

            nodi = list(self._model._grafo.nodes())
            for nodo in nodi :
                self._view._ddProdStart.options.append(ft.dropdown.Option(key=nodo.product_id, text=nodo.product_name))
                self._view._ddProdEnd.options.append(ft.dropdown.Option(key=nodo.product_id, text=nodo.product_name))
            self._view.update_page()
        except AttributeError:

            pass

    def handleBestProdotti(self, e):
        pass

    def handleCercaCammino(self, e):
        start = self._view._ddProdStart.value
        end = self._view._ddProdEnd.value
        if not start or not end:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un prodotto di partenza e di arrivo."))
            self._view.update_page()
            return

        try:
            lun_str = self._view._txtInLun.value
            if not lun_str:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"Inserire una lunghezza per il cammino."))
                self._view.update_page()
                return
            lun = int(lun_str)
            if lun <= 0:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"La lunghezza del cammino deve essere un intero positivo."))
                self._view.update_page()
                return

            cammino = self._model.cammino_ottimo(start,end,lun)
            if cammino is None:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"Nessun cammino trovato per i parametri scelti."))
                self._view.update_page()
            else:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"Somma dei pesi : {self._model.best_weight}"))
                for p in cammino :
                    self._view.txt_result.controls.append(ft.Text(f"{p}"))
                self._view.update_page()
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Inserire un valore numerico valido per la lunghezza."))
            self._view.update_page()
        except Exception as ex:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Errore: {ex}"))
            self._view.update_page()


        pass



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
