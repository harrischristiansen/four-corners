'''
	@ Harris Christiansen (Harris@HarrisChristiansen.com)
	Four Corners - https://github.com/harrischristiansen/four-corners
	BasePiece: Base definition of all game pieces
'''

class BasePiece(object):
	def __init__(self, name, player, tiles):
		self._name = name
		self._player = player
		self._tiles = tiles									# self._tiles[y][x] = 0 || 1
		self._width = len(tiles[0])
		self._height = len(tiles)
		self._tile_count = sum(t.count(1) for t in tiles)

	@property
	def name(self):
		return self._name
	@property
	def player(self):
		return self._player
	@property
	def tiles(self):
		return self._tiles
	@property
	def width(self):
		return self._width
	@property
	def height(self):
		return self._height
	@property
	def tile_count(self):
		return self._tile_count
