
import pyglet
from utility import *

WND_HEIGHT = 684
WND_WIDTH = 936

WND_TITLE = "INF 420 - Trabalho final | ChessBot"

BOARD_TEXTURE_SRC = "images/board.png"
PIECES_TEXTURE_SRC = "images/pieces.png"
PIECES_PROM_TEXTURE_SRC = "images/pieces_prom.png"

BOARD_X0 = 38
BOARD_Y0 = 38
BOARD_DIM = 608
PIECES_WIDTH = 608
PIECES_HEIGHT = 202
PIECES_DIM = 76

UI_X0 = 722
UI_Y0 = 38

TURN_X0 = UI_X0
TURN_Y0 = UI_Y0 + 376

class App():
    def __init__(self) -> None:
        self.window = pyglet.window.Window(width=WND_WIDTH, height=WND_HEIGHT, caption=WND_TITLE)
        self.fpsDisplay = pyglet.window.FPSDisplay(self.window, samples=60)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
    
    def loadTexture(self, name: str):
        return pyglet.resource.image(name)
    
    def loadFile(self, name: str):
        return open(name, 'r').read()

gameApp = App()

BOARD_TEXTURE_REAL = gameApp.loadTexture(BOARD_TEXTURE_SRC)
BOARD_TEXTURE = scaleTexture(BOARD_TEXTURE_REAL, (WND_WIDTH, WND_HEIGHT))

PIECES_TEXTURE_REAL = gameApp.loadTexture(PIECES_TEXTURE_SRC)
PIECES_PROM_TEXTURE_REAL = gameApp.loadTexture(PIECES_PROM_TEXTURE_SRC)
PIECES_TEXTURE = scaleTexture(PIECES_PROM_TEXTURE_REAL, (PIECES_WIDTH, PIECES_HEIGHT))
__piecesGrid = pyglet.image.TextureGrid(pyglet.image.ImageGrid(PIECES_TEXTURE_REAL, 2, 6))

def __scalePiece(piece):
    return scaleTexture(piece, (PIECES_DIM, PIECES_DIM))

BKING_TEXTURE = __scalePiece(__piecesGrid[0])
BQUEEN_TEXTURE = __scalePiece(__piecesGrid[1])
BBISHOP_TEXTURE = __scalePiece(__piecesGrid[2])
BKNIGHT_TEXTURE = __scalePiece(__piecesGrid[3])
BROOK_TEXTURE = __scalePiece(__piecesGrid[4])
BPAWN_TEXTURE = __scalePiece(__piecesGrid[5])
WKING_TEXTURE = __scalePiece(__piecesGrid[6])
WQUEEN_TEXTURE = __scalePiece(__piecesGrid[7])
WBISHOP_TEXTURE = __scalePiece(__piecesGrid[8])
WKNIGHT_TEXTURE = __scalePiece(__piecesGrid[9])
WROOK_TEXTURE = __scalePiece(__piecesGrid[10])
WPAWN_TEXTURE = __scalePiece(__piecesGrid[11])

# SQUARE_FRAG = gameApp.loadFile("shader/highlight.frag")
# SQUARE_VEX = gameApp.loadFile("shader/highlight.vert")
