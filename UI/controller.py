import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYear(self):
        years = self._model.getYears()
        for y in years:
            self._view._ddYear1.options.append(ft.dropdown.Option(y))

    def fillDDYear2(self):
        years = self._model.getYears()
        for y in years:
            self._view._ddYear2.options.append(ft.dropdown.Option(y))

    def handleBuildGraph(self, e):
        start = self._view._ddYear1.value
        end = self._view._ddYear2.value
        if start is None or start == "" or end is None or end == "":
            self._view.create_alert("Selezionare gli anni!")
            return
        start = int(start)
        end = int(end)
        self._model.buildGraph(start, end)
        self._view._btnPrintDetails.disabled=False
        self._view._btnCalcolaSoluzione.disabled=False
        nnodes, nedges = self._model.getInfo()
        self._view._txtGraphDetails.controls.clear()
        self._view._txtGraphDetails.controls.append(ft.Text(f"Grafo creato correttamente con {nnodes} nodi e {nedges} archi"))
        self._view.update_page()

    def handlePrintDetails(self, e):
        cc, max_weights = self._model.getMaxConn()
        cc.sort(key=lambda n: max_weights[n], reverse=True)
        for n in cc:
            self._view._txtGraphDetails.controls.append(ft.Text(f"{n.__str__()} - {max_weights[n]}"))
        self._view.update_page()


    def handleCercaDreamChampionship(self, e):
        pass


