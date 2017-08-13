from sdl2 import sdlttf, SDL_Color, render, SDL_FreeSurface, SDL_DestroyTexture
from TextRenderer import TextRenderer

class Console(object):
	"""docstring for Console"""
	def __init__(self, ren):
		super(Console, self).__init__()
		self.ren = ren
		self.textRenderer = TextRenderer(self.ren)
		self.fontColor = SDL_Color(255, 255, 255)
		sdlttf.TTF_Init()
		self.font = sdlttf.TTF_OpenFont("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 14)
		self.lines = ["hall o", "mallo", "10FPS"]

	@property
	def lines(self):
		return self._lines

	@lines.setter
	def lines(self, var):
		self._lines = var
		self.renderTexture()

	def renderTexture(self):
		if hasattr(self, "texture") and self.texture:
			SDL_DestroyTexture(self.texture)
		self.texture, self.clipRect = self.textRenderer.renderTexture("\n".join(self.lines))

	def render(self, ren):
		ren.copy(self.texture, dstrect=self.clipRect)

