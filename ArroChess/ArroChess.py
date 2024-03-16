"""
     ABC DEF GHI
    1   ┃   ┃   1
    2   ┃   ┃   2
    3   ┃   ┃   3
     ━━━╋━━━╋━━━ 
    4   ┃   ┃   4
    5   ┃   ┃   5
    6   ┃   ┃   6
     ━━━╋━━━╋━━━ 
    7   ┃   ┃   7
    8   ┃   ┃   8
    9   ┃   ┃   9
     ABC DEF GHI

    1. Take turns making moves. The first move is not limited, and then you
       need to make moves in the chessboard according to the relative position
       of the previous move in the small grid.
    2. When a certain piece in a small grid is connected in a row, column, or
       diagonal, the piece occupies the small grid.
    3. When pieces occupy small grid in rows, columns, or diagonals on the
       board, the player corresponding to the piece wins.
    4. If the next grid on the board is occupied, a free move is taken.
"""


class Board:
    def __init__(self):
        self.cb = [" " * 9] * 9
        self.O_moving = False
        self.O_occ = [False] * 9
        self.X_occ = [False] * 9
        self.last_move = None
    
    def output(self):
        op = "  ABC DEF GHI \n1 " + self.cb[0][:3] + "┃" + self.cb[1][:3] + "┃" + self.cb[2][:3] +\
             " 1\n2 " + self.cb[0][3:6] + "┃" + self.cb[1][3:6] + "┃" + self.cb[2][3:6] +\
             " 2\n3 " + self.cb[0][6:] + "┃" + self.cb[1][6:] + "┃" + self.cb[2][6:] +\
             " 3\n  ━━━╋━━━╋━━━" +\
             "  \n4 " + self.cb[3][:3] + "┃" + self.cb[4][:3] + "┃" + self.cb[5][:3] +\
             " 4\n5 " + self.cb[3][3:6] + "┃" + self.cb[4][3:6] + "┃" + self.cb[5][3:6] +\
             " 5\n6 " + self.cb[3][6:] + "┃" + self.cb[4][6:] + "┃" + self.cb[5][6:] +\
             " 6\n  ━━━╋━━━╋━━━" +\
             "  \n7 " + self.cb[6][:3] + "┃" + self.cb[7][:3] + "┃" + self.cb[8][:3] +\
             " 7\n8 " + self.cb[6][3:6] + "┃" + self.cb[7][3:6] + "┃" + self.cb[8][3:6] +\
             " 8\n9 " + self.cb[6][6:] + "┃" + self.cb[7][6:] + "┃" + self.cb[8][6:] +\
             " 9\n  ABC DEF GHI "
        print(op)

    def ifValid(self, a, b):
        if self.O_occ[a] or self.X_occ[a] or self.cb[a][b] != " ":
            return False
        if a == None:
            return False
        if not self.O_occ[self.last_move] and not self.X_occ[self.last_move] and a != self.last_move:
            return False
        return True
    
    def move(self, a, b):
        self.last_move = b
        self.O_moving = not self.O_moving
        if self.O_moving:
            ch = "O"
        else:
            ch = "X"
        self.cb[a] = self.cb[a][:b] + ch + self.cb[a][b + 1:]
        if self.cb[a][b - 3] == self.cb[a][b - 6] == ch or\
           (not b % 4 and self.cb[a][b - 4] == self.cb[a][b - 8] == ch) or\
           self.cb[a][b // 3 * 3] == self.cb[a][b // 3 * 3 + 1] == self.cb[a][b // 3 * 3 + 2] == ch:
            if self.O_moving:
                self.cb[a] = " _ ( ) - "
                self.O_occ[a] = True
            else:
                self.cb[a] = "\\ / X / \\"
                self.X_occ[a] = True
            return True
        return False
    
    def ifWin(self):
        if (self.O_occ[a] and self.O_occ[a - 3] and self.O_occ[a - 6]) or \
           (not a % 4 and self.O_occ[a - 4] and self.O_occ[a - 8]) or\
           (self.O_occ[a // 3 * 3] and self.O_occ[a // 3 * 3 + 1] and self.O_occ[a // 3 * 3 + 2]):
            return "O"
        elif (self.X_occ[a] and self.X_occ[a - 3] and self.X_occ[a - 6]) or \
             (not a % 4 and self.X_occ[a - 4] and self.X_occ[a - 8]) or\
             (self.X_occ[a // 3 * 3] and self.X_occ[a // 3 * 3 + 1] and self.X_occ[a // 3 * 3 + 2]):
            return "X"
        else:
            return False


def inPut():
    while 1:
        coor = input().upper()
        if len(coor) == 2 and 65 <= ord(coor[0]) <= 73 and 49 <= ord(coor[1]) <= 57:
            x = ord(coor[0]) - 65
            y = ord(coor[1]) - 49
            return y // 3 * 3 + x // 3, y % 3 * 3 + x % 3
        print("Invalid input")


if __name__ == "__main__":
    board = Board()
    board.output()
    a, b = inPut()
    board.move(a, b)
    board.output()
    while 1:
        a, b = inPut()
        if not board.ifValid(a, b):
            print("Invalid input")
            continue
        grid_occ = board.move(a, b)
        board.output()
        if grid_occ:
            player = board.ifWin()
            if player:
                print("{} Wins!".format(player))
                break
