from copy import deepcopy
from util import Vertex
from util import Edge
from util import Graph
from util import *
import itertools
import copy
import random
import math

class PercolationPlayer:
	#converts the graph into a dictionary
	#the key of the dictionary is the vertex and the values are all the neighboring vertices
	def get_info(graph):
		info = {}
		#print("Verticies", graph.V)
		#print("EDGES:", graph.E)
		for edge in graph.E:
			#if the vertex already exists in the dictionary keys, add the vertex on the other end of the edge
			if edge.a in info.keys():
				info[edge.a].append(edge.b)
			#vertex not in dictionary, create a new key
			else:
				info[edge.a] = [edge.b]

			if edge.b in info.keys():
				info[edge.b].append(edge.b)
			else:
				info[edge.b] = [edge.a]

		#add all the isolated edges
		for vert in graph.V:
			if vert not in info.keys():
				info[vert] = []

		#print(info.keys())
		#return the dictionary
		return info

	#print a representation of the graph
	def graph_view(all):

		for vert in all:
			print(vert, "connected to: ")
			for e in all[vert]:
				print(e)
			print("************")

	def ChooseVertexToColor(graph, player):
		#all the vertex nodes
		all_nodes = PercolationPlayer.get_info(graph)
		#print(all_nodes)

		#get all the empty nodes
		empty_nodes = {vert: all_nodes[vert] for vert in all_nodes if vert.color == -1}
		#see which vertex is the most connected
		max_e = max(empty_nodes, key=lambda x: len(empty_nodes[x]))
		#find the max value
		empty_nodes_max = [vert for vert in empty_nodes if len(empty_nodes[vert]) == len(empty_nodes[max_e])]
		#print("amount of max nodes:", len(empty_nodes), "Edge number: ", len(empty_nodes[max_e]))

		if len(empty_nodes_max) < 2:
			return empty_nodes_max[0]

		#if the score is positive, then the vertex you color will be a better move for you then the other player
		eff_scores = {}
		for vert in empty_nodes_max:
			score = 0
			for other_v in all_nodes[vert]:
				if other_v.color == 1 - player:
					score += 1
				elif other_v.color == player:
					score -= 1
			eff_scores[vert] = score

		#max effective score
		max_eff = max(eff_scores, key=lambda x: eff_scores[x])
		#find the nodes of the max vertex
		eff_nodes = [vert for vert in eff_scores if eff_scores[vert] == eff_scores[max_eff]]

		if len(eff_nodes) < 2:
			return eff_nodes[0]

		#count of all the edges attached to vertices attached to a Vertex.
		importance = {}
		for vert in eff_nodes:
			importance[vert] = sum(len(all_nodes[other_v]) for other_v in all_nodes[vert])

		max_i = max(importance, key=lambda x: importance[x])

		return max_i

	def ChooseVertexToRemove(graph, player):
		all_nodes = PercolationPlayer.get_info(graph)

		'''
		if len(graph.V) == 6:
			print("Player is", player)
			PercolationPlayer.graph_view(all_nodes)
		'''

		#player_nodes = [vert for vert in all_nodes if vert.color == player]
		#opposite player's nodes
		opp_nodes = [vert for vert in all_nodes if vert.color == 1 - player]

		if len(opp_nodes) > 0:

			#max edges of the opp_nodes
			opp_max_e = max(opp_nodes, key=lambda x: len(all_nodes[x]))
			opp_nodes = [vert for vert in all_nodes if len(all_nodes[vert]) == len(all_nodes[opp_max_e])]

			player_nodes = []
			for vert in opp_nodes:
				for v in all_nodes[vert]:
					if v.color == player:
						player_nodes.append(v)

			if len(player_nodes) < 1:
				player_nodes = [vert for vert in all_nodes if vert.color == player]

		else:
			player_nodes = [vert for vert in all_nodes if vert.color == player]

		#calculate the effective score
		eff_scores = {}

		#score is based on whether you destroy your vertex or another player's vertex
		for vert in player_nodes:
			eff_scores[vert] = sum(1 if other_v.color == 1 - player else -1 for other_v in all_nodes[vert])

		max_eff = max(eff_scores, key=lambda x: eff_scores[x])
		max_nodes = [vert for vert in player_nodes if eff_scores[vert] == eff_scores[max_eff]]

		if len(max_nodes) < 2:
			print("removing: ", max_nodes[0])
			return max_nodes[0]

		#count of all the edges attached to vertices attached to a Vertex and score based on that
		importance = {}
		for vert in max_nodes:
			importance[vert] = sum(len(all_nodes[other_v]) for other_v in all_nodes[vert])

		max_i = max(importance, key=lambda x: importance[x])

		important_nodes = [vert for vert in max_nodes if importance[vert] == importance[max_i]]

		if len(important_nodes) < 2:
			print("removing: ", important_nodes[0])
			return important_nodes[0]

		print("removing: ", max(important_nodes, key=lambda x: len(all_nodes[x])))
		return max(important_nodes, key=lambda x: len(all_nodes[x]))

# Feel free to put any personal driver code here.
def main():
	#PercolationPlayer.ChooseVertexToColor(BinomialRandomGraph(20, random.random()), 0)
	pass

if __name__ == "__main__":
    main()
