from copy import deepcopy
from util import Vertex
from util import Edge
from util import Graph
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

def children(graph, v):
	children = []
	for e in graph.IncidentEdges(v):
		if e.a == v:
			children.append(e.b)
		elif e.b == v:
			children.append(e.a)
	return children

#find the vertex with the index = i so that you can remove that.
#operations on that vertex
#at the call site for percolate child, would send graph, v.index
def PercolateChild(graph, index):
	child_graph = deepcopy(graph)
	#if in coloring
    # Get attached edges to this vertex, remove them.
	v = None
	for vertex in graph.V:
		if vertex.index == index:
			v = vertex
	for e in child_graph.IncidentEdges(v):
		child_graph.E.remove(e)
    # Remove this vertex.
	child_graph.V.remove(v)
    # Remove all isolated vertices.
	to_remove = {u for u in child_graph.V if len(child_graph.IncidentEdges(u)) == 0}
	child_graph.V.difference_update(to_remove)
	print(child_graph)
	return child_graph

def minimax(graph, player, currentDepth, targetDepth):
	mine = []
	for vertex in graph.V:
		if vertex.color == player:
			mine.append(vertex)
	#return a score and a vertex
	#WANT TO RETURN THE MOVE TO MAKE
	if isFinished(graph, player):
		print("Is finished")
		return score(graph, player)

	if currentDepth == targetDepth:
		return heuristic(graph, player)

	if player == 0:
		graph_children = []
		for vertex in mine:
			graph_children.append(PercolateChild(graph, vertex.index))
		print(graph_children)
		m_m = []
		for child in graph_children:
			m_m.append(minimax(child, 1-player, currentDepth+1, targetDepth))
		return max(m_m, key = lambda t: t[0])

	else:
		graph_children = []
		for vertex in mine:
			graph_children.append(PercolateChild(graph, vertex.index))
		m_m = []
		for child in graph_children:
			m_m.append(minimax(child, 1-player, currentDepth+1, targetDepth))
		#tuple with value of child's score and vertex you removed to get the child
		#key =
		return min(m_m, key = lambda t: t[0])


		#make a children function - should be the percolate code

		#figure out all of teh children for a given grapgh
		#call minimax on all the children
		#return the biggest minimax value for all the children

	'''
	else:
		vertices = []
		for edge in graph.E:
			if edge.a == vertex:
				vertices.append(edge.b)
			elif edge.b == vertex:
				vertices.append(edge.a)
		#return min(minimax(depth + 1, True, graph, vertex for vertices, player))
	'''



	'''
	dictionary = graph_dictionary(graph)
	if (curDepth == targetDepth):
		return score(graph, player)
	elif (maxTurn):
		#needs to go over all the childern
		#find all the children graphs
		#call minimax on all of the children, return the max of that
        return max(minimax(curDepth + 1, False, targetDepth),
                   minimax(curDepth + 1, dictionary[nodeIndex * 2 + 1],
                    False, targetDepth))
	else:
        return min(minimax(curDepth + 1, dictionary[nodeIndex * 2],
                     True, targetDepth),
                   minimax(curDepth + 1, dictionary[nodeIndex * 2 + 1],
                     True, targetDepth))
	'''
def Neighbors(graph, v):
	vertices = set()
	for edge in graph.E:
		if edge.a == v:
			vertices.add(edge.b)
		elif edge.b == v:
			vertices.add(edge.a)
	return vertices

#isFinish takes a graph and a player, which is an integer
#should return true or false
#if the graph contian
def isFinished(graph, player):
	player_vertices = [v for v in graph.V if v == player]
	other_player_vertices = [v for v in graph.V if v == 1-player]
	return len(player_vertices) == 0 or len(other_player_vertices) == 0


	#for all the vertices in the graph, if none of tehm are some players color
	# should just tell you if one of the subsets is empty

#def score(ONLY CALLED WHEN GAME IS OVER):
def score (graph, player):
	player = False
	other_player = False
	for vertex in graph.V:
		if vertex.color == player:
			return math.inf
		return -math.inf
	#for all the vertices in the graph, if none of them are player's color, then player loses
	# = -infinity
	#on an empty graph, whoever is going next loses


