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
		self._players = [Player(0), Player(1), Player(2), Player(3)]
		self._board = Board(self._players)
		self._viewer = FourCornersViewer(moveEvent=self.makeMove)
		self.updateViewer()

	######################### Move Making #########################

	def makeMove(self, piece, top_left_x, top_left_y):
		self._board.placePiece(piece, top_left_x, top_left_y)
		self.updateViewer()

	######################### Viewer #########################

	def mainViewerProcess(self):
		self._viewer.mainViewerLoop()

	def updateViewer(self):
		self._viewer.updateBoard(self._board)
