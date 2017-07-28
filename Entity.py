from sdl2 import SDL_FreeSurface
from sdl2.ext import load_image
from sdl2 import (render, surface)

class Entity(object):
	"""docstring for Entity"""
	def __init__(self, ren, transform, imgPath):
		super(Entity, self).__init__()
		self.x = 0
		self.y = 0
		self.loadImage(ren, imgPath)
		self.transform = transform
		

	def loadImage(self, ren, path):
		entitySurf = load_image(path)
		if entitySurf is None:
			raise Exception("Could not load image " + str(path))
		self.width = entitySurf.w
		self.height = entitySurf.h
		self.texture = render.SDL_CreateTextureFromSurface(
			ren.sdlrenderer, entitySurf).contents
		SDL_FreeSurface(entitySurf)
		if self.texture is None:
			raise Exception("Could not convert to texture")

	def render(self, ren):
		dst = self.transform([self.x, self.y, 
			self.width, self.height])
		dst = list(map(lambda x: int(round(x, 0)), dst))
		ren.copy(self.texture, dstrect = dst)
		