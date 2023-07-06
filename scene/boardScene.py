
import asyncio
import chess
import pyglet
import threading
from minimax import *
from scene.board import *
from scene.pieces import *
from scene.scene import *
from utility import pyglet

class BoardScene(Scene):
    def __init__(self, parentWnd: pyglet.window.Window):
        super().__init__(parentWnd=parentWnd)

        self.__boardImpl = chess.Board()

        self.__awaitingAgent = False
        self.__gameStarted = False
        self.__hoverSquare = None
        self.__lockBoardFeed = True
        self.__lockInput = True
        self.__selectedSquare = None
        self.__requestedProm = False
        
        self.__doUpdateHover = False
        self.__doUpdateMoves = False
        self.__doUpdatePieces = False
        self.__doUpdateSelected = False
        self.__doUpdateTurn = False

        self.__board = Board()
        self.addElement(self.__board, Scene.BACKGROUND)

        self.registerGroup('check')
        self.registerGroup('selected')
        self.registerGroup('hover')
        self.registerGroup('moves')
        self.registerGroup('capture')
        self.registerGroup('castling')
        self.registerGroup('pieces')
        self.registerGroup('ui')

        self.__checkHighlight = SquareHighlighter('check')
        self.addElement(self.__checkHighlight, 'check')
        self.__hoverHighlight = SquareHighlighter('hover')
        self.addElement(self.__hoverHighlight, 'hover')
        self.__selectedHighlight = SquareHighlighter('selected')
        self.addElement(self.__selectedHighlight, 'selected')
        self.__turnHighlight = SquareHighlighter('turn')
        self.addElement(self.__turnHighlight, 'ui')

        w = WKing()
        w.sprite.x = TURN_X0
        w.sprite.y = TURN_Y0
        self.addElement(w, 'ui')
        b = BKing()
        b.sprite.x = TURN_X0 + 100
        b.sprite.y = TURN_Y0
        self.addElement(b, 'ui')
        self.__wTimer = Timer(TURN_X0, TURN_Y0 + PIECES_DIM, PIECES_DIM, 36, self.__timerEnded)
        self.addElement(self.__wTimer, 'ui')
        self.__bTimer = Timer(TURN_X0 + 100, TURN_Y0 + PIECES_DIM, PIECES_DIM, 36, self.__timerEnded)
        self.addElement(self.__bTimer, 'ui')

        self.__ng = Button("Jogar contra IA", self.__newGame, UI_X0, UI_Y0 + BOARD_DIM - 36, 176, 36)
        self.addElement(self.__ng, 'ui')
        self.__gu = Button("Desistir", self.__giveUp, UI_X0 + 76, UI_Y0, 100, 36)
        self.__gu.disabled = True
        self.addElement(self.__gu, 'ui')

        # self.__mvlist = MoveList(UI_X0, UI_Y0 + 38, 176, 306)
        # self.addElement(self.__mvlist, 'ui')

        def initArx(type, group, r):
            arr = []
            for _ in range(r):
                e = SquareHighlighter(type)
                self.addElement(e, group)
                arr.append(e)
            
            return arr

        self.__capturesHighlight = initArx('capture', 'capture', 8)
        self.__castlingHighlight = initArx('castling', 'castling', 2)
        self.__movesHighlight = initArx('moves', 'moves', 27)

        self.__piecesSprites = {
            'k': [BKing()],
            'q': [BQueen() for _ in range(9)],
            'b': [BBishop() for _ in range(9)],
            'n': [BKnight() for _ in range(10)],
            'r': [BRook() for _ in range(10)],
            'p': [BPawn() for _ in range(8)],
            'K': [WKing()],
            'Q': [WQueen() for _ in range(9)],
            'B': [WBishop() for _ in range(9)],
            'N': [WKnight() for _ in range(10)],
            'R': [WRook() for _ in range(10)],
            'P': [WPawn() for _ in range(8)],
        }
        self.__drops = {}
        for key in ['k', 'q', 'b', 'n', 'r', 'p', 'K', 'Q', 'B', 'N', 'R', 'P']:
            for e in self.__piecesSprites[key]:
                self.addElement(e, 'pieces')
            self.__drops[key] = []

        self.__glass = Glass()
        self.addElement(self.__glass, 'ui')
        self.__promotion = PromotionGlass()
        self.addElement(self.__promotion, 'ui')
        self.__promotion.visible = False

        def initCoroLoop(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()
        self.__coroLoop = asyncio.new_event_loop()
        self.__worker = threading.Thread(target=initCoroLoop, args=(self.__coroLoop,))
        self.__minimaxCall = Minimax()
        self.__minimaxCall.init_evaluate_board(self.__boardImpl)

        self.__glass.update("")
        self.__initTimers()
        self.__worker.start()
        self.__doUpdate()

    def __canPromote(self, square):
        return any(e.promotion is not None for e in self.__boardImpl.generate_legal_moves(1 << chess.Bitboard(square)))

    def __doUpdate(self):
        self.__doUpdateHover = True
        self.__doUpdateMoves = True
        self.__doUpdatePieces = True
        self.__doUpdateSelected = True
        self.__doUpdateTurn = True
        self.update()

    def __evalMove(self, to_square):
        if self.__selectedSquare is not None:
            promotion = None
            if self.__canPromote(self.__selectedSquare):
                self.__to_square = to_square
                self.__requestPromotion()
                return True
            
            move = chess.Move(self.__selectedSquare, to_square, promotion)
            if self.__isLegalMove(move):
                self.__selectedSquare = None
                self.__makeMove(move)
                self.__minimaxMove()

                return True

        return False

    def __gameOver(self):
        self.__glass.update(f"Fim de Jogo. " + ("Você ganhou!" if self.__boardImpl.turn == chess.WHITE else "Você perdeu!"))
        self.__glass.visible = True
        self.__reset()

    def __getLegalCaptures(self, square):
        return [*self.__boardImpl.generate_legal_captures(1 << chess.Bitboard(square))]

    def __getCastlingMoves(self, square):
        return [*self.__boardImpl.generate_castling_moves(1 << chess.Bitboard(square))]

    def __getLegalMoves(self, square):
        return [*self.__boardImpl.generate_legal_moves(1 << chess.Bitboard(square))]

    def __giveUp(self):
        if self.__gameStarted:
            self.__glass.update("Fim de Jogo!")
            self.__glass.visible = True
            self.__reset()

    def __initTimers(self):
        def updt(_):
            self.__wTimer.update()
            self.__bTimer.update()

        pyglet.clock.schedule_interval(updt, 1/60)
        pyglet.clock.schedule_interval(updt, 1/60)

    def __isGameOver(self):
        return self.__boardImpl.is_game_over() or self.__boardImpl.is_insufficient_material() or self.__boardImpl.is_variant_end()

    def __isLegalMove(self, move):
        return self.__boardImpl.is_legal(move)

    def __makeMove(self, move):
        self.__boardImpl.push(move)
        if not self.__gameStarted:
            self.__gameStarted = True
            self.__gu.disabled = False
        # self.__mvlist.append(move + ' ')
        self.__doUpdate()

    def __makePromotion(self, move):
        self.__boardImpl.push(move)
        self.__promotion.visible = False
        self.__lockBoardFeed = False
        self.__requestedProm = False
        self.__doUpdate()
        self.__minimaxMove()

    @staticmethod
    async def __minimax(board, callback):
        move = Minimax().selectmove(board.copy(), 4)
        logging.debug(move)
        callback(move)

    def __minimaxMove(self):
        if not self.__awaitingAgent:
            def makeMinimaxMove(move):
                self.__makeMove(move)
                self.__awaitingAgent = False
                self.__lockInput = False
            self.__awaitingAgent = True
            asyncio.run_coroutine_threadsafe(self.__minimax(self.__boardImpl, makeMinimaxMove), self.__coroLoop)

    def __newGame(self):
        # fazer opção com o agente RND
        self.__awaitingAgent = False
        self.__gameStarted = False
        self.__gu.disabled = True
        self.__hoverSquare = None
        self.__lockBoardFeed = False
        self.__lockInput = True
        self.__selectedSquare = None
        self.__glass.visible = False
        self.__resetBoard()
        self.__resetTimers()
        self.__doUpdate()
        self.__minimaxMove()

    def __requestPromotion(self):
        self.__lockBoardFeed = True
        self.__requestedProm = True
        self.__promotion.visible = True
    
    def __reset(self):
        self.__lockBoardFeed = True
        self.__lockInput = True
        self.__gameStarted = False
        self.__stopTimers()

    def __resetBoard(self):
        self.__boardImpl.clear_stack()
        self.__boardImpl.reset()

    def __resetTimers(self):
        self.__wTimer.reset()
        self.__bTimer.reset()
    
    def __selectSquare(self, square):
        piece = self.__boardImpl.piece_at(square)
        if piece and piece.color == self.__boardImpl.turn:
            self.__selectedSquare = square
        else:
            self.__selectedSquare = None

    def __stopTimers(self):
        self.__wTimer.stop()
        self.__bTimer.stop()

    def __timerEnded(self):
        self.__glass.update(f"Fim de Jogo. " + ("Você ganhou!" if self.__boardImpl.turn == chess.WHITE else "Você perdeu!"))
        self.__glass.visible = True
        self.__reset()

    def __toggleTimer(self):
        # print(self.__boardImpl.turn)
        if self.__boardImpl.turn == chess.WHITE:
            self.__wTimer.start()
            self.__bTimer.pause()
        else:
            self.__wTimer.pause()
            self.__bTimer.start()

    def __updateCheck(self):
        if self.__boardImpl.is_check():
            square = self.__boardImpl.king(self.__boardImpl.turn)
            if square is not None:
                xy = self.__board.square2xy(square)
                self.__checkHighlight.shape.x = xy[0]
                self.__checkHighlight.shape.y = xy[1]
                self.__checkHighlight.shape.visible = True
        else:
            self.__checkHighlight.shape.visible = False

    def __updateHover(self):
        if self.__hoverSquare is not None:
            pos = self.__board.square2xy(self.__hoverSquare)
            self.__hoverHighlight.shape.x = pos[0]
            self.__hoverHighlight.shape.y = pos[1]
            self.__hoverHighlight.shape.visible = True
        else:
            self.__hoverHighlight.shape.visible = False

    def __updateMoves(self):
        def rangeSelc(range, collection):
            for i in collection:
                if (len(range) == 0):
                    i.shape.visible = False
                    continue

                xy = self.__board.square2xy(range[-1].to_square)
                i.shape.x = xy[0]
                i.shape.y = xy[1]
                i.shape.visible = True
                range.pop()

        def rangeUnselc(collection):
            for i in collection:
                i.shape.visible = False

        if self.__selectedSquare is not None:
            rangeSelc(self.__getLegalCaptures(self.__selectedSquare), self.__capturesHighlight)
            rangeSelc(self.__getCastlingMoves(self.__selectedSquare), self.__castlingHighlight)
            rangeSelc(self.__getLegalMoves(self.__selectedSquare), self.__movesHighlight)
        else:
            rangeUnselc(self.__capturesHighlight)
            rangeUnselc(self.__castlingHighlight)
            rangeUnselc(self.__movesHighlight)

    def __updatePieces(self):
        pieces = self.__boardImpl.piece_map()
        sprites = {key: self.__piecesSprites[key].copy() for key in self.__piecesSprites}
        for key in pieces:
            piece = pieces[key]
            xy = self.__board.square2xy(key)
            collection = sprites[piece.symbol()]
            collection[-1].sprite.x = xy[0]
            collection[-1].sprite.y = xy[1]
            collection[-1].sprite.visible = True
            collection.pop()

        self.__drops = sprites
        for key in self.__drops:
            for e in self.__drops[key]:
                e.sprite.visible = False

    def __updateSelected(self):
        if self.__selectedSquare is not None:
            pos = self.__board.square2xy(self.__selectedSquare)
            self.__selectedHighlight.shape.x = pos[0]
            self.__selectedHighlight.shape.y = pos[1]
            self.__selectedHighlight.shape.visible = True
        else:
            self.__selectedHighlight.shape.visible = False

    def __updateTurn(self):
        if self.__boardImpl.turn == chess.WHITE:
            self.__turnHighlight.shape.x = TURN_X0
            self.__turnHighlight.shape.y = TURN_Y0
        else:
            self.__turnHighlight.shape.x = TURN_X0 + 100
            self.__turnHighlight.shape.y = TURN_Y0
        self.__turnHighlight.shape.visible = True

    def on_activate(self):
        pass
    
    def on_deactivate(self):
        pass

    def on_close(self):
        async def stop():
            pass
        self.__coroLoop.stop()
        asyncio.run_coroutine_threadsafe(stop(), self.__coroLoop)
        self.__worker.join()
    
    def on_draw(self):
        self.batch.draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.__ng.hovering(x, y)
        self.__gu.hovering(x, y)

        if self.__lockBoardFeed:
            return
        
        if self.__board.inbounds(x, y):
            self.__hoverSquare = self.__board.xy2square(x, y)
            self.__doUpdateHover = True
        else:
            self.__hoverSquare = None
            self.__doUpdateHover = True

        self.update()
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.__ng.pressed(x, y)
        self.__gu.pressed(x, y)

        if self.__lockInput:
            return
        
        if self.__requestedProm:
            prom = self.__promotion.promotion(x, y)
            if self.__selectedSquare is None:
                raise RuntimeError("invalid promotion")
            if prom is not None:
                self.__makePromotion(chess.Move(self.__selectedSquare, self.__to_square, prom))
            self.__selectedSquare = None
            return

        square = self.__board.xy2square(x, y) if self.__board.inbounds(x, y) else None

        if button & pyglet.window.event.mouse.LEFT:
            if square is not None:
                if self.__selectedSquare is not None:
                    if not self.__evalMove(square):
                        self.__selectSquare(square)
                        self.__doUpdateSelected = True
                        self.__doUpdateMoves = True
                else:
                    self.__selectSquare(square)
                    self.__doUpdateSelected = True
                    self.__doUpdateMoves = True
        
        if button & pyglet.window.event.mouse.RIGHT:
            self.__selectedSquare = None
        
        self.update()

    def on_mouse_release(self, x, y, button, modifiers):
        self.__ng.released(x, y)
        self.__gu.released(x, y)

    def update(self):
        if self.__doUpdateHover:
            self.__updateHover()
            self.__doUpdateHover = False
        if self.__doUpdateMoves:
            self.__updateMoves()
            self.__doUpdateMoves = False
        if self.__doUpdatePieces:
            self.__updateCheck()
            self.__updatePieces()
            self.__doUpdatePieces = False
        if self.__doUpdateSelected:
            self.__updateSelected()
            self.__doUpdateSelected = False
        if self.__doUpdateTurn:
            self.__updateTurn()
            self.__doUpdateTurn = False
        
        if self.__gameStarted:
            self.__toggleTimer()
        
        if self.__isGameOver():
            self.__gameOver()
