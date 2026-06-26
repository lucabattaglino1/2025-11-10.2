import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # CONTROLLER
    def fillDDStores(self):
        store = self._model.getStores()
        for s in store:
            self._view._ddStore.options.append(ft.dropdown.Option(str(s.store_name)))
        self._view.update_page()

    def handleCreaGrafo(self, e):

        store = self._view._ddStore.value
        k = self._view._txtIntK.value

        if store is None:
            self._view.create_alert("Seleziona un valore")
            return

        if k is None:
            self._view.create_alert("Seleziona un valore")
            return

        self._model.buildGraph(k, store)

        # pulisco la lista risultati
        self._view.txt_result.controls.clear()

        # stampo le info
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi."))

        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore:"))
        for a1, a2, peso in self._model.getTopArchi():
            self._view.txt_result.controls.append(ft.Text(f"{a1.order_id} -> {a2.order_id} ({peso}) "))

        # AGGIUNGO I NODI AL DROPDOWN
        for n in self._model._nodes:
            self._view._ddNode.options.append(ft.dropdown.Option(key=str(n.order_id), text=str(n.order_id)))
        self._view._ddNode.disabled = False
        self._view._btnCerca.disabled = False
        self._view.update_page()



    def handleCerca(self, e):
        if self._view._ddNode.value is None:
            self._view.create_alert("Seleziona un nodo")
            return

        nodo = self._model._idMapAO[int(self._view._ddNode.value)]
        cammino = self._model.getCamminoLungo(nodo)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino più lungo ({len(cammino)} nodi):"))
        for n in cammino:
            self._view.txt_result.controls.append(ft.Text(f"Ordine {n.order_id}"))

        self._view.update_page()

    def handleRicorsione(self, e):
        pass