
import chess
import time


pawntable = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,  5,  5,  0, -20, -40,
    -30,  5, 10, 15, 15, 10,  5, -30,
    -30,  0, 15, 20, 20, 15,  0, -30,
    -30,  5, 15, 20, 20, 15,  5, -30,
    -30,  0, 10, 15, 15, 10,  0, -30,
    -40, -20,  0,  5,  5,  0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,  5,  0,  0,  0,  0,  5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10,  0, 10, 10, 10, 10,  0, -10,
    -10,  5,  5, 10, 10,  5,  5, -10,
    -10,  0,  5, 10, 10,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [
    0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    5, 10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -10,  5,  5,  5,  5,  5,  0, -10,
    0,  0,  5,  5,  5,  5,  0, -5,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

piecetypes = [chess.PAWN, chess.KNIGHT, chess.BISHOP,
              chess.ROOK, chess.QUEEN, chess.KING]
tables = [pawntable, knightstable, bishopstable,
          rookstable, queenstable, kingstable]
piecevalues = [100, 320, 330, 500, 900]


class Minimax():
    INF = 0xffffffff

    def __init__(self):
        self.boardvalue = 0

    def init_evaluate_board(self, board):
        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))

        material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)

        pawnsq = sum([pawntable[i]
                     for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                              for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([knightstable[i]
                       for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                                   for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq = sum([bishopstable[i]
                       for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                                  for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([rookstable[i]
                     for i in board.pieces(chess.ROOK, chess.WHITE)])
        rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([queenstable[i]
                      for i in board.pieces(chess.QUEEN, chess.WHITE)])
        queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                                 for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([kingstable[i]
                     for i in board.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.KING, chess.BLACK)])

        self.boardvalue = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

    def evaluate_board(self, board):
        if board.is_checkmate():
            if board.turn:
                return -9999
            else:
                return 9999
        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0

        eval = self.boardvalue
        return eval

    def update_eval(self, board, mov, side):

        # update piecequares
        movingpiece = board.piece_type_at(mov.from_square)
        if side:
            self.boardvalue -= tables[movingpiece - 1][mov.from_square]
            # update castling
            if (mov.from_square == chess.E1) and (mov.to_square == chess.G1):
                self.boardvalue -= rookstable[chess.H1]
                self.boardvalue += rookstable[chess.F1]
            elif (mov.from_square == chess.E1) and (mov.to_square == chess.C1):
                self.boardvalue -= rookstable[chess.A1]
                self.boardvalue += rookstable[chess.D1]
        else:
            self.boardvalue += tables[movingpiece - 1][mov.from_square]
            # update castling
            if (mov.from_square == chess.E8) and (mov.to_square == chess.G8):
                self.boardvalue += rookstable[chess.H8]
                self.boardvalue -= rookstable[chess.F8]
            elif (mov.from_square == chess.E8) and (mov.to_square == chess.C8):
                self.boardvalue += rookstable[chess.A8]
                self.boardvalue -= rookstable[chess.D8]

        if side:
            self.boardvalue += tables[movingpiece - 1][mov.to_square]
        else:
            self.boardvalue -= tables[movingpiece - 1][mov.to_square]

        # update material
        if mov.drop != None:
            if side:
                self.boardvalue += piecevalues[mov.drop-1]
            else:
                self.boardvalue -= piecevalues[mov.drop-1]

        # update promotion
        if mov.promotion != None:
            if side:
                self.boardvalue += piecevalues[mov.promotion-1] - piecevalues[movingpiece-1]
                self.boardvalue -= tables[movingpiece - 1][mov.to_square] \
                    + tables[mov.promotion - 1][mov.to_square]
            else:
                self.boardvalue -= piecevalues[mov.promotion-1] + piecevalues[movingpiece-1]
                self.boardvalue += tables[movingpiece - 1][mov.to_square] \
                    - tables[mov.promotion - 1][mov.to_square]

        return mov

    def make_move(self, mov, board):
        self.update_eval(board, mov, board.turn)
        board.push(mov)

        return mov

    def unmake_move(self, board):
        mov = board.pop()
        self.update_eval(board, mov, not board.turn)

        return mov

    def quiesce(self, board, alpha, beta):
        stand_pat = self.evaluate_board(board)
        if (stand_pat >= beta):
            return beta
        if (alpha < stand_pat):
            alpha = stand_pat

        for move in board.legal_moves:
            if board.is_capture(move):
                self.make_move(move, board)
                score = -self.quiesce(board, -beta, -alpha)
                self.unmake_move(board)
                if (score >= beta):
                    return beta
                if (score > alpha):
                    alpha = score
        return alpha

    def alphabeta(self, board, alpha, beta, depthleft):
        bestscore = -9999
        if (depthleft == 0):
            return self.quiesce(board, alpha, beta)
        for move in board.legal_moves:
            self.make_move(move, board)
            score = -self.alphabeta(board, -beta, -alpha, depthleft - 1)
            self.unmake_move(board)
            if (score >= beta):
                time.sleep(1/10000)
                return score
            if (score > bestscore):
                bestscore = score
            if (score > alpha):
                alpha = score
        return bestscore

    def selectmove(self, board, depth) -> chess.Move:
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            self.make_move(move, board)
            boardValue = -self.alphabeta(board, -beta, -alpha, depth-1)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if (boardValue > alpha):
                alpha = boardValue
            self.unmake_move(board)
        return bestMove

# def eval(self, board: chess.Board):
    #     scoreWhite = 0
    #     scoreBlack = 0
    #     for i in range(0, 8):
    #         for j in range(0, 8):
    #             squareIJ = chess.square(i, j)
    #             posicao = 8*i+j
    #             pieceIJ = board.piece_at(squareIJ)
    #             if str(pieceIJ) == "P":
    #                 scoreWhite += (100 + pawntable[posicao])
    #             if str(pieceIJ) == "N":
    #                 scoreWhite += (310 + knightstable[posicao])
    #             if str(pieceIJ) == "B":
    #                 scoreWhite += (320 + bishopstable[posicao])
    #             if str(pieceIJ) == "R":
    #                 scoreWhite += (500 + rookstable[posicao])
    #             if str(pieceIJ) == "Q":
    #                 scoreWhite += (900 + queenstable[posicao])
    #             if str(pieceIJ) == "p":
    #                 scoreBlack += (100 + pawntable[posicao])
    #             if str(pieceIJ) == "n":
    #                 scoreBlack += (310 + knightstable[posicao])
    #             if str(pieceIJ) == "b":
    #                 scoreBlack += (320 + bishopstable[posicao])
    #             if str(pieceIJ) == "r":
    #                 scoreBlack += (500 + rookstable[posicao])
    #             if str(pieceIJ) == "q":
    #                 scoreBlack += (900 + queenstable[posicao])

    #     valor = scoreWhite - scoreBlack
    #     return valor

    # def quiesce(self, board, alpha, beta):
    #     stand_pat = self.eval(board)
    #     if (stand_pat >= beta):
    #         return beta
    #     if (alpha < stand_pat):
    #         alpha = stand_pat

    #     for move in board.legal_moves:
    #         if board.is_capture(move):
    #             board.push(move)
    #             score = -self.quiesce(board, -beta, -alpha)
    #             board.pop()
    #             if (score >= beta):
    #                 return beta
    #             if (score > alpha):
    #                 alpha = score
    #     return alpha

    # def search(self, board: chess.Board, depth: int, a: int, b: int, maxm: bool):
    #     if board.is_checkmate():
    #         if board.turn == chess.WHITE:
    #             return -10000
    #         else:
    #             return 10000

    #     if board.is_stalemate() or board.is_insufficient_material():
    #         return 0

    #     if depth == 0:
    #         return self.quiesce(board, a, b)

    #     # time.sleep(1/10000)
    #     depth -= 1
    #     legalMove = board.legal_moves
    #     if maxm:
    #         bestScore = -self.INF
    #         for move in legalMove:
    #             board.push(move)
    #             bestScore = max(bestScore, self.search(
    #                 board, depth, a, b, not maxm))
    #             board.pop()
    #             a = max(a, bestScore)
    #             if a >= b:
    #                 # time.sleep(1/10000)
    #                 return bestScore

    #         return bestScore
    #     else:
    #         bestScore = self.INF
    #         for move in legalMove:
    #             board.push(move)
    #             bestScore = min(bestScore, self.search(
    #                 board, depth, a, b, not maxm))
    #             board.pop()
    #             b = min(a, bestScore)
    #             if b <= a:
    #                 time.sleep(1/10000)
    #                 return bestScore

    #         return bestScore

    # def nextMove(self, depth: int, board: chess.Board, maxm: bool = True):
    #     bestMove = None
    #     bestScore = -self.INF if maxm else self.INF

    #     for move in board.legal_moves:
    #         board.push(move)
    #         score = self.search(board, depth - 1, -
    #                             self.INF, self.INF, not maxm)
    #         board.pop()
    #         if maxm:
    #             if score > bestScore:
    #                 bestScore = score
    #                 bestMove = move
    #         else:
    #             # score = score*-1
    #             if score < bestScore:
    #                 bestScore = score
    #                 bestMove = move

    #     return (bestMove, bestScore)

