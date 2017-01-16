''' Draw tiles. '''

from matplotlib import pyplot as plt
from copy import deepcopy
from math import pi, sqrt, sin, cos 
from random import random

class Polygon:
	# A basic polygon.
	vertices = []
	color = None
	hatch = None
	edgeWidth = None
	edgeColor = None
	def __init__(self, newVerts):
		self.vertices = newVerts
	def __repr__(self):
		return "<Polygon " + str(self.vertices) + ">"
	def translate(self, x, y):
		for vert in self.vertices:
			vert[0] += x
			vert[1] += y
	def rotate(self, deg):
		for vert in self.vertices:
			rad = 2*pi*deg/360.0
			newX = vert[0]*cos(rad) - vert[1]*sin(rad)
			newY = vert[0]*sin(rad) + vert[1]*cos(rad)
			vert[0] = newX
			vert[1] = newY

class Triangle(Polygon):
	def __init__(self):
		Polygon.__init__(self, [[0,0],[0.5,sqrt(0.75)],[1,0]])

class Square(Polygon):
	def __init__(self):
		Polygon.__init__(self, [[0,0],[0,1],[1,1],[1,0]])

class Hexagon(Polygon):
	def __init__(self):
		Polygon.__init__(self, [
			[-sqrt(0.75),-0.5],
			[-sqrt(0.75),0.5],
			[0,1],
			[sqrt(0.75),0.5],
			[sqrt(0.75),-0.5],
			[0,-1]
		])

class Octagon(Polygon):
	def __init__(self):
		Polygon.__init__(self, [
			[1,1+sqrt(2)],[1,-1-sqrt(2)],
			[-1,1+sqrt(2)],[-1,-1-sqrt(2)],
			[1+sqrt(2),1],[1+sqrt(2),-1],
			[-1-sqrt(2),1],[-1-sqrt(2),-1]
		])

class Dodecagon(Polygon):
	#TODO: add Dodecagon coordinates.
	def __init__(self):
		Polygon.__init__(self, [])

def minMax(listOfPolys):
	''' Find the min and max of the x and y cooords = 4 values. '''
	xCoords = []
	yCoords = []
	for poly in listOfPolys:
		for vertex in poly.vertices:
			xCoords.append(vertex[0])
			yCoords.append(vertex[1])
	return [min(xCoords), max(xCoords), min(yCoords), max(yCoords)]

def polyToFig(listOfPolys, customLimits=None):
	''' Draw everything in listOfPolys. '''
	fig = plt.figure(figsize=(10,10))
	ax = plt.axes()
	# Remove all whitespace.
	plt.axis('off')
	fig.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
	ax.margins(0,0)
	ax.xaxis.set_major_locator(plt.NullLocator())
	ax.yaxis.set_major_locator(plt.NullLocator())
	# Force square coordinates:
	(minX, maxX, minY, maxY) = minMax(listOfPolys)
	plt.xlim([minX,maxX])
	plt.ylim([minY,maxY])
	ax.set_aspect('equal')
	# Limits override.
	if customLimits:
		plt.xlim([customLimits[0],customLimits[1]])
		plt.ylim([customLimits[2],customLimits[3]])
	# Add all the poly patches.
	for poly in listOfPolys:
		# Need a special poly type for Matplotlib.
		mplPoly = plt.Polygon(poly.vertices)
		if poly.color:
			mplPoly.set_facecolor(poly.color)
		if poly.hatch:
			mplPoly.set_hatch(poly.hatch)
		if poly.edgeWidth:
			mplPoly.set_linewidth(poly.edgeWidth)
		if poly.edgeColor:
			mplPoly.set_edgecolor(poly.edgeColor)
		ax.add_patch(mplPoly)
	return fig

def saveFig(figure, fileName):
	''' Save the figure without padding. Choose png, PDF or SVG for good results. '''
	figure.savefig(fileName, bbox_inches='tight', pad_inches = 0)

def tile(seedList, rVec, uVec, iter=3):
	''' Tile the plane with the polygons in seedList by translating them by rVec to the right and uVec up a total of iter times. Note that rTrans and uTrans can be diagonal. '''
	outList = []
	for shape in seedList:
		for rStep in range(-1*iter,iter):
			for uStep in range(-1*iter,iter):
				for poly in seedList:
					newPoly = deepcopy(poly)
					newPoly.translate(*[float(rStep)*float(p) for p in rVec])
					newPoly.translate(*[float(uStep)*float(p) for p in uVec])
					#TODO: don't just set random color
					randCol = [random(), random(), random()]
					newPoly.color = randCol
					newPoly.edgeColor = randCol
					outList.append(newPoly)
	return outList

def drawTest():
	pinkT = Triangle()
	pinkT.color = 'pink'
	pinkT.hatch = '/'
	orangeT = Triangle()
	orangeT.color = 'orange'
	orangeT.rotate(13.0)
	redHex = Hexagon()
	redHex.color = 'red'
	redHex.translate(0.0,-0.6)
	outFig = polyToFig([Square(), orangeT, pinkT, redHex])
	plt.show()

def regularTilings():
	f1 = polyToFig(tile([Triangle(),Polygon([[0.5,sqrt(0.75)],[1.5,sqrt(0.75)],[1,0]])], [1,0], [0.5,sqrt(0.75)],iter=9))
	f2 = polyToFig(tile([Square()], [1,0], [0,1]))
	f3 = polyToFig(tile([Hexagon()], [sqrt(3),0], [sqrt(0.75),1.5]))
	plt.show() # show all 3 plots.
	saveFig(f1, 'tiling.svg')

def semiRegularTilings():
	pass #TODO: implement me.

if __name__ == '__main__':
	regularTilings()
	#drawTest()
