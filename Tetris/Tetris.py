from pynput import keyboard as kb
from threading import Thread as Td
from time import sleep as sp, time as tm
from os import system as st
from random import randint as ri, seed as sd
from copy import deepcopy as dc


def on_press(key):
    global paused, moving_block, interface, mb_exist

    if hasattr(key, "char") and key.char == "p":
        paused = not paused
    elif key == kb.Key.esc:
        return False
    elif not paused and mb_exist:
        if key == kb.Key.up:
            print("r")
        elif key == kb.Key.left:
            mb = dc(moving_block)
            mb[1] -= 1
            if not if_occupied(interface, mb):
                st("cls")
                show(dc(interface), mb)
                moving_block = mb
        elif key == kb.Key.right:
            pass   
        elif key == kb.Key.down:
            pass
        elif key == kb.Key.space:
            pass


def show(itf, mb):
    global mb_exist
    a = itf
    if mb_exist:
        itf[mb[2]][mb[1]] = "[]"

        if mb[0] == "a1" or mb[0] == "c1" or mb[0] == "e1" or \
           mb[0] == "e3" or mb[0] == "e4" or mb[0] == "f1" or \
           mb[0] == "f3" or mb[0] == "g1" or mb[0] == "g3":
            itf[mb[2]][mb[1] - 1] = "[]"
        if mb[0] == "a1" or mb[0] == "b1" or mb[0] == "c2" or \
           mb[0] == "d1" or mb[0] == "d2" or mb[0] == "e1" or \
           mb[0] == "e2" or mb[0] == "e3" or mb[0] == "f1" or \
           mb[0] == "f3" or mb[0] == "g1" or mb[0] == "g3":
            itf[mb[2]][mb[1] + 1] = "[]"
        if mb[0] == "a2" or mb[0] == "b1" or mb[0] == "c1" or \
           mb[0] == "c2" or mb[0] == "d1" or mb[0] == "e1" or \
           mb[0] == "e2" or mb[0] == "e4" or mb[0] == "f2" or \
           mb[0] == "f4" or mb[0] == "g2" or mb[0] == "g4":
            itf[mb[2] - 1][mb[1]] = "[]"
        if mb[0] == "a2" or mb[0] == "d2" or mb[0] == "e2" or \
           mb[0] == "e3" or mb[0] == "e4" or mb[0] == "f2" or \
           mb[0] == "f4" or mb[0] == "g2" or mb[0] == "g4":
            itf[mb[2] + 1][mb[1]] = "[]"
        if mb[0] == "d1" or mb[0] == "f1" or mb[0] == "g4":
            itf[mb[2] - 1][mb[1] - 1] = "[]"
        if mb[0] == "b1" or mb[0] == "c1" or mb[0] == "d2" or \
           mb[0] == "f4" or mb[0] == "g1":
            itf[mb[2] - 1][mb[1] + 1] = "[]"
        if mb[0] == "f2" or mb[0] == "g3":
            itf[mb[2] + 1][mb[1] - 1] = "[]"
        if mb[0] == "c2" or mb[0] == "f3" or mb[0] == "g2":
            itf[mb[2] + 1][mb[1] + 1] = "[]"
        if mb[0] == "a1" or mb[0] == "c1" or mb[0] == "e1" or \
           mb[0] == "e3" or mb[0] == "e4" or mb[0] == "f1" or \
           mb[0] == "f3" or mb[0] == "g1" or mb[0] == "g1":
            itf[mb[2]][mb[1] - 1] = "[]"
        if mb[0] == "a1":
            itf[mb[2]][mb[1] + 2] = "[]"
        if mb[0] == "a2":
            itf[mb[2] + 2][mb[1]] = "[]"

    for row in itf:
        for c in row:
            print(c, end="")
        print()
    return a


def rand_block():
    sd(tm())
    type_ = chr(ri(97, 103)) + "1"
    y = 1
    if type_[0] == "a":
        y = 0
    return [type_, 4, y]


