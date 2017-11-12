'''
	@ Harris Christiansen (Harris@HarrisChristiansen.com)
	Four Corners - https://github.com/harrischristiansen/four-corners
	Player: Player object for game
'''

class Player(object):
	def __init__(self, index):
		self.available_pieces = []
		
		self._index = index

	@property
	def index(self):
		return self._index

	@property
	def isDead(self):
		return False
