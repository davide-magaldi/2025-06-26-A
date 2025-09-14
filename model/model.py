import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph= nx.Graph()
        self.idMap={}
        self.bestSol=[]
        self.bestScore = 0

    def getYears(self):
        return DAO.getYears()

    def buildGraph(self, start, end):
        self.graph.clear()
        nodes = DAO.getNodes()
        for n in nodes:
            for a in range(start, end+1):
                pi = DAO.getPiazzamenti(a, n.circuitId)
                if len(pi) != 0:
                    n.addPiazzamenti(a, pi)
            self.idMap[n.circuitId]=n
        self.graph.add_nodes_from(nodes)
        edges = DAO.getEdges(start, end)
        for e in edges:
            self.graph.add_edge(self.idMap[e[0]], self.idMap[e[1]], weight=e[2])

    def getMaxConn(self):
        max_comp = []
        max_len = 0
        max_weights = {}
        for c in nx.connected_components(self.graph):
            if len(c) > max_len:
                max_len = len(c)
                max_comp = list(c)
        for n in max_comp:
            max_weight = 0
            for ne in nx.neighbors(self.graph, n):
                if self.graph.get_edge_data(n, ne)['weight'] > max_weight:
                    max_weight = self.graph.get_edge_data(n, ne)['weight']
            max_weights[n] = max_weight
        return max_comp, max_weights

    def getInfo(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()

    def getBestSol(self, k, m):
        self.bestSol = []
        self.bestScore=0
        comp, pesi = self.getMaxConn()
        nodi = []
        for n in comp:
            if len(n.ris.items()) >= m:
                nodi.append(n)
        for n in nodi:
            parziale = [n]
            self.findNext(parziale, k, nodi)

    def findNext(self, parziale, k, nodi):
        if len(parziale) == k:
            score = self.getScore(parziale)
            if score > self.bestScore:
                self.bestScore = score
                self.bestSol = copy.deepcopy(parziale)
            return

        for n in nodi:
            for gara in n.res:
                if (n.circuitId, gara[0]) not in parziale:
                    parziale.append((n.circuitId, gara[0]))
                    self.findNext(parziale, k, nodi)
                    parziale.pop()

    def getScore(self, sol):
        itot = 0
        for gara in sol:
            circuito = self.idMap[gara[0]]
            tot = 0
            np = 0
            for p in circuito.res[gara[1]]:
                if p.position != "" or p.position is not None:
                    np += 1
                tot += 1
            i = 1 - np/tot
            itot += i
        return itot



