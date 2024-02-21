#!/usr/bin/env python3
from random import randint
import argparse
import keyboard
import os

col_no = None
row_no = None
mine_no = None
flag_no = None
mine_table = None
cover_table = None
cursor_pos = [0, 0]
game_over = False
mine = -1
flag = -1
platform = os.name


def place_mines(m):
    global mine_table
    while m != 0:
        col = randint(0, col_no-1)
        row = randint(0, row_no-1)
        if mine_table[row][col] != mine:
            mine_table[row][col] = mine
            m-=1


def fill_minefield():
    global mine_table
    for row in range(row_no):
        for col in range(col_no):
            if mine_table[row][col] == mine:
                if row-1 > -1 and col-1 > -1 and mine_table[row-1][col-1] != mine:
                    mine_table[row-1][col-1] += 1
                if row-1 > -1 and mine_table[row-1][col] != mine:
                    mine_table[row-1][col] += 1
                if row-1 > -1 and col+1 < col_no and mine_table[row-1][col+1] != mine:
                    mine_table[row-1][col+1] += 1
                if col-1 > -1 and mine_table[row][col-1] != mine:
                    mine_table[row][col-1] += 1
                if col+1 < col_no and mine_table[row][col+1] != mine:
                    mine_table[row][col+1] += 1
                if row+1 < row_no and col-1 > -1 and mine_table[row+1][col-1] != mine:
                    mine_table[row+1][col-1] += 1
                if row+1 < row_no and mine_table[row+1][col] != mine:
                    mine_table[row+1][col] += 1
                if row+1 < row_no and col+1 < col_no and mine_table[row+1][col+1] != mine:
                    mine_table[row+1][col+1] += 1
                

def move_cursor(row, col):
    global cursor_pos
    cursor_pos[0] = row
    cursor_pos[1] = col


def open_cell(row, col):
    global cover_table
    if cover_table[row][col] == 0:
        cover_table[row][col] = 1
        if mine_table[row][col] == 0:
            zero_spread(row, col)
        elif mine_table[row][col] == mine:
            end_screen_display()
    

def place_flag(row, col):
    global cover_table
    global flag_no
    if cover_table[row][col] == 0 and flag_no>0:
        cover_table[row][col] = flag
        flag_no -= 1
    elif cover_table[row][col] == flag:
        cover_table[row][col] = 0
        flag_no +=1


def zero_spread(row, col):
    global cover_table
    if row-1 > -1 and col-1 > -1 and cover_table[row-1][col-1] == 0:
        cover_table[row-1][col-1] = 1
        if mine_table[row-1][col-1] == 0:
            zero_spread(row-1, col-1)
    if row-1 > -1 and cover_table[row-1][col] == 0:
        cover_table[row-1][col] = 1
        if mine_table[row-1][col] == 0:
            zero_spread(row-1, col)       
    if row-1 > -1 and col+1 < col_no and cover_table[row-1][col+1] == 0:
        cover_table[row-1][col+1] = 1
        if mine_table[row-1][col+1] == 0:
            zero_spread(row-1, col+1)
    if col-1 > -1 and cover_table[row][col-1] == 0:
        cover_table[row][col-1] = 1
        if mine_table[row][col-1] == 0:
            zero_spread(row, col-1)
    if col+1 < col_no and cover_table[row][col+1] == 0:
        cover_table[row][col+1] = 1
        if mine_table[row][col+1] == 0:
            zero_spread(row, col+1)
    if row+1 < row_no and col-1 > -1 and cover_table[row+1][col-1] == 0:
        cover_table[row+1][col-1] = 1
        if mine_table[row+1][col-1] == 0:
            zero_spread(row+1, col-1)
    if row+1 < row_no and cover_table[row+1][col] == 0:
        cover_table[row+1][col] = 1
        if mine_table[row+1][col] == 0:
            zero_spread(row+1, col)
    if row+1 < row_no and col+1 < col_no and cover_table[row+1][col+1] == 0:
        cover_table[row+1][col+1] = 1
        if mine_table[row+1][col+1] == 0:
            zero_spread(row+1, col+1)


