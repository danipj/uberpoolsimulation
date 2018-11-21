import fileinput
from collections import defaultdict

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.dist = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.dist[(from_node, to_node)] = int(distance)

    def dijkstra(self, start, maxD=1e309):
        """Returns a map of nodes to distance from start and a map of nodes to
        the neighbouring node that is closest to start."""
        # total distance from origin
        tdist = defaultdict(lambda: 1e309)
        tdist[start] = 0
        # neighbour that is nearest to the origin
        preceding_node = {}
        unvisited = self.nodes

        while unvisited:
            current = unvisited.intersection(tdist.keys())
            if not current: break
            min_node = min(current, key=tdist.get)
            unvisited.remove(min_node)

            for neighbour in self.edges[min_node]:
                d = tdist[min_node] + self.dist[min_node, neighbour]
                if tdist[neighbour] > d and maxD >= d:
                    tdist[neighbour] = d
                    preceding_node[neighbour] = min_node

        return tdist, preceding_node

    def min_path(self, start, end, maxD=1e309):
        """Returns the minimum distance and path from start to end."""
        tdist, preceding_node = self.dijkstra(start, maxD)
        dist = tdist[end]
        backpath = [end]
        try:
            while end != start:
                end = preceding_node[end]
                backpath.append(end)
            path = list(reversed(backpath))
        except KeyError:
            path = None

        return dist, path

    def dist_to(self, *args): return self.min_path(*args)[0]
    def path_to(self, *args): return self.min_path(*args)[1]

grafo = Graph()
reqs = []

constroi = True
for line in fileinput.input():
    if len(line) < 3:
        constroi = False
        continue
    if constroi:
        partida, chegada, tempo = line.split(' ')
        if partida not in grafo.nodes:
            grafo.add_node(partida)
        if chegada not in grafo.nodes:
            grafo.add_node(chegada)
        grafo.add_edge(partida,chegada,tempo)
        line = input()
    else:
        # requisicoes
        req = line.split(' ')
        d = {'partida':req[0].strip(),'chegada':req[1].strip()}
        if len(req) > 2: #viagem em andamento
            #d['atual'] = req[2]
            d['partida'] = req[2].strip() # enunciado ambiguo
        reqs.append(d)
fileinput.close()
print(grafo.min_path('0','1'))




