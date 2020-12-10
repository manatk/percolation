from copy import deepcopy
from util import Vertex
from util import Edge
from util import Graph
from util import *
import copy
import random
import math

def graph_dictionary(graph):
	vertex_dictionary = {}
	for vertex in graph.V:
		vertex_dictionary[v] = set()
	for edge in graph.E:
		vertex_dictionary[edge.b].add(edge.a)
		vertex_dictionary[edge.a].add(edge.b)
	return vertex_dictionary

def PercolateChild(graph, index):
	child_graph = Graph(copy.copy(graph.V), copy.copy(graph.E))
	v = None
	for vertex in child_graph.V:
		if vertex.index == index:
			v = vertex
	for e in IncidentEdges(child_graph, v):
		child_graph.E.remove(e)
    # Remove this vertex.
	child_graph.V.remove(v)
    # Remove all isolated vertices.
	to_remove = {u for u in child_graph.V if len(IncidentEdges(child_graph, u)) == 0}
	child_graph.V.difference_update(to_remove)
	return child_graph

def score2(graph, player):
	print("INSCORE2")
	if len(graph.V) == 0:
		print(graph.V)
		print("EMPTY GRAPH")
		if player:
			return (math.inf)
		else:
			return (-math.inf)
	player_vertices = [v for v in graph.V if v.color == player]
	other_player_vertices = [v for v in graph.V if v.color == 1-player]
	if len(player_vertices) > 0:
		return (math.inf)
	else:
		return (-math.inf)

def minimax_root(graph, player):
	my_vertices = [v for v in graph.V if v.color == player]
	children_values = {}
	for vertex in my_vertices:
		move = vertex.index
		child = PercolateChild(graph, vertex.index)
		children_values[move] = minimax(child, 1-player, 0, 2, {})
	best_move = None
	best_score = 0

	for (move, value) in children_values.items():
		print(move, value)
		if value > best_score:
			best_move = move
			best_score = value
	print(best_move)
	for v in graph.V:
		if v.index == best_move:
			print("VERTEX = nest move")
			print (v)
			return v

	if best_move == None:
		"NONE SITUATION"
		return random.choice(my_vertices)

	# make sure we return a vertex either here, or in GetVertexToRemove later
#	return [v for v in graph.V if v.index == best_move]


def minimax(graph, player, currentDepth, targetDepth, counts):
	if currentDepth not in counts:
		counts[currentDepth] = 0
	counts[currentDepth] += 1
	#print(counts)
	mine = [v for v in graph.V if v.color == player]

	if isFinished(graph, player):
		#print("Is finished")
		#print(graph)
		return score2(graph, player)

	if currentDepth == targetDepth:
		#import pdb; pdb.set_trace()
		#print("currentDepth == targetDepth")
		return heuristic(graph, player)

	if player == 0:
		m_m = {}
		graph_children = []
		for vertex in mine:
			move = vertex.index
			child = PercolateChild(graph, move)
			m_m[move] = minimax(child, 1-player, currentDepth+1, targetDepth, counts)
			#print(graph_children)

		best_move = None
		best_score = 0
		for (move, score) in m_m.items():
			if score > best_score:
				best_move = move
				best_score = score

		return (best_score)

	else:
		m_m = {}
		for vertex in mine:
			move = vertex.index
			child = PercolateChild(graph, move)
			m_m[move] = minimax(child, 1-player, currentDepth+1, targetDepth, counts)
			#print(graph_children)

		best_move = None
		best_score = math.inf
		for (move, score) in m_m.items():
			if score < best_score:
				best_move = move
				best_score = score
		return (best_score)

def Neighbors(graph, v):
	vertices = set()
	for edge in graph.E:
		if edge.a == v:
			vertices.add(edge.b)
		elif edge.b == v:
			vertices.add(edge.a)
	return vertices

def isFinished(graph, player):
	player_vertices = [v for v in graph.V if v.color == player]
	other_player_vertices = [v for v in graph.V if v.color == 1-player]
	return len(player_vertices) == 0 or len(other_player_vertices) == 0

