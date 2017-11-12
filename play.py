'''
	@ Harris Christiansen (Harris@HarrisChristiansen.com)
	Four Corners - https://github.com/harrischristiansen/four-corners
	Play: Start a game
'''

import logging

from fcgame import FourCornersGame

# Show all logging
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
	game = FourCornersGame()
	game.mainViewerProcess()