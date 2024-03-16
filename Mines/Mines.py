from random import randint, seed
from time import time


def clr(text: str, c: int):
    if c == 0:  # black
        return "\033[30m" + text + "\033[0m"
    elif c == 1:  # italic
        return "\033[3m" + text + "\033[0m"
    elif c == 2:  # underline
        return "\033[4m" + text + "\033[0m"
    elif c == 3:  # red
        return "\033[31m" + text + "\033[0m"
    elif c == 4:  # green
        return "\033[32m" + text + "\033[0m"
    elif c == 5:  # yellow
        return "\033[33m" + text + "\033[0m"
    elif c == 6:  # blue
        return "\033[34m" + text + "\033[0m"
    elif c == 7:  # magenta
        return "\033[35m" + text + "\033[0m"
    elif c == 8:  # cyan
        return "\033[36m" + text + "\033[0m"
    elif c == 9:
        return "\033[5;7m" + text + "\033[0m"


def show(field: list) -> None:
    print(clr("   A B C D E F G H I J K L M N O P Q R S T U V W X Y Z", 1))
    for row in range(12):
        if 0<=row<=8:
            print(" " + clr(str(row + 1), 1), end=clr("|", 0))
        else:
            print(clr(str(row + 1), 1), end=clr("|", 0))
        
        for col in field[row]:
            if not col[1]:
                if col[0] == ">" or col[0] == ".":
                    print(clr(">", 0), end=clr("|", 0))
                else:
                    print(clr("_", 0), end=clr("|", 0))
            else:
                if col[0].isdigit():
                    print(clr(col[0], int(col[0])), end=clr("|", 0))
                elif col[0] == "!":
                    print(clr("!", 9), end=clr("|", 0))
                else:
                    print(" ", end=clr("|", 0))
        print(clr(str(row + 1), 1))
    print(clr("   A B C D E F G H I J K L M N O P Q R S T U V W X Y Z", 1))


def generate(mx: int, my: int) -> list:
    field = [[[" ", False] for i in range(26)] for j in range(12)]  # False for invisible operatable, True for visible and not operatable
    field[my][mx][1] = True
    for i in range(0, 50):  # generate mines
        seed(time())
        x, y = randint(0, 25), randint(0, 11)
        while field[y][x][0] != " " or (mx == x and my == y):
            x, y = randint(0, 25), randint(0, 11)
        field[y][x][0] = "*"
    for y in range(12):  # generate numbers
        for x in range(26):
            if field[y][x][0] == " ":
                num = 0
                if x >= 1:  # ←
                    if field[y][x-1][0] == "*": num += 1
                if x <= 24:  # →
                    if field[y][x+1][0] == "*": num += 1
                if y >= 1:  # ↑
                    if field[y-1][x][0] == "*": num += 1
                if y <= 10:  # ↓
                    if field[y+1][x][0] == "*": num += 1
                if x >= 1 and y >= 1:  # ↖
                    if field[y-1][x-1][0] == "*": num += 1
                if x >= 1 and y <= 10:  # ↗
                    if field[y+1][x-1][0] == "*": num += 1
                if x <= 24 and y >= 1:  # ↙
                    if field[y-1][x+1][0] == "*": num += 1
                if x <= 24 and y <= 10:  # ↘
                    if field[y+1][x+1][0] == "*": num += 1
                
                if num: field[y][x][0] = str(num)
    
    if field[my][mx][0] == " ":
        return erase(field, mx, my)
    else:
        return generate(mx, my)


def input_() -> tuple:
    while True:
        i = input().upper()
        if i[0].isalpha():
            x = ord(i[0]) - 65
            if i[1:].isdigit() and  1 <= int(i[1:]) <= 12:
                y = int(i[1:]) - 1
                z = " "
                break
        elif i[0] == ">":
            if i[1].isalpha():
                x = ord(i[1]) - 65
                if i[2:].isdigit() and  1 <= int(i[2:]) <= 12:
                    y = int(i[2:]) - 1
                    z = i[0]
                    break
        print("Wrong input\a")
    return x, y, z


def erase(field: list, x: int, y: int) -> list:
    if x >= 1 and y >= 1 and not field[y-1][x-1][1]:
        field[y-1][x-1][1] = True
        if field[y-1][x-1][0] == " ":
            field = erase(field, x-1, y-1)
    if x >= 1 and y <= 10 and not field[y+1][x-1][1]:
        field[y+1][x-1][1] = True
        if field[y+1][x-1][0] == " ":
            field = erase(field, x-1, y+1)
    if x <= 24 and y >= 1 and not field[y-1][x+1][1]:
        field[y-1][x+1][1] = True
        if field[y-1][x+1][0] == " ":
            field = erase(field, x+1, y-1)
    if x <= 24 and y <= 10 and not field[y+1][x+1][1]:
        field[y+1][x+1][1] = True
        if field[y+1][x+1][0] == " ":
            field = erase(field, x+1, y+1)
    if x >= 1 and not field[y][x-1][1]:
        field[y][x-1][1] = True
        if field[y][x-1][0] == " ":
            field = erase(field, x-1, y)
    if y >= 1 and not field[y-1][x][1]:
        field[y-1][x][1] = True
        if field[y-1][x][0] == " ": 
            field = erase(field, x, y-1)
    if x <= 24 and not field[y][x+1][1]:
        field[y][x+1][1] = True
        if field[y][x+1][0] == " ":
            field = erase(field, x+1, y)
    if y <= 10 and not field[y+1][x][1]:
        field[y+1][x][1] = True
        if field[y+1][x][0] == " ":
            field = erase(field, x, y+1)
    return field


def operate(field: list, x: int, y: int, z: str) -> tuple:
    if field[y][x][0] == "*" or field[y][x][0] == ">":
        if z == " ":
            field[y][x][1] = True
            field[y][x][0] = "!"
            return field, True
        elif field[y][x][0] == ">":
            field[y][x][0] = "*"
        else:
            field[y][x][0] = ">"
    else:
        if z == " ":
            field[y][x][1] = True
            if field[y][x][0] == " ":
                field = erase(field, x, y)
        else:
            if field[y][x][0] == " ":
                field[y][x][0] = "."
            else:
                field[y][x][0] = " "
    return field, False


def ifWin(field: list) -> int:
    num = 0
    win = True
    for row in field:
        for col in row:
            if col[0] == ">":
                num += 1
            elif col[0] == ".":
                win = False
    return num - 50


if __name__ == "__main__":
    show([[[" ", False] for i in range(26)] for j in range(12)])
    x, y, z = input_()
    while z != " ":
        print("Wrong input\a")
        x, y, z = input_()
    mineField = generate(x, y)
    # "_" unknown
    # " " none
    # "*" mine
    # ">" flagged
    # "." flagged wrong
    # "!" bombed

    bombed = False
    while not bombed:
        show(mineField)
        x, y, z =  input_()
        if not mineField[y][x][1]:
            mineField, bombed = operate(mineField, x, y, z)
            if not ifWin(mineField):
                break
        else:
            print("Wrong input\a")
    show(mineField)
    if bombed:    
        print("Fail")
    else:
        print("Win")


# erase()如何处理错误标记？
# 错误