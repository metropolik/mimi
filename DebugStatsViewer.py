from sdl2 import sdlttf, SDL_Color, render, SDL_FreeSurface, SDL_DestroyTexture
from TextRenderer import TextRenderer
from time import time

class DebugStatsViewer(object):
	"""DebugStatsViewer uses Borg pattern"""
	__shared_state = {}

	def __init__(self, ren = None):
		self.__dict__ = self.__shared_state
		super(DebugStatsViewer, self).__init__()

		#being instanciated for the first time
		#(borg calls init for each creation)
		if not hasattr(self, "ren"):
			self.ren = ren
			self.textRenderer = TextRenderer(self.ren)

			#init vars
			self._cFps = 0
			self._entitiesToRenderCount = 0
			self._pos = (0, 0)
			self._tilesToRenderCount = 0
			self.lastUpdated = time() - 1
			self.updateStats()

	@property
	def cFps(self):
		return self._cFps

	@cFps.setter
	def cFps(self, val):
		self._cFps = val
		self.updateStats()

	@property
	def entitiesToRenderCount(self):
		return self._entitiesToRenderCount

	@entitiesToRenderCount.setter
	def entitiesToRenderCount(self, val):
		self._entitiesToRenderCount = val
		self.updateStats()

	@property
	def pos(self):
		return self._pos

	@pos.setter
	def pos(self, val):
		self._pos = val
		#self.updateStats()

	@property
	def tilesToRenderCount(self):
		return self._tilesToRenderCount

	@tilesToRenderCount.setter
	def tilesToRenderCount(self, val):
		self._tilesToRenderCount = val
		self.updateStats()

	def updateStats(self):
		"""Creates a new stats Texture"""

		#only allow 10 text renders per second
		if time() - self.lastUpdated < 0.1:
			return
		if hasattr(self, "statsTexture") and self.statsTexture:
			SDL_DestroyTexture(self.statsTexture)
		statsText = str(self.cFps) + " FPS TilesToRender: " + str(self.tilesToRenderCount) + \
			" EToRender: " + str(self.entitiesToRenderCount) + " pos: " + str(self.pos)
		self.statsTexture, self.clipRect = self.textRenderer.renderTexture(statsText)
		self.lastUpdated = time()

	def render(self, ren):
		ren.copy(self.statsTexture, dstrect=self.clipRect)
