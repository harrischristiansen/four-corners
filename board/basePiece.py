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
		self._tile_count = len(np.nonzero(tiles))

		self._canPlacePiece = 0
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

	def canPlacePiece(self, board):

		if abs(self._canPlacePiece) == board.turn:
			return self._canPlacePiece > 0
		self._canPlacePiece = board.turn

		for y in range(board.rows):
			for x in range(board.cols):
				if board.board[y][x] == None:
					tempPiece = BasePiece(self._name+"_temp", self._player, self._tiles)
					for f in range(3): # Allow placement in any orientation
						for i in range(4):
							if board.canPlacePiece(tempPiece, x, y, requireAvaiable=False):
								return True
							tempPiece.rotate()
						if f == 1:
							tempPiece.rotate()
						tempPiece.flip()

		self._canPlacePiece = -board.turn
		return False

	## --------------- Piece Actions --------------- ##

	def rotate(self, direction=1):
		self._rotation = (self._rotation + direction) % 4

	def flip(self):
		self._tiles = np.flip(self._tiles, (self._rotation + 1) % 2)
