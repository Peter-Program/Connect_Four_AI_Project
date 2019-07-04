from connectfour.agents.computer_player import RandomAgent
import random

x = 0

POS_INFINITY = 100000000
NEG_INFINITY = -100000000

# python3 -m connectfour.game --player-one HumanPlayer  --player-two StudentAgent

# python3 -m connectfour.game --player-one RandomAgent  --player-two StudentAgent --fast --no-graphics


class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 4

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """
        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            # vals.append( self.dfMiniMax(next_state, 1) )
            vals.append(self.minimaxAlpBet(next_state, 1, NEG_INFINITY, POS_INFINITY, True))

        bestMove = moves[vals.index( max(vals) )]
        # print(vals)
        global x
        x = 0
        return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states
        if depth == self.MaxDepth or board.terminal():
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])

            vals.append( self.dfMiniMax(next_state, depth + 1) )
        
        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

    # Minimax algorithm with Alpha Beta Prunining 
    def minimaxAlpBet(self, board, depth, alpha, beta, maximize):

        if depth == self.MaxDepth or board.terminal():
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []
 
        # Max value
        if maximize:
            value = NEG_INFINITY
            for move in valid_moves:
                if (depth % 2) == 1:
                    next_state = board.next_state(self.id % 2 + 1, move[1])
                else:
                    next_state = board.next_state(self.id, move[1])

                value = max(value, self.minimaxAlpBet(next_state, depth + 1, alpha, beta, False))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value
     
        # Min Value
        else:
            value = POS_INFINITY
            for move in valid_moves:
                if (depth % 2) == 1:
                    next_state = board.next_state(self.id % 2 + 1, move[1])
                else:
                    next_state = board.next_state(self.id, move[1])

                value = min(value, self.minimaxAlpBet(next_state, depth + 1, alpha, beta, True))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

    # Used to help determin if the cell we are looking at is an enemy of the
    #  passed in player
    def isEnemyPiece(self, cellValue, player):
        return (cellValue > 0 and cellValue != player)

    # Calculating points based on horizontal features
    def checkHorizontal(self, board, player):
        points = 0
        for row in reversed(range(board.height)):
            for col in (range(2, board.width - 3)):
                posStart = board.get_cell_value(row, col)
                posNextRight1 = board.get_cell_value(row, col + 1)
                posNextRight2 = board.get_cell_value(row, col + 2)
                posNextRight3 = board.get_cell_value(row, col + 3)

                if posStart == player:
                    points += 4
                    # if Piece is next to same piece with them to the right
                    if posNextRight1 == player:
                        points += 6
                        if posNextRight2 == player:
                            points += 10
                            if posNextRight3 == player:
                                return 1000
                    # If Piece is next to enemy pieces so that we can block them
                    if self.isEnemyPiece(posNextRight1, player):
                        points += 8
                        if self.isEnemyPiece(posNextRight2, player):
                            points += 50

                # If enemy piece is in a row
                if self.isEnemyPiece(posStart, player):
                    points -= 4
                    # To the right
                    if self.isEnemyPiece(posNextRight1, player):
                        points -= 6
                        if self.isEnemyPiece(posNextRight2, player):
                            points -= 10
                            # enemy will win
                            if self.isEnemyPiece(posNextRight3, player):
                                return -1000

        for row in reversed(range(board.height)):
            for col in reversed(range(2, board.width)):
                posStart = board.get_cell_value(row, col)
                posNextLeft1 = board.get_cell_value(row, col - 1)
                posNextLeft2 = board.get_cell_value(row, col - 2)
                posNextLeft3 = board.get_cell_value(row, col - 3)

                if posStart == player:
                    points += 4
                    # if Piece is next to same piece with them to the left
                    if posNextLeft1 == player:
                        points += 6
                        if posNextLeft2 == player:
                            points += 10
                            # Player will win
                            if posNextLeft3 == player:
                                return 1000
                    # If Piece is next to enemy pieces so that we can block them
                    if self.isEnemyPiece(posNextLeft1, player):
                        points += 8
                        if self.isEnemyPiece(posNextLeft2, player):
                            points += 50

                # If enemy piece is in a row
                if self.isEnemyPiece(posStart, player):
                    points -= 4
                    # To the left
                    if self.isEnemyPiece(posNextLeft1, player):
                        points -= 6
                        if self.isEnemyPiece(posNextLeft2, player):
                            points -= 10
                            if self.isEnemyPiece(posNextLeft3, player):
                                return -1000
        return points

    # Calculating points based on Vertical features
    def checkVertical(self, board, player):
        points = 0

        for row in reversed(range(board.height - (board.num_to_connect - 1), board.height)):
            for col in (range(board.width)):
                posStart = board.get_cell_value(row, col)
                posUp1 = board.get_cell_value(row - 1, col)
                posUp2 = board.get_cell_value(row - 2, col)
                posUp3 = board.get_cell_value(row - 3, col)
                # if we have 2, 3 and/or 4 in a row vertically
                if posStart == player:
                    points += 2
                    if posUp1 == player:
                        points += 8
                        if posUp2 == player:
                            points += 50
                            if posUp3 == player:
                                return 1000

                # to Block oponent for they have 3 in a row
                if ((self.isEnemyPiece(posStart, player)) and
                    (self.isEnemyPiece(posUp1, player)) and
                    (self.isEnemyPiece(posUp2, player)) and 
                    (posUp3 == player)):
                    points += 100

                # Enemy is going to win
                if ((self.isEnemyPiece(posStart, player)) and
                    (self.isEnemyPiece(posUp1, player)) and
                    (self.isEnemyPiece(posUp2, player)) and
                    (self.isEnemyPiece(posUp3, player))):
                    return -1000
        return points

    # Calculating points based on left to right diagnal
    def checkDiagonallyLowerLeftToRight(self, board, player):
        points = 0
        for row in reversed(range(board.height - 2, board.height)):
            for col in (range(board.width - 3)):
                posStart = board.get_cell_value(row, col)
                posUp1 = board.get_cell_value(row - 1, col + 1)
                posUp2 = board.get_cell_value(row - 2, col + 2)
                posUp3 = board.get_cell_value(row - 3, col + 3)

                if (posStart == player):
                    if posUp1 == player:
                        points += 4
                        if posUp2 == player:
                            points += 6
                            if posUp3 == player:
                                return 1000

                # if enemy has valuable positions
                if self.isEnemyPiece(posStart, player):
                    points -= 4
                    if self.isEnemyPiece(posUp1, player):
                        points -= 6
                        if self.isEnemyPiece(posUp2, player):
                            points -= 20
                            if self.isEnemyPiece(posUp3, player):
                                return -1000
        return points

    # Calculating points based on Right to left diagnal
    def checkDiagonallyTopRightToLeft(self, board, player):
        points = 0
        for row in (range(board.height, board.height - 2)):
            for col in (reversed(range(3, board.width))):
                posStart = board.get_cell_value(row, col)
                posUp1 = board.get_cell_value(row + 1, col - 1)
                posUp2 = board.get_cell_value(row + 2, col - 2)
                posUp3 = board.get_cell_value(row + 3, col - 3)
                if (posStart == player):
                    if posUp1 == player:
                        points += 4
                        if posUp2 == player:
                            points += 6
                            if posUp3 == player:
                                return 1000
                # if enemy has valuable positions
                if self.isEnemyPiece(posStart, player):
                    points -= 4
                    if self.isEnemyPiece(posUp1, player):
                        points -= 6
                        if self.isEnemyPiece(posUp2, player):
                            points -= 20
                            if self.isEnemyPiece(posUp3, player):
                                return -1000
        return points

    # Returns value based on board state
    def checkGood(self, board, player):
        # self.printingState(board)
        goodValue = 0

        goodValue += self.checkHorizontal(board, player)
        goodValue += self.checkVertical(board, player)
        goodValue += self.checkDiagonallyLowerLeftToRight(board, player)
        goodValue += self.checkDiagonallyTopRightToLeft(board, player)

        return goodValue
    
    # prints the board state
    def printingState(self, board):
        blankRowCounter = 0
        global x
        x += 1
        print(x)
        for row in reversed(range(board.height)):
            if blankRowCounter >= board.width:
                # Stop, for the rest is blank
                break
            else:
                blankRowCounter = 0
            for col in range(board.width):
                cellValue = board.get_cell_value(row, col)
                if cellValue == 0:
                    blankRowCounter += 1
                print(cellValue, end=" ")
            print("counter " + str(blankRowCounter))
        print("--------------------------- \n")

    def evaluateBoardState(self, board):

        return self.checkGood(board, self.id)/1000
        

