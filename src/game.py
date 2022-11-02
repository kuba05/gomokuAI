import numpy as np

WINNING_SHAPES = [
    np.array(
        [
            [1, 1, 1, 1, 1]
        ]
    ),
    np.array(
        [
            [1],
            [1],
            [1],
            [1],
            [1]
        ]
    ),
    np.array(
        [
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
        ]
    ),
    np.array(
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0],
        ]
    )
]

class InvalidMove(ValueError):
    pass

class GomokuHelper():
    def getAllMoves(self, state):
        legalMoves = []
        for i, row in enumerate(state):
            for j, tile in enumerate(row):
                if tile == 0:
                    legalMoves.append([i, j])
        return legalMoves
                    
    def getStateAfterMove(self, state, move):
        newState = np.copy(state)
        newState[move[0], move[1]] = 1
        newState *= -1
        return newState
        
    def getOutcome(self, state):
        hight, width = state.shape
        
        for shape in WINNING_SHAPES:
            shapeHight = shape.shape[0]
            shapeWidth = shape.shape[1]
            
            for i in range(hight - shapeHight + 1):
                for j in range(width - shapeWidth + 1):
                    score = np.sum(np.sum(state[i : i + shapeHight, j : j + shapeWidth] * shape))
                    if score == 5 or score == -5:
                        return score // 5
        return 0
        
        
class GomokuGame():
    """
    Creates gomoku game.
    """
    def __init__(self, side = 15):
        # 1's represent X's, -1's O's
        self.state = np.full([side, side], 0, dtype=np.short)
        self.activePlayer = 1
        self.gomokuHelper = GomokuHelper()
        
    def getCurrentPosition(self):
        """
        Returns current game position as a 2D numpy array.
        
        0 means empty tile
        1 means X
        -1 means O
        """
        return self.state * self.activePlayer
        
    def getLegalMoves(self):
        self.gomokuHelper.getAllMoves(self.state)
        
    def playMove(self, x, y):
        if self.state[x, y] != 0:
            raise InvalidMove("Tile is not empty!")
        self.state = self.gomokuHelper.getStateAfterMove(self.state, (x, y))
        self.activePlayer *= -1
    
    def outcome(self):
        """
        returns 0 if noone has won yet
        returns 1 if X has won
        returns -1 if O has won
        
        If multiple winning combinations are on the board, this function will not work properly.
        """
        return self.gomokuHelper.getOutcome(self.state)
                  
if __name__ == "__main__":
    game = GomokuGame(side = 5)
    while game.outcome() == 0:
        print(game.getCurrentPosition())
        try:
            x = int(input("enter x: "))
            y = int(input("enter y: "))
            game.playMove(x, y)
        except (ValueError, IndexError) as e:
            print(e)
            print("Move again!")
        
    print("Game over!")
    print(game.outcome())
        
                        
                    
    