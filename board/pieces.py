'''
	@ Harris Christiansen (Harris@HarrisChristiansen.com)
	Four Corners - https://github.com/harrischristiansen/four-corners
	Pieces: Definition of all game pieces
'''

from .basePiece import BasePiece

class Single(BasePiece):
	def __init__(self, player):
		tiles = [
			[1],
		]
		super().__init__("single", player, tiles=tiles)

class Double(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 1],
		]
		super().__init__("double", player, tiles=tiles)

class Three_Bar(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 1, 1],
		]
		super().__init__("three bar", player, tiles=tiles)

class Three_L(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 1],
			[1, 0],
		]
		super().__init__("three L", player, tiles=tiles)

class Four_L(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 1, 1],
			[1, 0, 0],
		]
		super().__init__("four L", player, tiles=tiles)

class Four_Bar(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 1, 1, 1],
		]
		super().__init__("four bar", player, tiles=tiles)

class Four_Pyramid(BasePiece):
	def __init__(self, player):
		tiles = [
			[0, 1, 0],
			[1, 1, 1],
		]
		super().__init__("four pyramid", player, tiles=tiles)

class Four_Square(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 1],
			[1, 1],
		]
		super().__init__("four square", player, tiles=tiles)

class Four_ZigZag(BasePiece):
	def __init__(self, player):
		tiles = [
			[0, 1, 1],
			[1, 1, 0],
		]
		super().__init__("four zigzag", player, tiles=tiles)

class Five_C(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 1],
			[1, 0],
			[1, 1],
		]
		super().__init__("five C", player, tiles=tiles)

class Five_F(BasePiece):
	def __init__(self, player):
		tiles = [
			[0, 1, 1],
			[1, 1, 0],
			[0, 1, 0],
		]
		super().__init__("five f", player, tiles=tiles)

class Five_L(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 1, 1, 1],
			[1, 0, 0, 0],
		]
		super().__init__("five L", player, tiles=tiles)

class Five_T(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 1, 1],
			[0, 1, 0],
			[0, 1, 0],
		]
		super().__init__("five T", player, tiles=tiles)

class Five_W(BasePiece):
	def __init__(self, player):
		tiles = [
			[0, 1, 1],
			[1, 1, 0],
			[1, 0, 0],
		]
		super().__init__("five W", player, tiles=tiles)

class Five_Y(BasePiece):
	def __init__(self, player):
		tiles = [
			[0, 1, 0, 0],
			[1, 1, 1, 1],
		]
		super().__init__("five y", player, tiles=tiles)

class Five_Z(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 1, 0],
			[0, 1, 0],
			[0, 1, 1],
		]
		super().__init__("five Z", player, tiles=tiles)

class Five_Angle(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 0, 0],
			[1, 0, 0],
			[1, 1, 1],
		]
		super().__init__("five angle", player, tiles=tiles)

class Five_Bar(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 1, 1, 1, 1],
		]
		super().__init__("five bar", player, tiles=tiles)

class Five_Cross(BasePiece):
	def __init__(self, player):
		tiles = [
			[0, 1, 0],
			[1, 1, 1],
			[0, 1, 0],
		]
		super().__init__("five cross", player, tiles=tiles)

class Five_Utah(BasePiece):
	def __init__(self, player):
		tiles = [
			[1, 0],
			[1, 1],
			[1, 1],
		]
		super().__init__("five utah", player, tiles=tiles)

class Five_ZigZag(BasePiece):
	def __init__(self, player):
		tiles = [
			[0, 1, 1, 1],
			[1, 1, 0, 0],
		]
		super().__init__("five zigzag", player, tiles=tiles)
