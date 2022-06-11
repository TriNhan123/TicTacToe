from doctest import TestResults
from tictactoe import*

class level2Game(TicTacToe): 
    def __init__(self, n): 
        TicTacToe.__init__(self, n)
        self.player_1 = ""
        self.player_2 = ""
    
    def newGame(self, new_player):
        if new_player: 
            self.player_1 = input("P1, Enter your name: ").strip()
            self.player_2 = input("P2, Enter your name: ").strip()
        
        self.readHistory(self.player_1)
        self.readHistory(self.player_2) 

        #init new board 
        self.board = [[" "] * self.n for _ in range(self.n)]    
        self.rows = [0] * self.n 
        self.cols = [0] * self.n 
        self.diag = 0
        self.anti = 0

        while True: 
            r1, c1 = [int(x) for x in input("P1, Enter your move: ").split()]

            while self.checkValidMove(r1, c1) == False: 
                r1, c1 = [int(x) for x in input("P1, Enter your move: ").split()]
            self.playerMove(1, r1, c1) 
            player_1_state = self.checkGameState(1, r1, c1)
            if player_1_state == gameState.player_1_win: 
                self.recordHistory(True, self.player_1)
                self.recordHistory(False, self.player_2)
                self.renderBoard()
                print('Player 1 win')
                break 
            if player_1_state == gameState.draw: 
                self.recordHistory(False, self.player_1)
                self.recordHistory(False, self.player_2)
                print('Draw')
                break 
            self.renderBoard()

            r2, c2 = [int(x) for x in input("P2, Enter your move: ").split()]

            while self.checkValidMove(r2, c2) == False:
                r2, c2 = [int(x) for x in input("P2, Enter your move: ").split()]
            self.playerMove(2, r2, c2) 
            player_2_state = self.checkGameState(2, r2, c2)
            if player_2_state == gameState.bot_player_2_win: 
                self.recordHistory(True, self.player_2)
                self.recordHistory(False, self.player_1)
                self.renderBoard()
                print('Player 2 win')
                break 
            if player_2_state == gameState.draw: 
                self.recordHistory(False, self.player_2)
                self.recordHistory(False, self.player_1)
                print('Draw')
                break   
            self.renderBoard()

        choice = input("Play again? Y or N: ").strip() 
        if choice == "Y": 
            self.newGame(False) 
        elif choice == "N": 
            print("Bye")
    
        




    