
import logging
from game import *

logging.basicConfig(filename='chess-game.log', filemode='w', encoding='utf-8', level=logging.DEBUG)

chessGame = Game()
chessGame.run()
