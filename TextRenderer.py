from sdl2 import sdlttf, SDL_Color, render, SDL_FreeSurface

class TextRenderer(object):
	"""docstring for TextRenderer"""
	def __init__(self, ren):
		super(TextRenderer, self).__init__()
		self.ren = ren

		self.fontColor = SDL_Color(255, 255, 255)
		sdlttf.TTF_Init()
		self.font = sdlttf.TTF_OpenFont("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 14)

	def renderTexture(self):
		text = "\n".join(self.lines)
		textSurf = sdlttf.TTF_RenderText_Blended(self.font, text, self.fontColor)
		self.clipRect = textSurf.contents.clip_rect
		self.clipRect = [getattr(self.clipRect, a) for a in ["x", "y", "w", "h"]]
		self.texture = render.SDL_CreateTextureFromSurface(
			self.ren.sdlrenderer, textSurf).contents
		SDL_FreeSurface(textSurf)

