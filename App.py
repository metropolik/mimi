import sdl2, sys, sdl2.ext
from sdl2 import *
from sdl2.rect import SDL_Rect
from sdl2.timer import SDL_Delay, SDL_GetTicks
from View import View
from EntityManager import EntityManager
from Entity import Entity

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

class App(object):
	"""docstring for App"""
	def __init__(self):
		super(App, self).__init__()
		self.running = True

		sdl2.ext.init()
		self.win = sdl2.ext.Window("Lolololol", 
			size=(WINDOW_WIDTH, WINDOW_HEIGHT),
			flags=(SDL_WINDOW_RESIZABLE))
		self.win.show()
		self.ren = sdl2.ext.Renderer(self.win)		
		self.renderObj = []
		self.view = View(self.ren, WINDOW_WIDTH, WINDOW_HEIGHT)
		self.renderObj.append(self.view)
		self.entityManager = EntityManager(self.view)
		self.renderObj.append(self.entityManager)
		self.initResources()
		self.timeLastFrame = SDL_GetTicks()
		self.maxFPS = 60		
		self.middleMouseDown = False

		self.entityManager.insertEntity(Entity(self.ren, 
			self.view.worldToWindowTransformRect,
			'shoulders.png'))


	@property
	def maxFPS(self):		
		return self._maxFPS

	@maxFPS.setter
	def maxFPS(self, val):		
		self._maxFPS = val
		#turn into ms instead of sec
		self._timePerFrame = (1.0/self._maxFPS) * 1000

	def initResources(self):
		self.blue = sdl2.ext.Color(50, 150, 250)
		self.pink = sdl2.ext.Color(255, 0, 255)
		self.bgGrey = sdl2.ext.Color(57, 57, 57)
		self.rects = ((0, 0, 32, 32))

	def waitFPS(self):
		currentTime = SDL_GetTicks()
		passedTime = currentTime - self.timeLastFrame
		waitTime = round(self._timePerFrame - passedTime, 0)
		waitTime = waitTime if waitTime > 0 else 0
		SDL_Delay(int(waitTime))

		self.timeLastFrame = SDL_GetTicks()


	def handleInput(self):
		for event in sdl2.ext.get_events():
			if event.type == SDL_QUIT:
				self.running = False
				break
			elif event.type == SDL_MOUSEMOTION:
				self.currentMousePos = (event.motion.x, event.motion.y)
				if self.middleMouseDown:
					newMousePos = self.currentMousePos				
					self.view.x += (self.oldMousePos[0] - newMousePos[0]) / self.view.zoomFactor
					self.view.y += (self.oldMousePos[1] - newMousePos[1]) / self.view.zoomFactor
					self.oldMousePos = newMousePos

			elif event.type == SDL_MOUSEBUTTONDOWN:				
				if event.button.button == SDL_BUTTON_MIDDLE:
					self.oldMousePos = (event.button.x, event.button.y)				
					self.middleMouseDown = True

			elif event.type == SDL_MOUSEBUTTONUP:				
				if event.button.button == SDL_BUTTON_MIDDLE:				
					self.middleMouseDown = False

			elif event.type == SDL_MOUSEWHEEL:							
				motion = event.wheel.y * 0.025
				# self.view.x += (-self.currentMousePos[0] * self.view.zoomFactor + self.currentMousePos[0])/self.view.zoomFactor
				# self.view._y += (-self.currentMousePos[1] * self.view.zoomFactor + self.currentMousePos[1])/self.view.zoomFactor
				newZoomFactor = self.view.zoomFactor + motion
				if newZoomFactor < 2 and newZoomFactor > 0.4:
					self.view.zoomFactor += motion		

	def handleRendering(self):
		#self.ren.clear(color = self.pink) #for debugging
		self.ren.clear(color = self.bgGrey) #to fill 1pixel gaps
		for ro in self.renderObj:
			ro.render(self.ren)		
		self.ren.present()

	def run(self):
		while self.running:			
			self.handleInput()
			self.handleRendering()
			self.waitFPS()

	def __del__(self):		
		sdl2.ext.quit()


