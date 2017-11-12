'''
	@ Harris Christiansen (Harris@HarrisChristiansen.com)
	Four Corners - https://github.com/harrischristiansen/four-corners
	Game Viewer
'''

import logging
import pygame
import threading
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
SCORES_ROW_HEIGHT = 28
ACTIONBAR_ROW_HEIGHT = 25
TOGGLE_GRID_BTN_WIDTH = 75
TOGGLE_EXIT_BTN_WIDTH = 65
ABOVE_GRID_HEIGHT = ACTIONBAR_ROW_HEIGHT

class GeneralsViewer(object):
	def __init__(self, name=None):
		self._runPygame = True
		self._name = name
		self._receivedUpdate = False
		self._showGrid = True

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

			if (self._receivedUpdate):
				self._drawViewer()
				self._receivedUpdate = False

			time.sleep(0.2)

		pygame.quit() # Done. Quit pygame.

	''' ======================== Call to update viewer with new board state ======================== '''

	def updateBoard(self, board):
		self._board = board
		self._scores = sorted(update.scores, key=lambda general: general['total'], reverse=True) # Sort Scores
		self._receivedUpdate = True

		return self

	''' ======================== PRIVATE METHODS - Viewer Init - PRIVATE METHODS ======================== '''

	def _initViewier(self):
		pygame.init()

		# Set Window Size
		self._grid_height = self._board.rows * (CELL_HEIGHT + CELL_MARGIN) + CELL_MARGIN
		window_height = ACTIONBAR_ROW_HEIGHT + self._grid_height + SCORES_ROW_HEIGHT
		window_width = self._board.cols * (CELL_WIDTH + CELL_MARGIN) + CELL_MARGIN
		self._window_size = [window_width, window_height]
		self._screen = pygame.display.set_mode(self._window_size)

		window_title = "Four Corners"
		if (self._name != None):
			window_title += " - " + str(self._name)
		pygame.display.set_caption(window_title)
		self._font = pygame.font.SysFont('Arial', CELL_HEIGHT-10)
		self._fontLrg = pygame.font.SysFont('Arial', CELL_HEIGHT)

		self._clock = pygame.time.Clock()

	''' ======================== Handle Clicks ======================== '''

	def _handleClick(self, pos):
		if (pos[1] < ABOVE_GRID_HEIGHT):
			if (pos[0] < TOGGLE_GRID_BTN_WIDTH): # Toggle Grid
				self._toggleGrid()
			elif (pos[0] < TOGGLE_GRID_BTN_WIDTH+TOGGLE_EXIT_BTN_WIDTH): # Toggle Exit on Game Over
				self._board.exit_on_game_over = not self._board.exit_on_game_over
			self._receivedUpdate = True
		elif pos[1] > ABOVE_GRID_HEIGHT and pos[1] < self._window_size[1]-SCORES_ROW_HEIGHT: # Click inside Grid
			column = pos[0] // (CELL_WIDTH + CELL_MARGIN)
			row = (pos[1] - ABOVE_GRID_HEIGHT) // (CELL_HEIGHT + CELL_MARGIN)
			logging.info("Click %s @ grid coordinates: %d, %d" % (pos, row, column))

	''' ======================== Viewer Drawing ======================== '''

	def _drawViewer(self):
		self._screen.fill(BLACK) # Set BG Color
		self._drawActionbar()
		self._drawGrid()
		self._drawScores()

		self._clock.tick(60) # Limit to 60 FPS
		pygame.display.flip() # update screen with new drawing

	def _drawActionbar(self):
		# Toggle Grid Button
		pygame.draw.rect(self._screen, (0,80,0), [0, 0, TOGGLE_GRID_BTN_WIDTH, ACTIONBAR_ROW_HEIGHT])
		self._screen.blit(self._font.render("Toggle Grid", True, WHITE), (10, 5))

		# Toggle Exit on Game Over Button
		pygame.draw.rect(self._screen, (0,100,0) if self._board.exit_on_game_over else (90,0,0), [TOGGLE_GRID_BTN_WIDTH, 0, TOGGLE_EXIT_BTN_WIDTH, ACTIONBAR_ROW_HEIGHT])
		self._screen.blit(self._font.render("Auto Quit", True, WHITE), (TOGGLE_GRID_BTN_WIDTH+10, 5))

	def _drawScores(self):
		pos_top = self._window_size[1]-SCORES_ROW_HEIGHT
		score_width = self._window_size[0] / len(self._scores)
		for i, score in enumerate(self._scores):
			score_color = PLAYER_COLORS[int(score['i'])]
			if (score['dead'] == True):
				score_color = GRAY_DARK
			pygame.draw.rect(self._screen, score_color, [score_width*i, pos_top, score_width, SCORES_ROW_HEIGHT])
			self._screen.blit(self._font.render(self._board.usernames[int(score['i'])], True, WHITE), (score_width*i+3, pos_top+1))
			self._screen.blit(self._font.render(str(score['total'])+" on "+str(score['tiles']), True, WHITE), (score_width*i+3, pos_top+1+self._font.get_height()))

	def _drawGrid(self):
		for row in range(self._board.rows):
			for column in range(self._board.cols):
				tile = self._board.board[row][column]
				# Determine BG Color
				color = WHITE
				color_font = WHITE
				if tile.player != None: # Player
					color = PLAYER_COLORS[tile.player]

				# Draw Rect
				pos_left = (CELL_MARGIN + CELL_WIDTH) * column + CELL_MARGIN
				pos_top = (CELL_MARGIN + CELL_HEIGHT) * row + CELL_MARGIN + ABOVE_GRID_HEIGHT
				pygame.draw.rect(self._screen, color, [pos_left, pos_top, CELL_WIDTH, CELL_HEIGHT])
	 
		