def heuristic(graph, player):
	scores = {}
	candidates_to_remove = []
	second_candidates = []
	for vertex in graph.V:
		if vertex.color == player:
			candidates_to_remove.append(vertex)

	for vertex in candidates_to_remove:
		other_destroyed = 0
		self_destroyed = 0
		edges = (GetEdge(graph, vertex, player))
		for edge in edges:
			if edges[edge] == True:
				other_destroyed = other_destroyed + 1
			else:
				self_destroyed = self_destroyed + 1
		if other_destroyed > self_destroyed:
			second_candidates.append(vertex)
			scores[vertex] = 3
		else:
			scores[vertex] = -3

	#import pdb; pdb.set_trace()

	min_degree_vertex = None
	min_neighbors = math.inf

	if len(second_candidates) != 0:
		for vertex in second_candidates:
			edges = (GetEdge(graph, vertex, player))
			if len(edges) >= 1 and len(edges) < min_neighbors:
				min_degree_vertex = vertex
				min_neighbors = len(edges)
				scores[vertex] = scores[vertex] + 4
	else:
		for vertex in candidates_to_remove:
			edges = (GetEdge(graph, vertex, player))
			if len(edges) < min_neighbors:
				min_degree_vertex = vertex
				min_neighbors = len(edges)
				scores[vertex] = scores[vertex] + 1

	#import pdb; pdb.set_trace()

	best_score_vertex = max(scores, key=scores.get)
	best_score = scores[(max(scores, key=scores.get))]
	return (best_score)

def GetEdge(graph,vertex,player):
	edges = {}
	other_player = False
	for edge in graph.E:
		if edge.a == vertex or edge.b == vertex:
			if edge.a.color != player or edge.b.color != player:
				other_player = True
			edges[edge] = other_player
	return edges

def getDegree(graph,vertex):
	edges = []
	for edge in graph.E:
		if (edge.a == vertex or edge.b == vertex):
			#print("TRUE")
			edges.append(edge)
	return len(edges)

def getSelfDegree(graph,vertex,player):
	edges = []
	for edge in graph.E:
		if (edge.a == vertex or edge.b == vertex) and (edge.a == player or edge.b == player):
			edges.append(edge)
	return len(edges)

class PercolationPlayer:

	def ChooseVertexToColor(graph, player):
		max_vertices = []
		uncolored_vertices = []
		for vertex in graph.V:
			if vertex.color == -1:
				uncolored_vertices.append(vertex)
		max_degree_vertex = uncolored_vertices[0]
		max_degree = getDegree(graph, uncolored_vertices[0])
		for vertex in uncolored_vertices:
			degree = getDegree(graph, vertex)
			if degree > max_degree:
				max_degree_vertex = vertex
				max_degree = degree
				max_vertices.append(vertex)
		if len(max_vertices) > 0:
			max_self = -math.inf
			max_self_vertex = max_vertices[0]
			for vertex in max_vertices:
				degree_self = getSelfDegree(graph,vertex,player)
				if degree_self > max_self:
					max_self = degree_self
					max_self_vertex = vertex
			return max_self_vertex
		return max_degree_vertex
	# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
	# Should return a vertex `v` from graph.V where v.color == player
	def ChooseVertexToRemove(graph, player):
		#print(minimax(graph, player, 0, 6))
		#return(minimax_root(graph, player))

		temporary_graph = deepcopy(graph)
		candidates_to_remove = []
		second_candidates = []
		for vertex in temporary_graph.V:
			if vertex.color == player:
				candidates_to_remove.append(vertex)
				#print(Percolate(graph,vertex))
		min_degree_vertex = None
		min_neighbors = math.inf

		for vertex in candidates_to_remove:
			other_destroyed = 0
			self_destroyed = 0
			edges = (GetEdge(temporary_graph, vertex, player))
			for edge in edges:
				if edges[edge] == True:
					other_destroyed = other_destroyed + 1
				else:
					self_destroyed = self_destroyed + 1
			if other_destroyed > self_destroyed:
				second_candidates.append(vertex)
		if len(second_candidates) != 0:
			for vertex in second_candidates:
				edges = (GetEdge(temporary_graph, vertex, player))
				if len(edges) > 1 and len(edges)< min_neighbors:
					min_degree_vertex = vertex
					min_neighbors = len(edges)
				elif len(edges) < min_neighbors:
					min_degree_vertex = vertex
					min_neighbors = len(edges)
		else:
			for vertex in candidates_to_remove:
				edges = (GetEdge(temporary_graph, vertex, player))
				if len(edges) < min_neighbors:
					min_degree_vertex = vertex
					min_neighbors = len(edges)

		if min_degree_vertex == None:
			print(min_neighbors)
			print ("ERROR")
		return min_degree_vertex

# Feel free to put any personal driver code here.
def main():
	v1 = Vertex("A", 0)
	v2 = Vertex("B", 0)
	v3 = Vertex("C", 0)
	v4 = Vertex("D", 0)
	e1 = Edge(v1, v2)
	e2 = Edge(v3, v4)
	e3 = Edge(v2, v3)
	e4 = Edge(v4, v1)
	e5 = Edge(v2, v4)

	V = set([v1,v2,v3,v4])
	E = set([e1,e2,e3,e4,e5])

	graph1 = Graph(V,E)

if __name__ == "__main__":
    main()
