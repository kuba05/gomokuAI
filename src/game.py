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


class Game():
    def __init__(self, side = 15):
        self.state = np.full([side, side], 0, dtype=np.short)
        self.side = side
        self.activePlayer = 1
        
    def getCurrentPosition(self):
        return self.state
        
    def getCurrentPositionForAI(self):
        return self.state * self.activePlayer
        
    def getLegalMoves(self):
        legalMoves = []
        for i, row in enumerate(range(self.side)):
            for j, tile in enumerate(row):
                if tile == 0:
                    legalMoves.append([i, j])
    
    def playMove(self, x, y):
        self.state[x][y] = 1
    
    def outcome(self):
        for shape in WINNING_SHAPES:
            shapeHight = shape.shape[0]
            shapeWidth = shape.shape[1]
            
            for i in range(self.side - shapeHight + 1):
                for j in range(self.side - shapeWidth + 1):
                    score = np.sum(np.sum(self.state[i : i + shapeHight, j : j + shapeWidth] * shape))
                    if score == 5 or score == -5:
                        return score // 5
        return 0                    
                        
if __name__ == "__main__":
    game = Game(side = 5)
    while game.outcome() == 0:
        print(game.state)
        x = int(input("enter x: "))
        y = int(input("enter y: "))
        game.playMove(x, y)
        
    print("Game over!")
    print(game.outcome())
        
                        
                    
    