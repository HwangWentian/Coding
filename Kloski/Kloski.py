from pynput import keyboard as kb
from random import randint, seed
from time import time
from os import system


class Kloski:
    def __init__(self):
        self.bd = [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]
        
        seed(time())
        for i in range(1, 16):
            while True:
                a, b = randint(0, 3), randint(0, 3)
                if not self.bd[a][b]:
                    self.bd[a][b] = i
                    break
        
        for a in range(0, 4):
            for b in range(0, 4):
                if not self.bd[a][b]:
                    self.posi_0 = [a, b]
        
        self.moves = 0
    
    def show(self):
        system("cls")
        for i in self.bd:
            for j in i:
                if not j:
                    print("    ", end="")
                else:
                    if j < 10:
                        print(" ", end="")
                    print(j, end="  ")
            print()
        
        if self.moves:
            print(self.moves, "moves")

    def move(self, dir):
        a = self.posi_0
        if dir == "u" and a[0] != 3:
            self.bd[a[0]][a[1]] = self.bd[a[0] + 1][a[1]]
            self.bd[a[0] + 1][a[1]] = 0
            self.posi_0[0] += 1
            self.moves += 1
        elif dir == "d" and a[0] != 0:
            self.bd[a[0]][a[1]] = self.bd[a[0] - 1][a[1]]
            self.bd[a[0] - 1][a[1]] = 0
            self.posi_0[0] -= 1
            self.moves += 1
        elif dir == "l" and a[1] != 3:
            self.bd[a[0]][a[1]] = self.bd[a[0]][a[1] + 1]
            self.bd[a[0]][a[1] + 1] = 0
            self.posi_0[1] += 1
            self.moves += 1
        elif dir == "r" and a[1] != 0:
            self.bd[a[0]][a[1]] = self.bd[a[0]][a[1] - 1]
            self.bd[a[0]][a[1] - 1] = 0
            self.posi_0[1] -= 1
            self.moves += 1

    def ifOver(self):
        goal = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 0]]
        if self.bd == goal:
            return True
        return False


def op(key):
    global kloski
    if key == kb.Key.esc:
        return False
    elif key == kb.Key.up:
        kloski.move("u")
        kloski.show()
    elif key == kb.Key.left:
        kloski.move("l")
        kloski.show()
    elif key == kb.Key.right:
        kloski.move("r")
        kloski.show()
    elif key == kb.Key.down:
        kloski.move("d")
        kloski.show()
    if kloski.ifOver():
        print("You win")
        return False


if __name__ == "__main__":
    kloski = Kloski()
    kloski.show()
    listener = kb.Listener(on_press=op)
    listener.start()
    listener.join()
