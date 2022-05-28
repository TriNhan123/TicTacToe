
import json
import random
from enum import Enum

class gameState(Enum): 
    playing = 0 
    player_win = 1 
    bot_win = 2 
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
        self.player_name = ""

    def readHistory(self, player_name): 
        file = open('playerBase.json', 'r')
        self.playerBase = json.load(file)
        file.close()

        if player_name not in self.playerBase: 
            self.playerBase[player_name] = {'games_played' : 0, 'games_won' : 0 }
        
        
    def recordHistory(self, gameState, player_name):
        self.playerBase[player_name]['games_played'] += 1 
        if gameState == gameState.player_win:
            self.playerBase[player_name]['games_won'] += 1 
        print(self.playerBase[player_name])
        file = open('playerBase.json', 'w') 
        json.dump(self.playerBase, file)
        file.close()


    def newGame(self, new_player):
        if new_player: 
            self.player_name = input("Enter your name: ").strip()
        self.readHistory(self.player_name)
        self.board = [[" "] * self.n for _ in range(self.n)]
        self.rows = [0] * self.n 
        self.cols = [0] * self.n 
        self.diag = 0
        self.anti = 0
        while True: # while game not over

            r, c = [int(x) for x in input("Enter your move: ").split()]
            if r > (self.n - 1) or c > (self.n - 1): 
                print("3x3 tictactoe") 
                continue
            if self.board[r][c] != " ": 
                print("illegal move")
                continue

            player_move = self.playerMove(r, c)
            player_game_state = self.checkGameState(player_move, "X")

            if player_game_state == gameState.player_win: 
                self.recordHistory(gameState.player_win, self.player_name)
                self.renderBoard()
                print('You win')
                break 

            if player_game_state == gameState.draw: 
                self.recordHistory(gameState.draw, self.player_name)
                print('Draw')
                break
            
            bot_move = self.botMove()
            bot_move_state = self.checkGameState(bot_move, "O")

            if bot_move_state == gameState.bot_win: 
                self.recordHistory(gameState.bot_win, self.player_name)
                self.renderBoard()
                print('Bot win')
                break

            if bot_move_state == gameState.draw: 
                self.recordHistory(gameState.draw, self.player_name)
                print('Draw')
                break
            
            self.renderBoard()


        choice = input("Play again? Y or N: ").strip() 
        if choice == "Y": 
            self.newGame(False) 
        elif choice == "N": 
            print("Bye")

    def checkAvailableMove(self): 
        available_moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])): 
                if self.board[r][c] == " ": 
                    available_moves.append([r, c])
        return available_moves

    def playerMove(self, r, c):
        self.board[r][c] = "X"
        return [r, c] 

    def botMove(self): 
        available_moves = self.checkAvailableMove()
        random_move = random.choice(available_moves)
        r, c = random_move
        self.board[r][c] = "O"
        return [r, c]
    
    
    def checkGameState(self, move, turn): 
        r, c = move 
        val = 1 if turn == "X" else -1

        self.rows[r] += val 
        self.cols[c] += val 
        if r == c: self.diag += val 
        if r + c == (self.n - 1): self.anti += val 
        if (abs(self.rows[r]) == self.n or abs(self.cols[c]) == self.n 
            or abs(self.diag) == self.n or abs(self.anti) == self.n):
            return gameState.player_win if turn == "X" else gameState.bot_win
        elif not self.checkAvailableMove(): 
            return gameState.draw
        return gameState.playing
        
    def renderBoard(self): 
        for row in self.board: 
            for i, item in enumerate(row): 
                if i == 0: 
                    print("|" + item, end = "|")
                else:
                    print(item, end = "|")
            print()        

game = TicTacToe(4)
game.newGame(True)
# game.renderBoard()