"""
@author - Aayushi Srivastava
This code compares both LB-Triangulation and Minimum Degree Vertex based on the number of edges added in both of the algorithm.
"""


import random
import numpy as np

import itertools
import copy

import networkx as nx
import matplotlib.pyplot as plt
import sys


from time import sleep
#import abdc
#from Queue import Queue
#from threading import Thread


class ChordalVert:
	def __init__(self, noNodes, noEdges, m_vert=0):
		"""function to initialize the variables in the instance of a ChordalGraph"""
		self.noNodes = noNodes
		self.noEdges = noEdges
		self.vertexList = []
		self.GEdgeList = []
		self.HEdgeList = [] #HEdgeList
		self.REdgeList = []
		self.G = {}
		self.H = {}
		self.R = {}
		self.neb = [] 
		self.m_vert = m_vert
		self.minv = {}
		self.neb = []
		self.NEdgeList = []
		self.LEdgeList = []

	def ArbitraryGraph(self):
		"""function to create arbitrary graph"""
		self.G = nx.dense_gnm_random_graph(self.noNodes, self.noEdges)
		self.G = { 0: [1, 2, 4],
		   1: [0, 4],
		   2: [0, 3],
		   3: [2, 5],
		   4: [0, 1, 5],
		   5: [3, 4]}

		if type(self.G) is not dict:
			self.G = nx.to_dict_of_lists(self.G)
				
		for i in range(0, self.noNodes):
			self.vertexList.append(i)
		for key, value in self.G.iteritems():
			for v in value:
				if key<v:
					e = []
					e.append(key)
					e.append(v)
					self.GEdgeList.append(e)
		
		self.G = nx.Graph(self.G)
		connComp = sorted(nx.connected_components(self.G))
		self.G = nx.to_dict_of_lists(self.G)
		
		connComp = list(connComp)
		noOFConnComp = len(connComp)
		if noOFConnComp > 1:
			print "Here we are"
			print connComp
			self.G = nx.Graph(self.G)
			#self.plotArbitraryGraph(self.G)
			j = 0
			while j < noOFConnComp - 1:
				u = random.choice(list(connComp[j%noOFConnComp]))
				v = random.choice(list(connComp[(j+1)%noOFConnComp]))
				self.addAnEdge(self.G, self.GEdgeList, u, v)
				j = j + 1
		print str(self.G)
		self.G = nx.Graph(self.G)
		#self.plotArbitraryGraph(self.G)
		#print "see"
		self.G = nx.to_dict_of_lists(self.G)

		 
	def addAnEdge(self, graphToAdd, edgeListToAdd, v1, v2):
		"""function to add an edge in the graph"""
		graphToAdd = nx.to_dict_of_lists(graphToAdd)
		graphToAdd[v1].append(v2)
		graphToAdd[v2].append(v1)
		e = []
		e.append(v1)
		e.append(v2)
		edgeListToAdd.append(e)
		

	def plotArbitraryGraph(self, graphToDraw):
		"""To plot arbitrary graph"""
		edges = 0
		for node, degree in graphToDraw.iteritems():
			edges += len(degree) 
		
		GD = nx.Graph(graphToDraw)
		pos = nx.spring_layout(GD)
		print "\nArbitrary Graph: "+str(self.G)
		print "\nNo. of edges in the Arbitrary Graph: "+ str(edges/2)
		#plt.title("Arbitrary Graph")
		#nx.draw(GD, pos, width=8.0,alpha=0.5,with_labels = True)
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_nodes(GD, pos, node_color='red', node_size=300, alpha=0.8)
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		plt.show(block=False)
	
	def createChrdG(self):
		#Function to start Minimum Degree Vertex
		self.HEdgeList = copy.deepcopy(self.GEdgeList)
		self.H = copy.deepcopy(self.G)
		self.H = nx.Graph(self.H)

		print "Start Minimum Vertex Process"
		self.H = nx.Graph(self.H)
		self.Minvertex(self.vertexList,self.HEdgeList,self.H) #Function to generate MDV 
		
		print "End Minimum Vertex Process"
		return True


	def Minvertex(self,vertexList,edgeList, graphtoCons):
		graphtoCons = nx.Graph(graphtoCons)
		self.H = nx.Graph(self.H)
		#isChordal = False
		#print "My vertex list",vertexList
		random.shuffle(vertexList)
		self.H = nx.Graph(self.H)
		for v in vertexList:
			#print type(self.H)
			self.H = nx.Graph(self.H)
			dv = list(self.H.degree(self.H)) #list of tuples
			#dv = list(graphtoCons.degree(graphtoCons)) 
			#print "see the  degree list:"
			#print dv
			#print self.HEdgeList
			dvdict = dict(dv)
			#print "Dictionary of node-degree is", dvdict
			self.minv = dict(sorted(dvdict.items(), key=lambda kv:(kv[1], kv[0])))
			#print "Sorted dictionary of node-degree:",self.minv
			#graphtoCons = nx.to_dict_of_lists(graphtoCons)
			self.H = nx.Graph(self.H)
			#print "The dictionary looks like:", self.H
			mincp = copy.deepcopy(self.minv)
			try:
				for key,value in mincp.iteritems():
					if value < 2:
						self.minv.pop(key)
				#print "Deleted"
				#print "Updates:",self.minv
				graphtoCons = nx.Graph(graphtoCons)
				#nodeH = graphtoCons.nodes()
				nodeH = self.H.nodes()
				#print "Old Nodes are:",nodeH
				#print "New nodes are",list(self.minv)
				self.H.add_nodes_from(list(self.minv))
				self.H.remove_nodes_from(list(list(set(nodeH) - set(list(self.minv)))))
				self.H = nx.to_dict_of_lists(self.H)
				#print "New Dictionary:",self.H
				self.m_vert = min(self.minv.keys(), key=(lambda k:self.minv[k]))
				#print type(self.m_vert)
				print "Minimum degree vertex is:",self.m_vert
				self.H = nx.Graph(self.H)
				print "The chosen Minimum vertex is", self.m_vert
				
				self.neb = list(self.H.neighbors(self.m_vert))
				print "Neighbors of the chosen vertex are:",self.neb
				neblen = len(self.neb)
				
				self.H = nx.Graph(self.H)
				self.H.remove_node(self.m_vert)
				self.neighbcomp(self.m_vert,self.H)
				self.H = nx.Graph(self.H)
			except ValueError as e:
				print "Dictionary is Empty now"
				break


	def neighbcomp(self,chosvert,graphtoRecreate):
		"""To add an edge between neighbors of the vertices selected"""
		self.H = nx.Graph(self.H)
		nebcomb = list(itertools.combinations(self.neb,2))
		#print "See combinations:",nebcomb
		for p in nebcomb:
			v1 =  p[0]
			v2 = p[1]
			#print p
			if self.H.has_edge(*p) :
				#print p
				#print "Already edge is there"
				continue
			else:
				self.H.add_edge(*p)
				#print "Check this"
				self.NEdgeList.append(p)
				#print "My list", self.NEdgeList
				continue
		#print "Edges added using Minimum Degree",len(self.NEdgeList)

		self.H= nx.to_dict_of_lists(self.H)
		#print "See change",self.H

	def FinalGraph(self,newaddedgelist,vertexlist):
		"""Plots chordal graph using MDV"""
		#isChordal = False
		print "EdgeList verifying",newaddedgelist
		print "Total Edges added in Minimum Degree Process is ",len(newaddedgelist)
		GD = nx.Graph(self.G)
		pos = nx.spring_layout(GD)

		B = copy.deepcopy(self.G)
		B = nx.Graph(B)
		B.add_nodes_from(vertexlist)
		B.add_edges_from(newaddedgelist)
		B = nx.to_dict_of_lists(B)
		print "see B", B
		##Recognition----
		graph = nx.Graph(B)
		if nx.is_chordal(graph):
			print "IT IS CHORDAL"
		else :
			print "NO IT IS NOT CHORDAL"
		nx.draw_networkx_nodes(GD, pos, nodelist=vertexlist, node_color='red', node_size=300, alpha=0.8,label='Min degree')
			
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_edges(GD, pos, edgelist=newaddedgelist, width=8.0, alpha=0.5, edge_color='blue',label='Min degree')
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		plt.show(block=False)

	def createAuxGraph(self, graph, auxNodes):
		"""function to create induced graph on the set of vertices"""
		auxGraph = {}
		for i in auxNodes:
			if i in graph:
				auxGraph[i] = list(set(graph[i]).intersection(set(auxNodes)))
		return auxGraph


	def workLT(self):
		"""Function to start LB-Triang"""
		self.REdgeList = copy.deepcopy(self.GEdgeList)
		self.R = copy.deepcopy(self.G)

		print "SEE LB_Triang"

		self.LB_Triang(self.vertexList, self.REdgeList, self.R) #Function of LB-Triang
		print "Now let's see graph of LB"
		print "End of LB-Triang"


		return True
	
	def LB_Triang(self, vertexList, edgeList, graphToRecognize):
		"""This function is implemented based on the algorithm LB-Triang from the paper "A WIDE-RANGE EFFICIENT ALGORITHM FOR 
		MINIMAL TRIANGULATION" by Anne Berry for recognition chordal graphs and add edges (if necessary) by making each vertex 
		LB-simplicial.""" 
		graphToRecognize = nx.Graph(graphToRecognize)
		random.shuffle(vertexList)
		#vertexVisibility = [0]*len(vertexList)
		#isChordal = False
		for v in vertexList:
			print "The vertex "+str(vertexList.index(v))+"-"+str(v)+" is verifying..."
			#openNeighbors = graphToRecognize[v]
			#self.R = nx.to_dict_of_lists(self.R)
			openNeighbors = self.R[v]
			print "My openNeighbor is:" ,openNeighbors
			#self.R = nx.to_dict_of_lists(self.R)
			closedNeighbors = copy.deepcopy(openNeighbors)
			#print type(closedNeighbors)
			closedNeighbors.append(v)
			print "My closed neighbors",closedNeighbors
			cNMinusE = list(set(vertexList).difference(set(closedNeighbors))) #V-S
			#print "cNMinusE is",cNMinusE
			if cNMinusE:
				#print "Loopys"
				#VMinusSGraph = self.createAuxGraph(graphToRecognize, cNMinusE) #G(V-S)
				VMinusSGraph = self.createAuxGraph(self.R, cNMinusE) #G(V-S)
				componentsOri = sorted(nx.connected_components(nx.Graph(VMinusSGraph)))
				print "Component(s) in the graph: "+str(componentsOri)
				componentsCompAll = []
				for co in componentsOri:
					openNCO = []
					for v1 in co:
						#print type(self.R)
						#openNV1 = graphToRecognize[v1]
						openNV1 = self.R[v1]
						#print type(openNV1)
						#print "openNV1:",openNV1
						openNCO = openNCO+openNV1
						#print "pehle wala openNCO",openNCO
					openNCO = list(set(openNCO).difference(co))
					#print "see openNCO",openNCO
					self.LbEdges(openNCO)
					self.R = nx.to_dict_of_lists(self.R)
			else:
				print "The vertex "+str(v)+" does not generate any minimal separator."
				print "================================================"
			
	def LbEdges(self,vlist):
		"""Function to add fill-edges in LB-Triang"""
		self.R = nx.Graph(self.R)
		lbcomb = list(itertools.combinations(vlist,2))
		#print "See combinations:",lbcomb
		for p in lbcomb:
			#print p
			v1 = p[0]
			v2 = p[1]
			if self.R.has_edge(*p):
				#print p
				#print "Already edge is there"
				continue
			else:
				self.R.add_edge(*p)
				#print "Check this"
				self.LEdgeList.append(p)
				#print "My list", self.LEdgeList
				templist = []
				templist.append(v1)
				templist.append(v2)
				self.REdgeList.append(templist)
				#print "My list", self.LEdgeList
				#print "MY seen list",self.REdgeList

		#print "Edges added using LB-Triang",len(set(self.LEdgeList))
	 
	
	def LBFinalGraph(self,newaddedgelist,vertexlist):
		"""Chordal graph is plotted using LBT"""
		GD = nx.Graph(self.G)
		pos = nx.spring_layout(GD)
		print "New edges added are:",newaddedgelist
		print "Total Edges added in LB-Triang is", len(newaddedgelist)
		F = copy.deepcopy(self.G)
		F = nx.Graph(F)
		F.add_nodes_from(vertexlist)
		F.add_edges_from(newaddedgelist)
		F = nx.to_dict_of_lists(F)
		#print "see F", F
		graph = nx.Graph(F)
		if nx.is_chordal(graph):
			print "IT IS CHORDAL"
		else:
			print "NO IT IS NOT CHORDAL"
	

		nx.draw_networkx_nodes(GD, pos,nodelist=vertexlist, node_color='red', node_size=300, alpha=0.8,label='LB_Triang')
					
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_edges(GD, pos, edgelist=newaddedgelist, width=8.0, alpha=0.5, edge_color='blue',label='LB_Triang')
		nx.draw_networkx_labels(GD,pos)
		nx.draw_networkx(GD,pos,True)
		plt.show(block=False)


			


