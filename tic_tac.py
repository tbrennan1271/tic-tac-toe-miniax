#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 12:28:14 2020

@author: tylerbrennan
"""
import numpy as np
BOARD_SIZE = 3
PLAYERS = ["X", "O"]

# Creates a 2D array to hold all game values
# OUT: game - the game board 
def setup():
    game = []
    for i in range(BOARD_SIZE):
        temp = []
        for j in range(BOARD_SIZE):
            temp.append(" ")
        game.append(temp)
    return game

# Provides a visual representation of the board
def print_board(game):
    print()
    spacing = "---" * BOARD_SIZE + ("-" * (BOARD_SIZE - 3))     # Just makes the board look even for each BOARD_SIZE input
    for i in range(len(game)):
        row = game[i]
        line = ""
        for j in range(len(row)):
            line += row[j]
            if j < BOARD_SIZE - 1:
                line += " | "
        
        print(line)
        if i < BOARD_SIZE - 1:
            print(spacing)

# Takes in player choice and determines if it is valid
# IN: player - the player who is making the choice, game - the game board
def choice(player, game):
    print_board(game)
    print("\n", PLAYERS[player], "player, it is your turn")
    user_in = input("Enter your choice as 'row column': ")
    user_in = user_in.split()
    for i in range(len(user_in)):
        user_in[i] = int(user_in[i]) - 1
        if user_in[i] > BOARD_SIZE - 1 or user_in[i] < 0:
            print("Please enter a choice within the correct range: 1 to", BOARD_SIZE)
            choice(player, game)
            return
    if game[user_in[0]][user_in[1]] == " ":
        game[user_in[0]][user_in[1]] = PLAYERS[player]
    else:
        print("Please enter a choice that has not already been taken")
        choice(player, game)
        return
    
# Determines if a player wins or if there is a tie
# IN: game - the game board, win - boolean value if one player has won, tie - boolean value for if there is a tie
# OUT: win - boolean value if one player has won, tie - boolean value for if there is a tie
def score(game, win, tie):
    for i in range(BOARD_SIZE):
        col = set()
        row = set()
        for column in range(BOARD_SIZE):
            col.add(game[i][column])
        for horizontal in range(BOARD_SIZE):
            row.add(game[horizontal][i])
        if (len(col) == 1 and ' ' not in col) or (len(row) == 1 and ' ' not in row):
            win = True
            return  win, tie
    cross1 = set()
    cross2 = set()
    for pt in range(BOARD_SIZE):
        cross1.add(game[pt][pt])
        cross2.add(game[pt][BOARD_SIZE - pt - 1])
    if (len(cross1) == 1 and ' ' not in cross1) or (len(cross2) == 1 and ' ' not in cross2):
        win = True
        return win, tie
    count = 0
    for line in game:
        if " " not in line:
            count += 1
    if count == BOARD_SIZE:
        tie = True
    return win, tie

# def ai(game, player)
    
win = False
tie = False
player = np.random.randint(2)
game = setup()
while not win and not tie:
    if player == 1:
        player = 0
    else: 
        player = 1
    choice(player, game)
    win, tie = score(game, win, tie)
if win:
    print_board(game)
    print("\n", PLAYERS[player], "has won!")
else:
    print_board(game)
    print("\n Sorry it's a tie!")