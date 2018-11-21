import sys
from collections import defaultdict
from copy import copy

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.dist = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        #self.edges[to_node].append(from_node)
        self.dist[(from_node, to_node)] = int(distance)

    def dijkstra(self, start, maxD=1e309):
        """Returns a map of nodes to distance from start and a map of nodes to
        the neighbouring node that is closest to start."""
        # total distance from origin
        tdist = defaultdict(lambda: 1e309)
        tdist[start] = 0
        # neighbour that is nearest to the origin
        preceding_node = {}
        unvisited = copy(self.nodes)

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
file = open(sys.argv[1], 'r') 
numero = 0
for line in file:
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
    else:
        # requisicoes
        numero +=1
        req = line.split(' ')
        d = {'n': numero, 'partida':req[0].strip(),'chegada':req[1].strip()}
        if len(req) > 2: #viagem em andamento
            #d['atual'] = req[2]
            d['partida'] = req[2].strip() # enunciado ambiguo
        d['tpadrao'] = grafo.min_path(d['partida'],d['chegada'])[0]
        reqs.append(d)

file.close()
res = []
for r in reqs:
    incs = []
    for s in reqs:
        if r == s:
            continue
        #testar todos os caminhos e guardar o menor
        menor = 20
        #A C D B
        ttotal = grafo.min_path(r['partida'],s['partida'])[0]+s['tpadrao']+grafo.min_path(s['chegada'],r['chegada'])[0]
        inc = ttotal/r['tpadrao']
        # nesse caso inc2 é sempre 1
        if inc <= 1.4:
            menor = inc
            cam = (r['partida'],s['partida'],s['chegada'],r['chegada'])
        #A C B D
        ttotal = grafo.min_path(r['partida'],s['partida'])[0] +grafo.min_path(s['partida'],r['chegada'])[0]+grafo.min_path(r['chegada'],s['chegada'])[0]
        inc = max(ttotal/r['tpadrao'],ttotal/s['tpadrao'])
        if inc < menor and inc <= 1.4:
            menor = inc
            cam = (r['partida'],s['partida'],r['chegada'],s['chegada'])
        #C A D B
        ttotal = grafo.min_path(s['partida'],r['partida'])[0] +grafo.min_path(r['partida'],s['chegada'])[0]+grafo.min_path(s['chegada'],r['chegada'])[0]
        inc = max(ttotal/r['tpadrao'],ttotal/s['tpadrao'])
        if inc < menor and inc <= 1.4:
            menor = inc
            cam = (s['partida'],r['partida'],s['chegada'],r['chegada'])
        #C A B D
        ttotal = grafo.min_path(s['partida'],r['partida'])[0] +r['tpadrao']+grafo.min_path(r['chegada'],s['chegada'])[0]
        inc = ttotal/s['tpadrao'] # nesse caso inc1 é sempre 1
        if inc < menor and inc <= 1.4:
            menor = inc
            cam = (s['partida'],r['partida'],r['chegada'],s['chegada'])
        incs.append((menor,cam,s['n']))
    # incs tem todas as menores inconveniencias com todos os pares de r
    # achar a menor das inconveniencias
    menor = (20,0)
    for x in incs:
        if x[0] < menor[0]:
            menor = x
    res.append((r['n'],menor))
# achar os menores pares

while len(res) > 1:
    menor = (0,(20,0))
    for x in res:
        if x[1][0] < menor[1][0]:
            menor = x
    # encontrar par
    for x in res:
        if x[0] == menor[1][2]:
            match = x        
    res.remove(match)
    res.remove(menor)
    print ('passageiros:',menor[0],match[0],'percurso:',' '.join(menor[1][1]))

if len(res)==1:
    # encontrar percurso original
    for x in reqs:
        if x['n']==res[0][0]:
            p = x
    print('passageiro:' ,p['n'],'percurso:',p['partida'],p['chegada'])






