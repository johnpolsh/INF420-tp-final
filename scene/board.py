
import chess
import pyglet
import time
from app import *
from scene.scene import *
from utility import *

class Board(SceneElement):
    def __init__(self):
        super().__init__(createSprite(BOARD_TEXTURE))

    @property
    def sprite(self):
        return super().sprite

    def batchToScene(self, batch, group):
        return super().batchToScene(batch, group)

    def delete(self):
        return super().delete()

    def inbounds(self, x: int, y: int):
        return x >= BOARD_X0 and x < BOARD_X0 + BOARD_DIM and y >= BOARD_Y0 and y < BOARD_Y0 + BOARD_DIM

    def xy2square(self, x: int, y: int):
        x -= BOARD_X0
        y = BOARD_DIM + BOARD_Y0 - y

        return x // PIECES_DIM + (y // PIECES_DIM) * 8
    
    def square2xy(self, square: int):
        return (BOARD_X0 + (square % 8) * PIECES_DIM, BOARD_DIM - (BOARD_Y0 + (square // 8) * PIECES_DIM))

class SquareHighlighter(SceneElement):
    def __init__(self, type):
        super().__init__()

        color = (255, 255, 255)
        if type == 'moves':
            self.shape = pyglet.shapes.Circle(0, 0, PIECES_DIM // 5, color=(77, 147, 187, 63))
            self.shape.anchor_position = (-PIECES_DIM // 2, -PIECES_DIM // 2)
        elif type == 'turn':
            self.shape = pyglet.shapes.BorderedRectangle(0, 0, width=PIECES_DIM - 8, height=PIECES_DIM - 8, color=(20, 57, 81), border=2, border_color=(135, 161, 180))
            self.shape.anchor_position = (-4, -4)
        elif type == 'check':
            self.shape = pyglet.shapes.BorderedRectangle(0, 0, width=PIECES_DIM, height=PIECES_DIM, color=(187, 77, 77), border=2, border_color=(255, 200, 5))
        else:
            if type == 'capture':
                color = (187, 77, 140)
            if type == 'castling':
                color = (140, 187, 140)
            if type == 'selected':
                color = (77, 187, 140, 100)
            if type == 'hover':
                color = (77, 147, 187)

            self.shape = pyglet.shapes.BorderedRectangle(0, 0, width=PIECES_DIM, height=PIECES_DIM, color=color, border=2, border_color=(135, 161, 180))

        self.shape.visible = False
    
    @property
    def sprite(self):
        raise RuntimeError("SquareHighlighter does not have an accessible sprite")

    def delete(self):
        self.shape.delete()

    def batchToScene(self, batch, group):
        self.shape.batch = batch
        self.shape.group = group

class Button(SceneElement):
    def __init__(self, text, callback, x, y, width, height):
        super().__init__()

        self.callback = callback
        self.__disabled = False
        self.label = pyglet.text.Label(text, x=x, y=y + height // 2, anchor_y='center', width=width, height=height, font_size=18, color=(135, 161, 180, 255), align='center')
        self.shape = pyglet.shapes.BorderedRectangle(x, y, width=width, height=height, color=(20, 57, 84), border=2, border_color=(20, 57, 84))

    @property
    def sprite(self):
        raise RuntimeError("SquareHighlighter does not have an accessible sprite")

    def delete(self):
        self.shape.delete()
        self.label.delete()

    def batchToScene(self, batch, group):
        self.shape.batch = batch
        self.shape.group = group
        self.label.batch = batch
        self.label.group = group

    @property
    def disabled(self):
        return self.__disabled
    
    @disabled.setter
    def disabled(self, val):
        if self.__disabled != val:
            self.__disabled = val
            if val:
                self.shape.color = (12, 32, 47)
                self.shape.border_color = (12, 32, 47)
                self.label.color = (57, 86, 106, 255)
            else:
                self.shape.color = (20, 57, 84)
                self.shape.border_color = (20, 57, 84)
                self.label.color = (135, 161, 180, 255)

    def hovering(self, x, y):
        if self.__disabled:
            return

        self.shape.color = (20, 57, 84)
        if self.inbounds(x, y):
            self.shape.border_color = (135, 161, 180)
        else:
            self.shape.border_color = (20, 57, 84)

    def inbounds(self, x, y):
        if not self.shape.width or not self.shape.height:
            return
        
        return x >= self.shape.x and x < self.shape.x + self.shape.width and y >= self.shape.y and y < self.shape.y + self.shape.height

    def pressed(self, x, y):
        if self.__disabled:
            return
        
        if self.inbounds(x, y):
            self.shape.color = (12, 32, 47)
            self.callback()
    
    def released(self, x, y):
        if self.__disabled:
            return
        
        if self.inbounds(x, y):
            self.shape.color = (20, 57, 84)

    @property
    def visible(self):
        return self.label.visible and self.shape.visible

    @visible.setter
    def visible(self, val):
        self.label.visible = val
        self.shape.visible = val

class Timer(SceneElement):
    def __init__(self, x, y, width, height, callback, span=720):
        super().__init__()

        self.__callback = callback
        self.__past = 0
        self.__span = span
        self.__start = 0
        self.__running = False
        self.label = pyglet.text.Label(self.__getTime(self.__span), x=x, y=y + height // 2, anchor_y='center', font_size=18, color=(135, 161, 180, 255), width=width, height=height, align='center')
    
    def __getTime(self, sec):
        clc = divmod(sec, 60)

        return "%02d:%02d" % clc

    @property
    def sprite(self):
        raise RuntimeError("Timer does not have an accessible sprite")

    def delete(self):
        self.label.delete()

    def batchToScene(self, batch, group):
        self.label.batch = batch
        self.label.group = group

    def pause(self):
        if self.__running:
            self.__running = False
            self.__past += time.time() - self.__start
            
    def reset(self):
        self.label.text = self.__getTime(self.__span)
        self.stop()

    def start(self):
        if not self.__running:
            self.__start = time.time()
            self.__running = True

    def stop(self):
        self.__running = False
        self.__past = 0
        self.__start = 0

    def update(self):
        if self.__running:
            remn = self.__span - (time.time() - self.__start + self.__past)
            if remn > .0:
                self.label.text = self.__getTime(remn)
            else:
                self.__running = False
                self.__past = self.__span
                self.__callback()

# BUG: o código gera lança erro inespera no momento que o texto na label é alterado
# Traceback (most recent call last):
#  File "C:\Python310\lib\site-packages\pyglet\graphics\vertexdomain.py", line 110, in __del__
#    for attribute in self.attributes:
# AttributeError: 'IndexedVertexDomain' object has no attribute 'attributes'
class MoveList(SceneElement):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.label = pyglet.text.document.UnformattedDocument("movimentos: ")
        self.label.set_style(0, 1, dict(font_size=12, color=(135, 161, 180, 255)))
        self.text = pyglet.text.layout.ScrollableTextLayout(self.label, width, height, multiline=True)
        self.text.x = x
        self.text.y = y
    
    @property
    def sprite(self):
        raise RuntimeError("Timer does not have an accessible sprite")

    def append(self, msg):
        self.label.insert_text(-1, msg)

    def batchToScene(self, batch, group):
        self.text.batch = batch
        self.text.group = group

    def delete(self):
        self.text.delete()

    def update(self, msg = ''):
        self.label.text = msg

class Glass(SceneElement):
    def __init__(self):
        super().__init__()

        self.shape = pyglet.shapes.Rectangle(BOARD_X0, BOARD_Y0, BOARD_DIM, BOARD_DIM, color=(0, 0, 0, 170))
        self.label = pyglet.text.Label(font_size=36, x=BOARD_X0 + BOARD_DIM // 2, y=BOARD_Y0 + BOARD_DIM // 2, anchor_x='center', anchor_y='center', align='center')

    @property
    def sprite(self):
        raise RuntimeError("Timer does not have an accessible sprite")

    def delete(self):
        self.shape.delete()

    def batchToScene(self, batch, group):
        self.shape.batch = batch
        self.shape.group = group
        self.label.batch = batch
        self.label.group = group

    @property
    def visible(self):
        return self.shape.visible

    @visible.setter
    def visible(self, val):
        self.label.visible = val
        self.shape.visible = val

    def update(self, msg):
        self.label.text = msg

class PromotionGlass(SceneElement):
    def __init__(self):
        super().__init__()

        self.shape = pyglet.shapes.Rectangle(BOARD_X0, BOARD_Y0, BOARD_DIM, BOARD_DIM, color=(0, 0, 0, 170))
        self.P_X0 = BOARD_X0 + (BOARD_DIM - 4 * PIECES_DIM) // 2
        self.P_Y0 = BOARD_Y0 + (BOARD_DIM - PIECES_DIM) // 2
        self.pieces = [
            pyglet.sprite.Sprite(WQUEEN_TEXTURE, self.P_X0, self.P_Y0),
            pyglet.sprite.Sprite(WBISHOP_TEXTURE, self.P_X0 + PIECES_DIM, self.P_Y0),
            pyglet.sprite.Sprite(WKNIGHT_TEXTURE, self.P_X0 + 2 * PIECES_DIM, self.P_Y0),
            pyglet.sprite.Sprite(WROOK_TEXTURE, self.P_X0 + 3 * PIECES_DIM, self.P_Y0)
        ]
        # self.label = pyglet.text.Label(font_size=36, x=BOARD_X0 + BOARD_DIM // 2, y=BOARD_Y0 + BOARD_DIM // 2, anchor_x='center', anchor_y='center', align='center')

    @property
    def sprite(self):
        raise RuntimeError("Timer does not have an accessible sprite")

    def delete(self):
        self.shape.delete()

    def batchToScene(self, batch, group):
        self.shape.batch = batch
        self.shape.group = group
        for p in self.pieces:
            p.batch = batch
            p.group = group

    def promotion(self, x, y):
        piece = None
        if y >= self.P_Y0 and y < self.P_Y0 + PIECES_DIM:
            if x >= self.P_X0 and x < self.P_X0 + PIECES_DIM:
                piece = chess.QUEEN
            if x >= self.P_X0 + PIECES_DIM and x < self.P_X0 + 2 * PIECES_DIM:
                piece = chess.BISHOP
            if x >= self.P_X0 + 2 * PIECES_DIM and x < self.P_X0 + 3 * PIECES_DIM:
                piece = chess.KNIGHT
            if x >= self.P_X0 + 3 * PIECES_DIM and x < self.P_X0 + 4 * PIECES_DIM:
                piece = chess.ROOK
        
        return piece

    @property
    def visible(self):
        return self.shape.visible

    @visible.setter
    def visible(self, val):
        self.shape.visible = val
        for p in self.pieces:
            p.visible = val