def if_landed(itf, mb):
    if mb[0] == "a1" or mb[0] == "b1" or mb[0] == "c1" or \
       mb[0] == "d1" or mb[0] == "e1" or mb[0] == "f1" or \
       mb[0] == "g1":
        if mb[2] == 19: return True
    elif mb[0] == "c2" or mb[0] == "d2" or mb[0] == "e2" or \
         mb[0] == "e3" or mb[0] == "e4" or mb[0] == "f2" or \
         mb[0] == "f3" or mb[0] == "f4" or mb[0] == "g2" or \
         mb[0] == "g3"or mb[0] == "g4":
        if mb[2] == 18: return True
    else:
        if mb[2] == 17: return True

    if mb[0] == "a1" or mb[0] == "c1" or mb[0] == "e1" or \
       mb[0] == "e3" or mb[0] == "e4" or mb[0] == "f1" or \
       mb[0] == "f3" or mb[0] == "g1":
        if interface[mb[2] + 1][mb[1] - 1] == "[]": return True
    if mb[0] == "a1" or mb[0] == "b1" or mb[0] == "d1" or \
       mb[0] == "d2" or mb[0] == "e1" or mb[0] == "e2" or \
       mb[0] == "e3" or mb[0] == "f1" or mb[0] == "g1" or \
       mb[0] == "g3":
        if interface[mb[2] + 1][mb[1] + 1] == "[]": return True
    if mb[0] == "a1" or mb[0] == "b1" or mb[0] == "c1" or \
       mb[0] == "c2" or mb[0] == "d1" or mb[0] == "e1" or \
       mb[0] == "f1" or mb[0] == "f3" or mb[0] == "g1" or \
       mb[0] == "g3":
        if interface[mb[2] + 1][mb[1]] == "[]": return True
    if mb[0] == "d2" or mb[0] == "e2" or mb[0] == "e3" or \
       mb[0] == "e4" or mb[0] == "f2" or mb[0] == "f4" or \
       mb[0] == "g2" or mb[0] == "g4":
        if interface[mb[2] + 2][mb[1]] == "[]": return True
    if mb[0] == "d1" or mb[0] == "g4":
        if interface[mb[2]][mb[1] - 1] == "[]": return True
    if mb[0] == "c1" or mb[0] == "f4":
        if interface[mb[2]][mb[1] + 1] == "[]": return True
    if mb[0] == "f2" or mb[0] == "g3":
        if interface[mb[2] + 2][mb[1] - 1] == "[]": return True
    if mb[0] == "c2" or mb[0] == "f3" or mb[0] == "g2":
        if interface[mb[2] + 2][mb[1] + 1] == "[]": return True
    if mb[0] == "a1":
        if interface[mb[2] + 1][mb[1] + 2] == "[]": return True
    if mb[0] == "a2":
        if interface[mb[2] + 3][mb[1]] == "[]": return True

    return False


def if_occupied(itf, mb):
    if mb[0] == "a1" or mb[0] == "c1" or mb[0] == "e1" or \
       mb[0] == "e3" or mb[0] == "e4" or mb[0] == "f1" or \
       mb[0] == "f3" or mb[0] == "g1" or mb[0] == "g3":
        if 0 <= mb[2] <= 19 or 0 <= mb[1] - 1 <= 9 or \
           interface[mb[2]][mb[1] - 1] == "[]":
            return True
    if mb[0] == "a1" or mb[0] == "b1" or mb[0] == "c2" or \
       mb[0] == "d1" or mb[0] == "d2" or mb[0] == "e1" or \
       mb[0] == "e2" or mb[0] == "e3" or mb[0] == "f1" or \
       mb[0] == "f3" or mb[0] == "g1" or mb[0] == "g3":
        if 0 <= mb[2] <= 19 or 0 <= mb[1] + 1 <= 9 or \
           interface[mb[2]][mb[1] + 1] == "[]":
            return True
    if mb[0] == "a2" or mb[0] == "b1" or mb[0] == "c1" or \
       mb[0] == "c2" or mb[0] == "d1" or mb[0] == "e1" or \
       mb[0] == "e2" or mb[0] == "e4" or mb[0] == "f2" or \
       mb[0] == "f4" or mb[0] == "g2" or mb[0] == "g4":
        if 0 <= mb[2] - 1 <= 19 or 0 <= mb[1] <= 9 or \
           interface[mb[2] - 1][mb[1]] == "[]":
            return True
    if mb[0] == "a2" or mb[0] == "d2" or mb[0] == "e2" or \
       mb[0] == "e3" or mb[0] == "e4" or mb[0] == "f2" or \
       mb[0] == "f4" or mb[0] == "g2" or mb[0] == "g4":
        if 0 <= mb[2] + 1 <= 19 or 0 <= mb[1] <= 9 or \
           interface[mb[2] + 1][mb[1]] == "[]":
            return True
    if mb[0] == "d1" or mb[0] == "f1" or mb[0] == "g4":
        if 0 <= mb[2] - 1 <= 19 or 0 <= mb[1] - 1 <= 9 or \
           interface[mb[2] - 1][mb[1] - 1] == "[]":
            return True
    if mb[0] == "b1" or mb[0] == "c1" or mb[0] == "d2" or \
       mb[0] == "f4" or mb[0] == "g1":
        if 0 <= mb[2] - 1 <= 19 or 0 <= mb[1] + 1 <= 9 or \
           interface[mb[2] - 1][mb[1] + 1] == "[]":
            return True
    if mb[0] == "f2" or mb[0] == "g3":
        if 0 <= mb[2] + 1 <= 19 or 0 <= mb[1] - 1 <= 9 or \
           interface[mb[2] + 1][mb[1] - 1] == "[]":
            return True
    if mb[0] == "c2" or mb[0] == "f3" or mb[0] == "g2":
        if 0 <= mb[2] <= 19 or 0 <= mb[1] - 1 <= 9 or \
           interface[mb[2] + 1][mb[1] + 1] == "[]":
            return True
    if mb[0] == "a1" or mb[0] == "c1" or mb[0] == "e1" or \
       mb[0] == "e3" or mb[0] == "e4" or mb[0] == "f1" or \
       mb[0] == "f3" or mb[0] == "g1" or mb[0] == "g1":
        if 0 <= mb[2] <= 19 or 0 <= mb[1] - 1 <= 9 or \
           interface[mb[2]][mb[1] - 1] == "[]":
            return True
    if mb[0] == "a1":
        if 0 <= mb[2] <= 19 or 0 <= mb[1] - 1 <= 9 or \
           interface[mb[2]][mb[1] + 2] == "[]":
            return True
    if mb[0] == "a2":
        if 0 <= mb[2] <= 19 or 0 <= mb[1] - 1 <= 9 or \
           interface[mb[2] + 2][mb[1]] == "[]":
            return True
    return False


