'''
	@ Harris Christiansen (Harris@HarrisChristiansen.com)
	Four Corners - https://github.com/harrischristiansen/four-corners
	BasePiece: Base definition of all game pieces
'''

import numpy as np

class BasePiece(object):
	def __init__(self, name, player, tiles):
		self._name = name
		self._player = player
		self._tiles = tiles									# self._tiles[y][x] = 0 || 1
		self._width = len(tiles[0])
		self._height = len(tiles)
		self._tile_count = sum(t.count(1) for t in tiles)
		self._rotation = 0

	@property
	def name(self):
		return self._name
	@property
	def player(self):
		return self._player
	@property
	def tiles(self):
		return np.rot90(self._tiles, k=self._rotation)
	@property
	def width(self):
		if self._rotation % 2 == 1:
			return self._height
		return self._width
	@property
	def height(self):
		if self._rotation % 2 == 1:
			return self._width
		return self._height
	@property
	def tile_count(self):
		return self._tile_count

	def rotate(self, direction=1):
		self._rotation = (self._rotation + direction) % 4

	def flip(self):
		self._tiles = np.flip(self._tiles, (self._rotation + 1) % 2)
