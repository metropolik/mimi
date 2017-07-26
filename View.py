from sdl2.ext import load_image
from sdl2 import (render, surface)
from sdl2 import SDL_Texture
from numpy import dot


class View(object):
	"""docstring for View"""
	def __init__(self, ren, win_width, win_height):
		super(View, self).__init__()		
		self.width = win_width
		self.height = win_height		

		self.elementsInView = []

		backgroundSurf = load_image("backgroundTile.png")
		if backgroundSurf is None:
			raise Exception("Could not load background")
		self.bgTileWidth = backgroundSurf.w
		self.bgTileHeight = backgroundSurf.h
		self.background = render.SDL_CreateTextureFromSurface(
			ren.sdlrenderer, backgroundSurf).contents
		if self.background is None:
			raise Exception("Could not convert to texture")

		self.tilesInView = set()
		self.zoomFactor = 1.0
		self.x, self.y = 0, 0 #causes updateView			

	def updateView(self):
		self.calcTilesInView()
		self.calcViewMatrix()

	def calcViewMatrix(self):
		self.viewMatrix = [[self.zoomFactor, 0.0, -self.x],
							[0.0, self.zoomFactor, -self.y],
							[0.0, 0.0, 1.0]]

	def worldToWindowTransform(self, point):
		return dot(self.viewMatrix, point + [1.0]).tolist()[:-1]

	def worldToWindowTransformRect(self, rect):
		pa, pb = rect[:2], rect[2:]
		return worldToWindowTransform(pa) + \
				 worldToWindowTransform(pb)

	def findClosestMultiple(self, x, b):
		return int(float(x)/float(b))*b

	def calcTilesInView(self):
		self.tilesInView.clear()
		#calc upper left corner that is in view
		xul = self.findClosestMultiple(self.x, self.bgTileWidth)
		xul = xul if xul >= self.x else xul + self.bgTileWidth
		yul = self.findClosestMultiple(self.y, self.bgTileHeight)
		yul = yul if yul >= self.y else yul + self.bgTileHeight

		#instead use upper left corner that is not in view
		xul -= self.bgTileWidth
		yul -= self.bgTileHeight
		
		#add all other corners that are in view
		cx = xul
		cy = yul
		it = 0
		while self.x + self.width > cx:
			while self.y + self.height > cy:
				corner = (cx, cy)
				self.tilesInView.add(corner)			
				cy += self.bgTileHeight
			cx += self.bgTileWidth
			cy = yul
			it += 1
		print "tiles to render: ", len(self.tilesInView)

	@property
	def x(self):
		return self._x

	@property 
	def y(self):
		return self._y

	@x.setter #only y causes update since x and y are always set together
	def x(self, val): #hopefully
		self._x = val

	@y.setter
	def y(self, val):
		self._y = val
		self.updateView()
		print "new pos", self.x, self.y

	def drawTileAt(self, ren, x, y):		
		ren.copy(self.background, dstrect = (x, y, 
			self.bgTileWidth, self.bgTileHeight))
	

	def render(self, ren):
		for x, y in self.tilesInView:
			self.drawTileAt(ren, x-self.x, y - self.y)

		