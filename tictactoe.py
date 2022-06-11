import json
import random
from enum import Enum

class gameState(Enum): 
    playing = 0 
    player_1_win = 1 
    bot_player_2_win = 2 
    draw = 3 

class TicTacToe: 
    def __init__(self, n): 
        self.board = [[""] * n for _ in range(n)]
        self.n = n 
        self.rows = [0] * n
        self.cols = [0] * n 
        self.diag = 0
        self.anti = 0 
        self.playerBase = {}

    def readHistory(self, player_name): 
        file = open('playerBase.json', 'r')
        self.playerBase = json.load(file)
        file.close()

        if player_name not in self.playerBase: 
            self.playerBase[player_name] = {'games_played' : 0, 'games_won' : 0 }   
        
    def recordHistory(self, isWinner, player_name):
        self.playerBase[player_name]['games_played'] += 1 
        if isWinner:
            self.playerBase[player_name]['games_won'] += 1 
        print(player_name + " stat:", self.playerBase[player_name])
        file = open('playerBase.json', 'w') 
        json.dump(self.playerBase, file)
        file.close()

    def checkAvailableMove(self): 
        available_moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])): 
                if self.board[r][c] == " ": 
                    available_moves.append([r, c])
        return available_moves

    def checkValidMove(self, r, c): 
        #True if valid, False if not valid
        if r > (self.n - 1) or c > (self.n - 1): 
            print(f"This is {self.n} * {self.n} tictactoe") 
            return False 
        if self.board[r][c] != " ": 
            print("illegal move")
            return False
        return True

    def playerMove(self, player, r, c):
        if player == 1: 
            self.board[r][c] = 'X'
        elif player == 2: 
            self.board[r][c] = 'O'

    def botMove(self): 
        available_moves = self.checkAvailableMove()
        random_move = random.choice(available_moves)
        r, c = random_move
        self.board[r][c] = "O"
        return r, c
     
    def renderBoard(self): 
        for row in self.board: 
            for i, item in enumerate(row): 
                if i == 0: 
                    print("|" + item, end = "|")
                else:
                    print(item, end = "|")
            print()        

    def checkGameState(self, player, r, c): 
        val = 1 if player == 1 else -1

        self.rows[r] += val 
        self.cols[c] += val 
        if r == c: self.diag += val 
        if r + c == (self.n - 1): self.anti += val 

        if (abs(self.rows[r]) == self.n or abs(self.cols[c]) == self.n 
            or abs(self.diag) == self.n or abs(self.anti) == self.n):
            return gameState.player_1_win if player == 1 else bot_player_2_win
        elif not self.checkAvailableMove(): 
            return gameState.draw
        return gameState.playing