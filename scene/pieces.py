
from app import *
from scene.scene import *

class Piece(SceneElement):
    def __init__(self, texture):
        super().__init__(createSprite(texture))

    @property
    def sprite(self):
        return super().sprite

    def delete(self):
        return super().delete()

    def batchToScene(self, batch, group):
        return super().batchToScene(batch, group)

class BKing(Piece):
    def __init__(self):
        super().__init__(BKING_TEXTURE)

class BQueen(Piece):
    def __init__(self):
        super().__init__(BQUEEN_TEXTURE)

class BBishop(Piece):
    def __init__(self):
        super().__init__(BBISHOP_TEXTURE)

class BKnight(Piece):
    def __init__(self):
        super().__init__(BKNIGHT_TEXTURE)

class BRook(Piece):
    def __init__(self):
        super().__init__(BROOK_TEXTURE)

class BPawn(Piece):
    def __init__(self):
        super().__init__(BPAWN_TEXTURE)

class WKing(Piece):
    def __init__(self):
        super().__init__(WKING_TEXTURE)

class WQueen(Piece):
    def __init__(self):
        super().__init__(WQUEEN_TEXTURE)

class WBishop(Piece):
    def __init__(self):
        super().__init__(WBISHOP_TEXTURE)

class WKnight(Piece):
    def __init__(self):
        super().__init__(WKNIGHT_TEXTURE)

class WRook(Piece):
    def __init__(self):
        super().__init__(WROOK_TEXTURE)

class WPawn(Piece):
    def __init__(self):
        super().__init__(WPAWN_TEXTURE)