def add_block(itf, mb):
    itf[mb[2]][mb[1]] = "[]"
    if mb[0] == "a1" or mb[0] == "c1" or mb[0] == "e1" or \
       mb[0] == "e3" or mb[0] == "e4" or mb[0] == "f1" or \
       mb[0] == "f3" or mb[0] == "g1" or mb[0] == "g3":
        itf[mb[2]][mb[1] - 1] = "[]"
    if mb[0] == "a1" or mb[0] == "b1" or mb[0] == "c2" or \
       mb[0] == "d1" or mb[0] == "d2" or mb[0] == "e1" or \
       mb[0] == "e2" or mb[0] == "e3" or mb[0] == "f1" or \
       mb[0] == "f3" or mb[0] == "g1" or mb[0] == "g3":
        itf[mb[2]][mb[1] + 1] = "[]"
    if mb[0] == "a2" or mb[0] == "b1" or mb[0] == "c1" or \
       mb[0] == "c2" or mb[0] == "d1" or mb[0] == "e1" or \
       mb[0] == "e2" or mb[0] == "e4" or mb[0] == "f2" or \
       mb[0] == "f4" or mb[0] == "g2" or mb[0] == "g4":
        itf[mb[2] - 1][mb[1]] = "[]"
    if mb[0] == "a2" or mb[0] == "d2" or mb[0] == "e2" or \
       mb[0] == "e3" or mb[0] == "e4" or mb[0] == "f2" or \
       mb[0] == "f4" or mb[0] == "g2" or mb[0] == "g4":
        itf[mb[2] + 1][mb[1]] = "[]"
    if mb[0] == "d1" or mb[0] == "f1" or mb[0] == "g4":
        itf[mb[2] - 1][mb[1] - 1] = "[]"
    if mb[0] == "b1" or mb[0] == "c1" or mb[0] == "d2" or \
       mb[0] == "f4" or mb[0] == "g1":
        itf[mb[2] - 1][mb[1] + 1] = "[]"
    if mb[0] == "f2" or mb[0] == "g3":
        itf[mb[2] + 1][mb[1] - 1] = "[]"
    if mb[0] == "c2" or mb[0] == "f3" or mb[0] == "g2":
        itf[mb[2] + 1][mb[1] + 1] = "[]"
    if mb[0] == "a1" or mb[0] == "c1" or mb[0] == "e1" or \
       mb[0] == "e3" or mb[0] == "e4" or mb[0] == "f1" or \
       mb[0] == "f3" or mb[0] == "g1" or mb[0] == "g1":
        itf[mb[2]][mb[1] - 1] = "[]"
    if mb[0] == "a1":
        itf[mb[2]][mb[1] + 2] = "[]"
    if mb[0] == "a2":
        itf[mb[2] + 2][mb[1]] = "[]"


"""
                a2 [] b1 [][]      [][]    []
    a1 []{}[][]    {}    {}[] c1 []{}   c2 {}[]
                   []                        []
                   []

    d1 [][]        []      []      []                  []
         {}[] d2 {}[] e1 []{}[] e2 {}[] e3 []{}[] e4 []{}
                 []                []        []        []

    f1 []       f2 [] f3 []{}[] f4 [][]
       []{}[]      {}        []    {}
                 [][]              []

           []    []             g4 [][]
    g1 []{}[] g2 {}   g3 []{}[]      {}
                 [][]    []          []
"""
if __name__ == "__main__":
    paused = False
    moving_block = [None] * 3  # eg: ["c2", 3, 15]
    mb_exist = False

    listener = kb.Listener(on_press=on_press)
    listener.start()
    interface = [[" ." for j in range(10)] for i in range(20)]

    while True:
        st("cls")
        show(dc(interface), dc(moving_block))
        sp(.3)
        if not mb_exist:
            moving_block = rand_block()
            mb_exist = True
            if if_occupied(interface, moving_block):
                st("cls")
                show(dc(interface), dc(moving_block))
                break
        else:
            moving_block[2] += 1
        if if_landed(interface, moving_block):
            add_block(interface, moving_block)
            mb_exist = False
            moving_block = [None] * 3
        if not listener.is_alive():
            break
