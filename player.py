'''
	@ Harris Christiansen (Harris@HarrisChristiansen.com)
	Four Corners - https://github.com/harrischristiansen/four-corners
	Player: Player object for game
'''

class Player(object):
	def __init__(self, game, index):
		self.available_pieces = []
		
		self._game = game
		self._index = index

	@property
	def index(self):
		return self._index

	@property
	def isDead(self):
		for piece in self.available_pieces:
			if piece.canPlacePiece(self._game.board):
				return False
		return True
