import Tkinter
import tkMessageBox

import random

import CompareABnMV as CG
#import chrdTrialq as CG

def isStrInt(str):
	"""function to check if str is int or not"""
	try: 
		int(str)
		return True
	except ValueError:
		return False
	
class gui_tk(Tkinter.Tk):
	"""The main class contains gui_tk initialization"""

	def __init__(self,parent):
		"""function to initialize the instance of Tkinter and ChordalGraph"""
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
		self.ag = CG.ChordalVert(0, 0)
		self.G = False
		self.H = False
		self.R = False
		
	def initialize(self):
		"""function to initialize the components in the gui"""
		self.grid()

		self.lblNumNodesText = Tkinter.StringVar()
		lblNodes = Tkinter.Label(self, textvariable=self.lblNumNodesText)
		lblNodes.grid(row=0, column=0, sticky=Tkinter.W)
		self.lblNumNodesText.set(u'No. of Nodes ')

		self.nodesEntry = Tkinter.Entry(self)
		self.nodesEntry.grid (row=0, column=1, sticky=Tkinter.W)
		
		self.lblNumEdgesText = Tkinter.StringVar()
		lblEdges = Tkinter.Label(self, textvariable=self.lblNumEdgesText)
		lblEdges.grid(row=1, column=0, sticky=Tkinter.W)
		self.lblNumEdgesText.set(u'No. of Edges ')
	
		self.edgesEntry = Tkinter.Entry(self)
		self.edgesEntry.grid (row=1, column=1, sticky=Tkinter.W)

		
		#Arbitrary Graph"		
		buttonCreateAG = Tkinter.Button(self,text=u'Generate Arbitrary Graph', 
										   command=self.onCreateAGClick)
		buttonCreateAG.grid(row=3, column=0, sticky=Tkinter.W)
		
		buttonViewAG = Tkinter.Button(self,text=u'View Arbitrary Graph', 
										   command=self.onViewAGClick)
		buttonViewAG.grid(row=3, column=1, sticky=Tkinter.W)        
		
		#LB-Triang Chordal Graph
		buttonLBCreateWCG = Tkinter.Button(self,text=u'Generate LB Chordal Graph', 
											  command=self.onCreateLBCGClick)
		buttonLBCreateWCG.grid(row=4, column=0, sticky=Tkinter.W)
		
		buttonLBViewWCG = Tkinter.Button(self,text=u'View LB Chordal Graph', 
											  command=self.onViewLBCGClick)
		buttonLBViewWCG.grid(row=4, column=1, sticky=Tkinter.W)


        #Minimum Degree Chordal Graph
		buttonMDCreateWCG = Tkinter.Button(self,text=u'Generate MD Chordal Graph', 
											  command=self.onCreateMDCGClick)
		buttonMDCreateWCG.grid(row=5, column=0, sticky=Tkinter.W)
		
		buttonMDViewWCG = Tkinter.Button(self,text=u'View MD Chordal Graph', 
											  command=self.onViewMDCGClick)
		buttonMDViewWCG.grid(row=5, column=1, sticky=Tkinter.W)
		
	def onCreateAGClick(self):
		"""function to check valid input and to create arbitrary Graph"""

		noNodes = self.nodesEntry.get()
		if isStrInt(noNodes):
			noNodes = int (self.nodesEntry.get())
			if (noNodes < 4):
				tkMessageBox.showwarning("Warning","Entry for nodes is less than 4.")
				return
		else:
			tkMessageBox.showwarning("Warning","Entry for nodes is not an integer.")
			return
		
		noEdges = self.edgesEntry.get()
		if isStrInt(noEdges):
			noEdges = int (self.edgesEntry.get())
			if (noEdges < 3):
				tkMessageBox.showwarning("Warning","Entry for edges is less than 3.")
				return
			if (noEdges < (noNodes-1)):
				tkMessageBox.showwarning("Warning","Entry for edges must be enough for a tree structure. Needs %d." %(noNodes-1))
				return
			if (noEdges > (noNodes*(noNodes-1))/2)  :
				tkMessageBox.showwarning("Warning","Entry for edges provided is more than a complete graph." )
				return
		else:
			tkMessageBox.showwarning("Warning","Entry for edges is not an integer.")
			return
				
		self.ag = CG.ChordalVert(noNodes, noEdges)
		self.ag.ArbitraryGraph()
		self.G = True
		
	def onViewAGClick(self):
		"""function to call plotGraph to draw arbitrary graph"""
		if self.G:
			#self.ag.plotGraph(self.ag.G, 1)
			self.ag.plotArbitraryGraph(self.ag.G)
		else:
			tkMessageBox.showwarning("Warning","Create Arbitrary Graph first to view Arbitrary Graph.")
			return
	
	def onCreateLBCGClick(self):
		"""function to call createCG"""
		if self.G:
			self.ag.workLT()
			self.R = True
		#else:
		#	tkMessageBox.showwarning("Warning","Create Arbitrary Graph first before create Chordal Graph.")
			return
	
	def onViewLBCGClick(self):
		"""function to call plotGraph to draw chordal graph"""
		if self.R:
			self.ag.LBFinalGraph(self.ag.LEdgeList,self.ag.vertexList)
			#self.ag.plotGraph(self.ag.G, 1)

		#else:
		#	tkMessageBox.showwarning("Warning","Create Chordal Graph first to view Chordal Graph.")
			return

	def onCreateMDCGClick(self):
		"""function to call createMinDegreeChordal"""
		if self.G:
			self.ag.createChrdG()
			self.H = True
		#else:
		#	tkMessageBox.showwarning("Warning","Create Arbitrary Graph first before create Chordal Graph.")
			return
	
	def onViewMDCGClick(self):
		"""function to call plotGraph to draw chordal graph"""
		if self.H:
			self.ag.FinalGraph(self.ag.NEdgeList,self.ag.vertexList)
		#else:
		#	tkMessageBox.showwarning("Warning","Create Chordal Graph first to view Chordal Graph.")
			return
			
def center(toplevel):
	"""function to compute the center of the screen and place the window in the center"""
	toplevel.update_idletasks()
	w = toplevel.winfo_screenwidth()
	h = toplevel.winfo_screenheight()
	size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
	x = w/2 - size[0]/2
	y = h/2 - size[1]/2
	toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

if __name__ == "__main__":
	"""main function: the starting point of this weakly chordal graph generation method"""
	app = gui_tk(None)
	app.title("Chordal Graph (CG) Generation")  
	app.geometry('300x200')#window size
	center(app)
	app.mainloop()
	app.quit()