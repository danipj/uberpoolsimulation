import fileinput
from collections import defaultdict

class Graph:
  def __init__(self):
    self.nodes = set()
    self.edges = defaultdict(list)
    self.distances = {}

  def add_node(self, value):
    self.nodes.add(value)

  def add_edge(self, from_node, to_node, distance):
    self.edges[from_node].append(to_node)
    self.edges[to_node].append(from_node)
    self.distances[(from_node, to_node)] = distance

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
		d = {'partida':req[0],'chegada':req[1]}
		if len(req) > 2: #viagem em andamento
			#d['atual'] = req[2]
			d['partida'] = req[2] # enunciado ambiguo
		reqs.append(d)




