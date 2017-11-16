'''
	@ Harris Christiansen (Harris@HarrisChristiansen.com)
	Four Corners - https://github.com/harrischristiansen/four-corners
	Game Viewer
'''

import logging
import pygame
import time

# Color Definitions
BLACK = (0,0,0)
GRAY_DARK = (110,110,110)
GRAY = (160,160,160)
WHITE = (255,255,255)
GOLD = (217, 163, 0)
PLAYER_COLORS = [(255,0,0), (0,0,255), (0,128,0), (128,0,128), (0,128,128), (0,70,0), (128,0,0), (255,165,0), (30,250,30)]

# Table Properies
CELL_WIDTH = 20
CELL_HEIGHT = 20
CELL_MARGIN = 5
PIECES_ROW_HEIGHT = 80
ACTIONBAR_ROW_HEIGHT = 25
ACTION_BTN_WIDTH = 120
ABOVE_GRID_HEIGHT = ACTIONBAR_ROW_HEIGHT
MAX_TILE_SIZE = 12

class FourCornersViewer(object):
	def __init__(self, name=None, moveEvent=None):
		self.selected_piece = None

		self._runPygame = True
		self._name = name
		self._moveEvent = moveEvent
		self._receivedUpdate = False
		self._clearSelectedPiece()

	def mainViewerLoop(self):
		while not self._receivedUpdate: # Wait for first update
			time.sleep(0.5)

		self._initViewier()

		while self._runPygame:
			for event in pygame.event.get(): # User did something
				if event.type == pygame.QUIT: # User clicked quit
					self._runPygame = False # Flag done
				elif event.type == pygame.MOUSEBUTTONDOWN: # Mouse Click
					self._handleClick(pygame.mouse.get_pos())
				elif event.type == pygame.MOUSEMOTION: # Mouse Hover
					self._handleHover(pygame.mouse.get_pos())

			if self._receivedUpdate:
				self._drawViewer()
				self._receivedUpdate = False

			time.sleep(0.1)

		pygame.quit() # Done. Quit pygame.

	''' ======================== Call to update viewer with new board state ======================== '''

	def updateBoard(self, board):
		self._board = board
		if self.selected_piece != None and self.selected_piece.player != board.currentPlayer:
			self._clearSelectedPiece()
		self._receivedUpdate = True
		return self

	''' ======================== PRIVATE METHODS - Viewer Init - PRIVATE METHODS ======================== '''

	def _initViewier(self):
		pygame.init()

		# Set Window Size
		self._grid_height = self._board.rows * (CELL_HEIGHT + CELL_MARGIN) + CELL_MARGIN
		window_height = ACTIONBAR_ROW_HEIGHT + self._grid_height + PIECES_ROW_HEIGHT
		window_width = self._board.cols * (CELL_WIDTH + CELL_MARGIN) + CELL_MARGIN
		self._window_size = [window_width, window_height]
		self._screen = pygame.display.set_mode(self._window_size)

		window_title = "Four Corners"
		if self._name != None:
			window_title += " - " + str(self._name)
		pygame.display.set_caption(window_title)
		self._font = pygame.font.SysFont('Arial', CELL_HEIGHT-10)
		self._fontLrg = pygame.font.SysFont('Arial', CELL_HEIGHT)

		self._clock = pygame.time.Clock()

	''' ======================== Handle Clicks ======================== '''

	def _handleClick(self, pos):
		self._receivedUpdate = True
		if pos[1] < ACTIONBAR_ROW_HEIGHT:
			if pos[0] < ACTION_BTN_WIDTH: # Rotate Left
				for piece in self._board.availablePieces:
					piece.rotate()
			elif pos[0] < 2*ACTION_BTN_WIDTH: # Rotate Right
				for piece in self._board.availablePieces:
					piece.rotate(-1)
			elif pos[0] < 3*ACTION_BTN_WIDTH: # Flip
				for piece in self._board.availablePieces:
					piece.flip()
			self._receivedUpdate = True
		elif pos[1] > ABOVE_GRID_HEIGHT and pos[1] < self._window_size[1] - PIECES_ROW_HEIGHT: # Click inside Grid
			grid_pos = self._transMouseToGridPos(pos)
			self._moveEvent(self.selected_piece, grid_pos[0], grid_pos[1])
			logging.debug("Click %s @ grid coordinates: %d, %d" % (pos, grid_pos[0], grid_pos[1]))
		elif pos[1] >= self._window_size[1] - PIECES_ROW_HEIGHT: # Select Piece
			pieces = self._board.availablePieces
			pieces_per_row = int(len(pieces) / 2)
			piece_width = self._window_size[0] / pieces_per_row
			piece_offset = int(pos[0] / piece_width)
			piece_row = 1 if pos[1] >= self._window_size[1] - (PIECES_ROW_HEIGHT/2) else 0
			piece_index = (piece_row*(pieces_per_row+1)) + piece_offset
			piece = pieces[piece_index]
			logging.debug("Selected piece %s" % piece)
			self.selected_piece = piece

	def _transMouseToGridPos(self, pos):
		if pos[1] >= ABOVE_GRID_HEIGHT and pos[1] <= self._window_size[1] - PIECES_ROW_HEIGHT: # Click inside Grid
			return (pos[0] // (CELL_WIDTH + CELL_MARGIN), (pos[1] - ABOVE_GRID_HEIGHT) // (CELL_HEIGHT + CELL_MARGIN))
		return (0,0)

	''' ======================== Handle Hover Preview ======================== '''

	def _handleHover(self, pos):
		if pos[1] < ABOVE_GRID_HEIGHT or pos[1] > self._window_size[1] - PIECES_ROW_HEIGHT or self.selected_piece == None: # Hover Outside Grid or no selected piece
			self._hoverTiles = {}
			self._receivedUpdate = True
			return False

		grid_pos = self._transMouseToGridPos(pos)
		piece = self.selected_piece
		if (grid_pos == self._hoverPos):
			return False

		can_place = self._board.canPlacePiece(piece, grid_pos[0], grid_pos[1])

		self._hoverTiles = {}
		for y in range(piece.height):
			for x in range(piece.width):
				g_x = grid_pos[0]+x
				g_y = grid_pos[1]+y
				if self._board.isValidPosition(g_x, g_y) and piece.tiles[y][x] == 1:
					self._hoverTiles[(g_x, g_y)] = can_place

		self._hoverPos = grid_pos
		self._receivedUpdate = True

	def _clearSelectedPiece(self):
		self.selected_piece = None
		self._hoverPos = None
		self._hoverTiles = {}

	''' ======================== Viewer Drawing ======================== '''

	def _drawViewer(self):
		self._screen.fill(BLACK) # Set BG Color
		self._drawActionbar()
		self._drawGrid()
		self._drawAvailablePieces()

		self._clock.tick(60) # Limit to 60 FPS
		pygame.display.flip() # update screen with new drawing

	def _drawActionbar(self):
		# Rotate Left Button
		pygame.draw.rect(self._screen, PLAYER_COLORS[4], [0, 0, ACTION_BTN_WIDTH, ACTIONBAR_ROW_HEIGHT])
		self._screen.blit(self._font.render("Rotate CC", True, WHITE), (10, 5))

		# Rotate Right Button
		pygame.draw.rect(self._screen, PLAYER_COLORS[5], [ACTION_BTN_WIDTH, 0, ACTION_BTN_WIDTH, ACTIONBAR_ROW_HEIGHT])
		self._screen.blit(self._font.render("Rotate Clockwise", True, WHITE), (ACTION_BTN_WIDTH+10, 5))

		# Flip Button
		pygame.draw.rect(self._screen, PLAYER_COLORS[3], [ACTION_BTN_WIDTH*2, 0, ACTION_BTN_WIDTH, ACTIONBAR_ROW_HEIGHT])
		self._screen.blit(self._font.render("Flip", True, WHITE), (ACTION_BTN_WIDTH*2+10, 5))

	def _drawAvailablePieces(self):
		pos_top = self._window_size[1] - PIECES_ROW_HEIGHT
		pieces = self._board.availablePieces
		if len(pieces) == 0:
			return False

		pieces_per_row = int((len(pieces)+1) / 2)
		piece_width = self._window_size[0] / pieces_per_row
		for i, piece in enumerate(pieces):
			pos_top = self._window_size[1] - PIECES_ROW_HEIGHT
			if i >= pieces_per_row:
				pos_top += PIECES_ROW_HEIGHT/2

			if piece.canPlacePiece(self._board):
				color = fadeColor(PLAYER_COLORS[pieces[0].player.index], 40 if i%2==0 else -40)
			else:
				color = GRAY_DARK

			self._drawPiece(piece, color, piece_width * (i % (pieces_per_row)), pos_top, piece_width)
			

	def _drawPiece(self, piece, color, pos_left, pos_top, width):
		tile_width = (width - 2) / piece.width
		tile_height = (PIECES_ROW_HEIGHT - 10) / piece.height
		tile_height = min(min(tile_height, tile_width), (PIECES_ROW_HEIGHT-5)/2/piece.height)
		tile_width = min(tile_width, tile_height)
		for y in range(piece.height):
			for x in range(piece.width):
				if piece.tiles[y][x] == 1:
					pygame.draw.rect(self._screen, color, [pos_left+1+(tile_width*x), pos_top+2+(tile_height*y), tile_width-2, tile_height-2])

	def _drawGrid(self):
		for row in range(self._board.rows):
			for column in range(self._board.cols):
				piece = self._board.board[row][column]
				# Determine BG Color
				color = WHITE
				color_font = WHITE
				if piece != None:
					color = PLAYER_COLORS[piece.player.index]

				if (column, row) in self._hoverTiles:
					can_place = self._hoverTiles[(column, row)]
					if color == WHITE:
						color = fadeColor(PLAYER_COLORS[self.selected_piece.player.index], -80 if can_place else 80)
					else:
						color = GRAY_DARK

				# Draw Rect
				pos_left = (CELL_MARGIN + CELL_WIDTH) * column + CELL_MARGIN
				pos_top = (CELL_MARGIN + CELL_HEIGHT) * row + CELL_MARGIN + ABOVE_GRID_HEIGHT
				pygame.draw.rect(self._screen, color, [pos_left, pos_top, CELL_WIDTH, CELL_HEIGHT])

''' ======================== Color Manipulation ======================== '''

def fadeColor(color, increaseBy=5):
	return (sorted((0, (color[0]+increaseBy), 255))[1],
		sorted((0, (color[1]+increaseBy), 255))[1],
		sorted((0, (color[2]+increaseBy), 255))[1])
