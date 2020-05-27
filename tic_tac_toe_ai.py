'''
Created on Thu May 21 12:28:14 2020
@author: Tyler Brennan

Utilizing minimax algorithm to create an artificial intelligence to play tic tac toe
'''
import numpy as np
import copy 

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

def choose_player():
    user = input("Enter if you want to be X or O (put anything else for random): ").lower()
    if user == 'x' or user == 'o':
        player = PLAYERS.index(user)
    else:
        player = np.random.randint(2)
        print("You are playing as", PLAYERS[player])
    comp = (player + 1) % 2
    return player, comp

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
# OUT: win - boolean value if one player has won, tie - boolean value for if there is a tie, winner - the person who won (or ' ' if tie)
def end(game, win, tie):
    for i in range(BOARD_SIZE):     # Checks columns and rows
        col = set()
        row = set()
        for column in range(BOARD_SIZE):
            col.add(game[i][column])
        for horizontal in range(BOARD_SIZE):
            row.add(game[horizontal][i])
        if len(col) == 1 and ' ' not in col:
            win = True
            return  win, tie, col.pop()
        elif len(row) == 1 and ' ' not in row:
            win = True
            return  win, tie, row.pop()
    cross1 = set()
    cross2 = set()
    for pt in range(BOARD_SIZE):    # Checks each cross
        cross1.add(game[pt][pt])
        cross2.add(game[pt][BOARD_SIZE - pt - 1])
    if len(cross1) == 1 and ' ' not in cross1:
        win = True
        return win, tie, cross1.pop()
    elif len(cross2) == 1 and ' ' not in cross2:
        win = True
        return win, tie, cross2.pop()
    count = 0
    for line in game:
        if " " not in line:
            count += 1
    if count == BOARD_SIZE:
        tie = True
    return win, tie, ' '

# AI for the computer player
# IN: game - the game board, player - numeric representation of the player (AI in this case)
def ai(game, player, comp):
    blank = []
    choices = []
    best = {}
    
    win = False
    tie = False
    
    # Determine if the game is over and return score
    win, tie, winner = end(game, win, tie)
    if win and winner == PLAYERS[comp]:
        best['score'] = 1
        return best
    elif win  and winner != PLAYERS[comp]:
        best['score'] = -1
        return best
    elif tie:
        best['score'] = 0
        return best
    
    # Find every possible move
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if game[row][col] == " ":
                blank.append([row, col])
                
    # For every possible move recursively call the algorithm and record the scores
    for space in blank:
        temp = copy.deepcopy(game)
        choice = {}
        choice['pt'] = space
        temp[space[0]][space[1]] = PLAYERS[player]
        temp_dict = ai(temp, (player + 1) % 2, comp)
        choice['score'] = temp_dict['score']
        choices.append(choice)
        
    # Determine the best plays for the AI and the player
    if player == comp:
        best['score'] = -100
        for choice in choices:
            if choice['score'] >= best['score']:
                best['score'] = choice['score']
                best['pt'] = choice['pt']
    elif player != comp:
        best['score'] = 100
        for choice in choices:
            if choice['score'] <= best['score']:
                best['score'] = choice['score']
                best['pt'] = choice['pt']
    return best


    
win = False
tie = False
player, comp = choose_player()
game = setup()
while not win and not tie:
    if player == comp:
        play = ai(game, player, comp)
        game[play['pt'][0]][play['pt'][1]] = PLAYERS[comp]
    else:
        choice(player, game)
    win, tie, winner = end(game, win, tie)
    player = (player + 1) % 2
if win:
    print_board(game)
    print("\n", winner, "has won!")
else:
    print_board(game)
    print("\n Sorry it's a tie!")