def display_minefield():
    print("Mark all the mines to win")
    print("Flags:", flag_no)
    for row in range(row_no):
        for col in range(col_no):
            if cover_table[row][col] == 1 and cursor_pos[0] == row and cursor_pos[1] == col:
                print(f"[{mine_table[row][col]}]", end = " ")
            elif cover_table[row][col] == -1 and cursor_pos[0] == row and cursor_pos[1] == col:
                print("[X]", end = " ")
            elif cover_table[row][col] == -1:
                print(" X ", end = " ")
            elif cover_table[row][col] == 1:
                print(f" {mine_table[row][col]} ", end = " ")
            elif cover_table[row][col] == 0 and cursor_pos[0] == row and cursor_pos[1] == col:
                print("[\u25a0]", end = " ")
            else:
                print(" \u25a0 ", end = " ")
        print()
    print("Use \"z\" to open, \"x\" to flag and arrow keys to move")


def check_win_con():
    global game_over
    for row in range(row_no):
        for col in range(col_no):
            if mine_table[row][col] == mine and cover_table[row][col] != flag:
                return
    clear()
    print("YOU WIN")
    game_over = True


def end_screen_display():
    global game_over
    clear()
    for row in range(row_no):
        for col in range(col_no):
            if mine_table[row][col] == mine and cursor_pos[0] == row and cursor_pos[1] == col:
                print("[O]", end = " ")
            elif mine_table[row][col] == mine:
                print(" O ", end = " ")
            elif cover_table[row][col] == 1:
                print(f" {mine_table[row][col]} ", end = " ")
            else:
                print(" \u25a0 ", end = " ")
        print()
    print("GAME OVER")
    game_over = True


def clear():
    if platform == "nt":
        os.system("cls")
    else:
        os.system("clear")


def play():
    first_click = True
    place_mines(flag_no)
    while not game_over:
        clear()
        display_minefield()
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_UP:
            key = event.name
            if key == "q":
                break
            elif key == "up":
                if cursor_pos[0] - 1 > -1:
                    move_cursor(cursor_pos[0] - 1, cursor_pos[1])
            elif key == "down":
                if cursor_pos[0] + 1 < row_no:
                    move_cursor(cursor_pos[0] + 1, cursor_pos[1])
            elif key == "right":
                if cursor_pos[1] + 1 < col_no:
                    move_cursor(cursor_pos[0], cursor_pos[1] + 1)
            elif key == "left":
                if cursor_pos[1] - 1 > -1:
                    move_cursor(cursor_pos[0], cursor_pos[1] - 1)
            elif key == "z":
                if first_click:
                    if mine_table[cursor_pos[0]][cursor_pos[1]] == mine:
                        place_mines(1)
                        mine_table[cursor_pos[0]][cursor_pos[1]] = 0
                    fill_minefield()
                    open_cell(cursor_pos[0], cursor_pos[1])
                else:
                    open_cell(cursor_pos[0], cursor_pos[1]) 
                first_click = False
            elif key == "x":
                place_flag(cursor_pos[0], cursor_pos[1])
                check_win_con()


def main():
    global row_no
    global col_no
    global cover_table
    global mine_table
    global flag_no
    parser=argparse.ArgumentParser()
    parser.add_argument("-l", "--level", help="choose difficulty level 1 or 2 or 3 for board size.(Default is 2)")
    args=parser.parse_args()
    if args.level == "2":
        row_no = 9
        col_no = 15
        flag_no = 20
    elif args.level == "3":
        row_no = 12
        col_no = 16
        flag_no = 35
    else:
        row_no = 9
        col_no = 9
        flag_no = 10
    cover_table = [[0 for _ in range(col_no)] for _ in range(row_no)]
    mine_table = [[0 for _ in range(col_no)] for _ in range(row_no)]
    play()


if __name__ == "__main__":
    main()