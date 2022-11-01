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

class Game():
    """
    Creates gomoku game.
    """
    def __init__(self, side = 15):
        # 1's represent X's, -1's O's
        self.state = np.full([side, side], 0, dtype=np.short)
        self.side = side
        self.activePlayer = 1
        
    def getCurrentPosition(self):
        """
        Returns current game position as a 2D numpy array.
        
        0 means empty tile
        1 means X
        -1 means O
        """
        return self.state
        
    def getCurrentPositionForAI(self):
        """
        Returns current game position as a 2D numpy array.
        
        0 means empty tile
        1 means tile controlled by the active player
        -1 means tile controlled by the inactive player
        """
        return self.state * self.activePlayer
        
    def getLegalMoves(self):
        legalMoves = []
        for i, row in enumerate(range(self.side)):
            for j, tile in enumerate(row):
                if tile == 0:
                    legalMoves.append([i, j])
    
    def playMove(self, x, y):
        if self.state[x][y] != 0:
            raise InvalidMove("This tile's already full!")
        self.state[x][y] = self.activePlayer
        self.activePlayer *= -1
    
    def outcome(self):
        """
        returns 0 if noone has won yet
        returns 1 if X has won
        returns -1 if O has won
        
        If multiple winning combinations are on the board, this function will not work properly.
        """
        for shape in WINNING_SHAPES:
            shapeHight = shape.shape[0]
            shapeWidth = shape.shape[1]
            
            for i in range(self.side - shapeHight + 1):
                for j in range(self.side - shapeWidth + 1):
                    score = np.sum(np.sum(self.state[i : i + shapeHight, j : j + shapeWidth] * shape))
                    if score == 5 or score == -5:
                        return score // 5
        return 0                    
    
    def outcomeForAI(self):
        """
        returns 0 if none has won yet
        returns 1 if the active player has won
        returns -1 if the inactive player has won
        
        If multiple winning combinations are on the board, this function will not work properly.
        """
        return self.outcome() * self.activePlayer()
                  
if __name__ == "__main__":
    game = Game(side = 5)
    while game.outcome() == 0:
        print(game.state)
        try:
            x = int(input("enter x: "))
            y = int(input("enter y: "))
            game.playMove(x, y)
        except (ValueError, IndexError) as e:
            print(e)
            print("Move again!")
        
    print("Game over!")
    print(game.outcome())
        
                        
                    
    