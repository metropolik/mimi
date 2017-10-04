import sdl2, sys, sdl2.ext
from sdl2 import *
from sdl2.rect import SDL_Rect
from sdl2.timer import SDL_Delay, SDL_GetTicks
from View import View
from EntityManager import EntityManager
from Entity import Entity
from Console import Console
from time import time
from sdl2 import sdlttf
from DebugStatsViewer import DebugStatsViewer

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

class App(object):
	"""docstring for App"""
	def __init__(self):
		super(App, self).__init__()
		self.running = True

		sdl2.ext.init()
		sdlttf.TTF_Init()
		self.win = sdl2.ext.Window("Lolololol",
			size=(WINDOW_WIDTH, WINDOW_HEIGHT),
			flags=(SDL_WINDOW_RESIZABLE))
		self.win.show()
		self.ren = sdl2.ext.Renderer(self.win)
		self.renderObj = []

		self.leftClickListeners = []
		self.mouseMoveListeners = []

		#needs to be initialized before everything that uses it
		self.debugStatsViewer = DebugStatsViewer(self.ren)

		self.view = View(self.ren, WINDOW_WIDTH, WINDOW_HEIGHT)
		self.renderObj.append(self.view)

		self.renderObj.append(self.debugStatsViewer)

		self.entityManager = EntityManager(self.view)
		self.renderObj.append(self.entityManager)

		self.initResources()
		self.timeLastFrame = SDL_GetTicks()
		self.maxFPS = 60
		self.fpsCounter = 0
		self.fpsWatchStartTime = time()
		self.middleMouseDown = False

		self.entityManager.insertEntity(Entity(self.ren,
			self.view.worldToWindowTransformRect,
			'shoulders.png'))

		#register listeners
		self.mouseMoveListeners.append(self.entityManager)
		self.leftClickListeners.append(self.entityManager)

		# self.console = Console(self.ren)
		# self.renderObj.append(self.console)

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
		if time() - self.fpsWatchStartTime >= 1.0: #one second passed
			self.debugStatsViewer.cFps = self.fpsCounter
			self.fpsCounter = 0
			self.fpsWatchStartTime = time()
		self.fpsCounter += 1

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

					#nofify listeners
					for listener in self.mouseMoveListeners:
						listener.nofifyMouseMoveEvent(pos=(event.motion.x, event.motion.y))

			elif event.type == SDL_MOUSEBUTTONDOWN:
				if event.button.button == SDL_BUTTON_MIDDLE:
					self.oldMousePos = (event.button.x, event.button.y)
					self.middleMouseDown = True
				elif event.button.button == SDL_BUTTON_LEFT:
					pos = (event.button.x, event.button.y)
					pos = self.view.windowToWorldTransform(pos)
					for listener in self.leftClickListeners:
						listener.notifyLeftMouseEvent(buttonDown=True,
							pos=pos)

			elif event.type == SDL_MOUSEBUTTONUP:
				if event.button.button == SDL_BUTTON_MIDDLE:
					self.middleMouseDown = False
				elif event.button.button == SDL_BUTTON_LEFT:
					pos = (event.button.x, event.button.y)
					pos = self.view.windowToWorldTransform(pos)
					for listener in self.leftClickListeners:
						listener.notifyLeftMouseEvent(buttonDown=False,
							pos=pos)

			elif event.type == SDL_MOUSEWHEEL:
				motion = event.wheel.y * 0.07 * self.view.zoomFactor
				newZoomFactor = self.view.zoomFactor + motion
				if newZoomFactor < 2 and newZoomFactor > 0.2:
					preZF = self.view.zoomFactor
					self.view.zoomFactor += motion
					diffZF = preZF - self.view.zoomFactor
					a = (WINDOW_WIDTH/2.0)
					b = (WINDOW_HEIGHT/2.0)
					zoomOffsetw =  (-a * diffZF) / (self.view.zoomFactor * preZF)
					zoomOffseth =  (-b * diffZF) / (self.view.zoomFactor * preZF)
					self.view.x += zoomOffsetw
					self.view.y += zoomOffseth

	def handleRendering(self):
		#self.ren.clear(color = self.pink) #for debugging
		self.ren.clear(color = self.bgGrey) #to fill 1pixel gaps
		for ro in self.renderObj:
			ro.render(self.ren)
		self.ren.present()

	def updateLogic(self):
		pass

	def run(self):
		while self.running:
			self.handleInput()
			self.updateLogic()
			self.handleRendering()
			self.waitFPS()

	def __del__(self):
		sdl2.ext.quit()
