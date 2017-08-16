from sdl2 import sdlttf, SDL_Color, render, SDL_FreeSurface, SDL_TEXTUREACCESS_TARGET, SDL_CreateTexture, SDL_PIXELFORMAT_RGBA8888, SDL_SetTextureBlendMode, SDL_BLENDMODE_BLEND

class TextRenderer(object):
	"""TextRenderer sdlttf must initialized already"""
	def __init__(self, ren):
		super(TextRenderer, self).__init__()
		self.ren = ren

		self.fontColor = SDL_Color(255, 255, 255)
		self.font = sdlttf.TTF_OpenFont("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 18)
		self.glyphTextures = {}
		self.charSpacing = 0 #in pixel
		self.format = SDL_PIXELFORMAT_RGBA8888

	def addNewGlyph(self, glyph):
		glyphSurface = sdlttf.TTF_RenderGlyph_Blended(self.font, ord(glyph), self.fontColor)
		clipRect = glyphSurface.contents.clip_rect
		clipRect = [getattr(clipRect, a) for a in ["x", "y", "w", "h"]]
		#print "clipRect", clipRect
		texture = render.SDL_CreateTextureFromSurface(self.ren.sdlrenderer, glyphSurface).contents
		SDL_FreeSurface(glyphSurface)
		self.glyphTextures[glyph] = (texture, clipRect)

	def renderTexture(self, text):
		if not text:
			return None

		rHeight = 0
		rWidth = 0
		for i, char in enumerate(text):
			if char not in self.glyphTextures:
				#print "new char", char, ord(char)
				self.addNewGlyph(char)

			glyphHeight = self.glyphTextures[char][1][3]
			if glyphHeight > rHeight:
				rHeight = glyphHeight
			glyphWidth = self.glyphTextures[char][1][2]
			rWidth += glyphWidth
			if i != len(text) - 1: #do not add spacing after last char
				rWidth += self.charSpacing

		rTexture = SDL_CreateTexture(self.ren.sdlrenderer, self.format, SDL_TEXTUREACCESS_TARGET, rWidth, rHeight)
		SDL_SetTextureBlendMode(rTexture.contents, SDL_BLENDMODE_BLEND)

		oldRenderTarget = render.SDL_GetRenderTarget(self.ren.sdlrenderer)
		render.SDL_SetRenderTarget(self.ren.sdlrenderer, rTexture)

		cx = 0
		for char in text:
			texture = self.glyphTextures[char][0]
			dstRect = self.glyphTextures[char][1]
			dstRect[0] = cx
			self.ren.copy(texture, dstrect = dstRect)
			cx += dstRect[2]
			cx += self.charSpacing
		render.SDL_SetRenderTarget(self.ren.sdlrenderer, oldRenderTarget)
		return (rTexture.contents, (0, 0, rWidth, rHeight))
