from sdl2.ext import load_image
from sdl2 import (render, surface)
from sdl2 import SDL_Texture, SDL_FreeSurface
from numpy import dot


class View(object):
	"""docstring for View"""
	def __init__(self, ren, win_width, win_height):
		super(View, self).__init__()		
		self.width = win_width
		self.height = win_height
		self.win_width = win_width
		self.win_height = win_height		

		self.elementsInView = []

		backgroundSurf = load_image("backgroundTile.png")
		if backgroundSurf is None:
			raise Exception("Could not load background")
		self.bgTileWidth = backgroundSurf.w
		self.bgTileHeight = backgroundSurf.h
		self.background = render.SDL_CreateTextureFromSurface(
			ren.sdlrenderer, backgroundSurf).contents
		SDL_FreeSurface(backgroundSurf)
		if self.background is None:
			raise Exception("Could not convert to texture")

		self.tilesInView = list()
		self.zoomFactor = 1.0
		self.x, self.y = 0, 0 #causes updateView

	def updateView(self):
		self.calcViewMatrix()
		self.calcTilesInView()

	def calcViewMatrix(self):
		self.width = self.win_width * (1.0/self.zoomFactor)
		self.height = self.win_height * (1.0/self.zoomFactor)
		self.viewMatrix = [[self.zoomFactor, 0.0, -self.x * self.zoomFactor],
							[0.0, self.zoomFactor, -self.y * self.zoomFactor],
							[0.0, 0.0, 1.0]]

	def calcViewMatrixP(self):
		self.width = self.win_width * (1.0/self.zoomFactor)
		self.height = self.win_height * (1.0/self.zoomFactor)
		self.viewMatrix = [[self.zoomFactor, 0.0, -self.x * self.zoomFactor - self.zoomFocusPt[0] * self.zoomFactor + self.zoomFocusPt[0]],
							[0.0, self.zoomFactor, -self.y * self.zoomFactor - self.zoomFocusPt[1] * self.zoomFactor + self.zoomFocusPt[1]],
							[0.0, 0.0, 1.0]]		

	def worldToWindowTransform(self, point):		
		return dot(self.viewMatrix, point + [1.0]).tolist()[:-1]

	def worldToWindowTransformRect(self, rect):
		pa, pb = rect[:2], rect[2:] #pb is width and height
		#make pb absolute
		pb[0], pb[1] = pb[0] + pa[0], pb[1] + pa[1]
		pa = self.worldToWindowTransform(pa)
		pb = self.worldToWindowTransform(pb) #transform
		#make pb rel. again
		pb[0], pb[1] = pb[0] - pa[0], pb[1] - pa[1]
		return pa + pb

	def findClosestMultiple(self, x, b):
		return (x//b)*b

	def calcTilesInView(self):
		del self.tilesInView[:]
		#calc upper left corner that is in just out of view
		xul = self.findClosestMultiple(self.x, 
			self.bgTileWidth)		
		yul = self.findClosestMultiple(self.y, 
			self.bgTileHeight)
	
		
		#add all other corners that are in view
		cx = xul
		cy = yul		
		while self.x + self.width > cx:
			while self.y + self.height > cy:
				corner = [cx, cy]
				self.tilesInView.append(corner)			
				cy += self.bgTileHeight
			cx += self.bgTileWidth
			cy = yul				
		print "tiles to render: ", len(self.tilesInView)

	@property
	def zoomFactor(self):
		return self._zoomFactor

	@zoomFactor.setter
	def zoomFactor(self, val):
		self._zoomFactor = val
		if hasattr(self, "x"):
			self.updateView()

	@property
	def x(self):
		return self._x

	@property 
	def y(self):
		return self._y

	#only y causes update 
	#since x and y are always set together
	@x.setter
	def x(self, val): #hopefully
		self._x = val

	@y.setter
	def y(self, val):
		self._y = val
		self.updateView()
		print "new pos", self.x, self.y

	def drawTileAt(self, ren, dst):		
		ren.copy(self.background, dstrect = dst)
	

	def render(self, ren):
		for x, y in self.tilesInView:
			dst = self.worldToWindowTransformRect([x, y,
				self.bgTileWidth, self.bgTileHeight])
			dst = list(map(lambda x: int(round(x, 0)), dst))
			self.drawTileAt(ren, dst)

		