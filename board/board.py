'''
	@ Harris Christiansen (Harris@HarrisChristiansen.com)
	Four Corners - https://github.com/harrischristiansen/four-corners
	Board: Game Board
'''

BOARD_WIDTH = 20
BOARD_HEIGHT = 20

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
CORNER_DIRECTIONS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

from . import pieces

import logging

class Board(object):
	def __init__(self, players):
		self._players = players
		self._player_count = len(players)
		self._current_player = self._players[0]

		self._rows = BOARD_HEIGHT
		self._cols = BOARD_WIDTH
		self._board = [[None for x in range(self.cols)] for y in range(self.rows)]		# self._board[y][x] = piece

		for player in self._players:
			self.resetPieces(player)

	################################ Properties ################################

	@property
	def rows(self):
		return self._rows
	@property
	def cols(self):
		return self._cols
	@property
	def board(self):
		return self._board
	@property
	def currentPlayer(self):
		return self._current_player
	@property
	def availablePieces(self):
		return self._current_player.available_pieces

	################################ Board Setup ################################

	def resetPieces(self, player):
		player.available_pieces = self._createPieces(player)

	def _createPieces(self, player):
		return [
			pieces.Single(player),
			pieces.Double(player),
			pieces.Three_Bar(player),
			pieces.Three_L(player),
			pieces.Four_L(player),
			pieces.Four_Bar(player),
			pieces.Four_Pyramid(player),
			pieces.Four_Square(player),
			pieces.Four_ZigZag(player),
			pieces.Five_C(player),
			pieces.Five_F(player),
			pieces.Five_L(player),
			pieces.Five_T(player),
			pieces.Five_W(player),
			pieces.Five_Y(player),
			pieces.Five_Z(player),
			pieces.Five_Angle(player),
			pieces.Five_Bar(player),
			pieces.Five_Cross(player),
			pieces.Five_Utah(player),
			pieces.Five_ZigZag(player),
		]

	################################ Move Making ################################

	def placePiece(self, piece, top_left_x, top_left_y):
		if piece == None or not self._isValidPosition(top_left_x, top_left_y):
			return False

		if self._assignPiece(piece, top_left_x, top_left_y):
			self._next_player()
			return True
		return False

	def _next_player(self):
		if self._current_player not in self._players:
			self._current_player = self._players[0]
			return

		# Update self._current_player to next player
		index = self._players.index(self._current_player)
		next_index = (index + 1) % self._player_count
		self._current_player = self._players[next_index]

	def _assignPiece(self, piece, top_left_x, top_left_y):
		if not self._canPlacePiece(piece, top_left_x, top_left_y):
			return False
		piece.player.available_pieces.remove(piece)

		for y in range(piece.height):
			for x in range(piece.width):
				if piece.tiles[y][x] == 1:
					self._assignTile(piece, top_left_x+x, top_left_y+y)

		return True

	def _assignTile(self, piece, x, y):
		if self._board[y][x] == None:
			self._board[y][x] = piece
			return True
		raise ValueError("Error: Tile already assigned during call to _assignTile")

	################################ Move Validation ################################

	def _canPlacePiece(self, piece, top_left_x, top_left_y):
		if not piece in piece.player.available_pieces:
			return False

		touchesCorner = False
		for y in range(piece.height):
			for x in range(piece.width):
				if piece.tiles[y][x] == 1:
					if self._doesTouchCorner(piece, top_left_x+x, top_left_y+y):
						touchesCorner = True
					if not self._canPlaceTile(piece, top_left_x+x, top_left_y+y):
						return False
		return touchesCorner

	def _doesTouchCorner(self, piece, x, y):
		if (x == 0 or x == self.cols-1) and (y == 0 or y == self.rows-1):
			return True

		for corner in self._tile_corners(x, y):
			if corner.player == piece.player:
				return True
		return False

	def _canPlaceTile(self, piece, x, y):
		if not self._isValidPosition(x, y) or self._board[y][x] != None:
			return False
		for neighbor in self._tile_neighbors(x, y):
			if neighbor.player == piece.player:
				return False
		return True

	################################ Tile Selection ################################

	def _tile_neighbors(self, x, y):
		neighbors = []
		for dy, dx in DIRECTIONS:
			if self._isValidPosition(x+dx, y+dy):
				if self._board[y+dy][x+dx] != None:
					neighbors.append(self._board[y+dy][x+dx])
		return neighbors

	def _tile_corners(self, x, y):
		corners = []
		for dy, dx in CORNER_DIRECTIONS:
			if self._isValidPosition(x+dx, y+dy):
				if self._board[y+dy][x+dx] != None:
					corners.append(self._board[y+dy][x+dx])
		return corners

	def _isValidPosition(self, x, y):
		return 0 <= y < self._rows and 0 <= x < self._cols


