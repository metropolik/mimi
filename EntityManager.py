
class EntityManager(object):
	"""docstring for EntityManager"""
	def __init__(self, view):
		super(EntityManager, self).__init__()
		self.view = view
		self.TILESIZE = 256		
		self.oldView = (self.view.x, self.view.y, 
			self.view.width, self.view.height)

		#saves for each entity in which bucket it is
		self._bucketEntity = {}

		#stores for each Tile which entites are in it
		#1 Bucket = 1 Tile
		self._entityBuckets = {}

		self._inViewEntities = set()		

	def insertEntity(self, entity):
		"""	Assumes the entity is no larger than 4 tiles
			adds the 4 corners into the entityBuckets """

		if not entity in self._bucketEntity:
				self._bucketEntity = list()

		for corner in ((entity.x, entity.y), #upper left
			(entity.x + entity.width, entity.y), #upper right
			(entity.x, entity.y + entity.height), #lower left
			(entity.x + entity.width, 
				entity.y + entity.height)):

			#get tile
			corner = self.findTile(corner, self.TILESIZE)

			#if entity bucket of tile does not already exist
			#create one
			if not corner in self._entityBuckets:
				self._entityBuckets[corner] = set()

			#add to bucket (because set, no duplicates)			
			self._entityBuckets[corner].add(entity)			
			#add bucket to bucketEntity
			self._bucketEntity.append(
				self._entityBuckets[corner])

		self.updateEntitesInView()


	def removeEntity(self, entity, destroyBucketEntity = True):
		if entity not in self._bucketEntity:
			return
		for bucket in self._bucketEntity[entity]:
			bucket.remove(entity)
		if destroyBucketEntity:			
			del self._bucketEntity[entity]


	def updateEntity(self, entity):
		self.removeEntity(entity, destroyBucketEntity = False)
		self.insertEntity(entity)

	def findTile(self, c, b):
		"""returns the tile this coordinate is in
		tiles are always defined by their upper left
		corner"""
		return ((c[0]//b)*b, (c[1]//b)*b)

	def updateEntitesInView(self):
		#cannot reuse View's calcTileInView since it is
		#dependend on the tile size


		self._inViewEntities.clear()
		#calc upper left corner that is just out of view
		xul, yul = self.findTile((self.view.x, self.view.y), 
			self.TILESIZE)	
		
		#add all other corners that are in view
		cx = xul
		cy = yul
		#iterate over all tiles that are in view
		#and union the entites they are holding
		while self.view.x + self.view.width > cx:
			while self.view.y + self.view.height > cy:
				corner = (cx, cy)
				if corner in self._entityBuckets:
					self._inViewEntities = self. \
						_inViewEntities.union(
							self._entityBuckets[corner])
				cy += self.TILESIZE
			cx += self.TILESIZE
			cy = yul				
		print "entities to render: ", len(self._inViewEntities)

	def render(self, ren):
		currentView = (self.view.x, self.view.y, 
			self.view.width, self.view.height)
		if currentView != self.oldView:
			self.updateEntitesInView()
			self.oldView = currentView
		for e in self._inViewEntities:
			e.render(ren)
