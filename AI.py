
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
        self.board = [[""] * 3 for _ in range(3)]
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

    def checkAvailableMove(self, board): 
        available_moves = []
        for r in range(len(board)):
            for c in range(len(board[r])): 
                if self.board[r][c] == " ": 
                    available_moves.append([r, c])
        return available_moves

    def playerMove(self, r, c): 
        self.board[r][c] = "X"
        return [r, c] 

    def botMove(self): 
        available_moves = self.checkAvailableMove(self.board)
        best_score = float("-inf")
        best_move = (-1, -1)
        original_board = self.board

        for possible_move in available_moves: 
            self.move(possible_move, "O", self.board)
            score = self.calculate(possible_move, "O", 2, self.board) 
            self.undo(original_board)

            if score > best_score: 
                best_score = score 
                best_move = possible_move
        r, c = best_move
        self.board[r][c] = "O"
        return [r, c]   

    def calculate(self, move, turn, board): 
        game_state = self.checkGameState(move, turn)
        original_board = board
        if game_state != gameState.playing: 
            if game_state == gameState.draw: 
                return 0 
            else: 
                return 1 if game_state == gameState.bot_win else -1
            
            
        scores = []
        
        available_moves = self.checkAvailableMove(board)
        for possible_move in available_moves: 
            if turn == "O": 
                new_turn = "X"
            elif turn == "X": 
                new_turn = "O"
            self.move(possible_move, new_turn, board)
            scores.append(self.calculate(possible_move, new_turn, board))
            self.undo(original_board)
            
        print(scores)
        if (turn == "O" and game_state == gameState.bot_win): 
            return max(scores) 
        else: 
            return min(scores)
        
    def move(self, move, turn, board): 
        r, c = move 
        if turn == "X": 
            board[r][c] == "X"
        else: 
            board[r][c] == "O"

    def undo(self, ori_game_state): 
        board, rows, cols, diag, anti = ori_game_state
        self.board = board
        self.rows = rows 
        self.cols = cols 
        self.diag = diag 
        self.anti = anti 
        
        
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
        elif not self.checkAvailableMove(self.board): 
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

game = TicTacToe(3)
game.newGame(True)
# game.renderBoard()
