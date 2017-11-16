'''
	@ Harris Christiansen (Harris@HarrisChristiansen.com)
	Four Corners - https://github.com/harrischristiansen/four-corners
	Game: Four Corners Game Manager
'''

from player import Player
from viewer import FourCornersViewer
from board.board import Board

class FourCornersGame(object):
	def __init__(self):
		self._players = [Player(self, 0), Player(self, 1), Player(self, 2), Player(self, 3)]
		self._board = Board(self._players)
		self._viewer = FourCornersViewer(moveEvent=self.makeMove)
		self._updateViewer()

	@property
	def board(self):
		return self._board

	######################### Move Making #########################

	def makeMove(self, piece, top_left_x, top_left_y):
		self._board.placePiece(piece, top_left_x, top_left_y)
		self._updateViewer()

	######################### Viewer #########################

	def mainViewerProcess(self):
		self._viewer.mainViewerLoop()

	def _updateViewer(self):
		self._viewer.updateBoard(self._board)