def heuristic(graph, player):

	scores = {}
	candidates_to_remove = []
	second_candidates = []
	for vertex in graph.V:
		if vertex.color == player:
			candidates_to_remove.append(vertex)
			#print(Percolate(graph,vertex))

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

	min_degree_vertex = None
	min_neighbors = math.inf

	'''
	#connecting to fewest number of player's max_vertices
	for vertex in second_candidates:
		edges = (GetEdge(graph, vertex, player))
		for edge in edges:
			if edge.a == player and edge.b == player:
				scores[vertex] = scores[vertex] - 1
			else:
				if len(edges) > 1 and len(edges) < min_neighbors:
					min_degree_vertex = vertex
					min_neighbors = len(edges)
					scores[vertex] = scores[vertex] + 2
	'''

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
	#print(scores[(max(scores, key=scores.get))])
	return {max(scores, key=scores.get), scores[(max(scores, key=scores.get))]}

	included_score = 0
	excluded_score = 0
	for vertex in graph:
		if vertex.color == player:
			included_score = included_score + 1
		else:
			excluded_score = excluded_score + 1
	return excluded_score - included_score

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
		#print(type(edge.a))
		if (edge.a == vertex or edge.b == vertex) and (edge.a == player or edge.b == player):
			edges.append(edge)
	return len(edges)

class PercolationPlayer:
	# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
# Should return a vertex `v` from graph.V where v.color == -1

	def ChooseVertexToColor(graph, player):

		degrees={vertex: 0 for vertex in graph.V}
		for edge in graph.E:
			degrees[edge.a] +=1
			degrees[edge.b] += 1
		max_key = max(degrees, key=degrees.get)
		while max_key.color != -1:
			degrees.pop(max_key)
			max_key = max(degrees, key=degrees.get)

		return max_key

		'''
		uncolored_vertices = {}
		for vertex in graph.V:
			if vertex.color == -1:
				uncolored_vertices[vertex] = None
		for vertex in uncolored_vertices:
			uncolored_vertices[vertex] = getDegree(graph, vertex)
		return max(uncolored_vertices, key = uncolored_vertices.get)
		'''


		'''
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
		print(max_vertices)
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
		'''

	# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
	# Should return a vertex `v` from graph.V where v.color == player
	def ChooseVertexToRemove(graph, player):
		minimax(graph, player, 0, 100)
		#minimax(graph, player, currentDepth, targetDepth)

		#assign weights to various features
		#print(heuristic(graph, player))
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


		#basically see which one of these vertices has the fewest
		#number of edges connecting to one of your vertices.
		#return random.choice(candidates_to_remove)
		'''
		same_color_vertices = []
		max_degree_vertex = None
		max_neighbors = -math.inf
		for vertex in temporary_graph.V:
			neighbors = Neighbors(temporary_graph, vertex)
			neighbor_count = len(neighbors)
			if neighbor_count > max_neighbors:
				max_neighbors = neighbor_count
				max_degree_vertex = vertex
		print(max_degree_vertex)
		return max_degree_vertex
		'''


	#if vertex.color == player:
	#			same_color_vertices.append(vertex)
	#	return random.choice(same_color_vertices)

	   #print(graph.IncidentEdges(graph.vertex))

# Feel free to put any personal driver code here.
def main():
	v1 = Vertex("A", 0)
	v2 = Vertex("B", 0)
	v3 = Vertex("C", 0)
	v4 = Vertex("D", 0)
	#print(v1.name)
	e1 = Edge(v1, v2)
	e2 = Edge(v3, v4)
	e3 = Edge(v2, v3)
	e4 = Edge(v4, v1)
	e5 = Edge(v2, v4)

	V = set([v1,v2,v3,v4])
	E = set([e1,e2,e3,e4,e5])

	graph1 = Graph(V,E)
#	print(children(graph1,v2))
	#print(Percolate(graph1,v2))


if __name__ == "__main__":
    main()

	#next STEPS
	#getting a working children's function
	#get a working heuristic function by moving some of the heuristic logic into
	#the heuristic function. Assign arbitrary weights to things
	#find a good target depth which is still within the 500 ms range

#QUESTIONS
'''
1) children copy issue
2) calling minimax correctly?
3) return move from minimax? How to do that? OR better to return number/score?
4) heuristic okay? Returning both the vertex and the score
5) multiple vertices will have the same score. How to handle that?

'''
