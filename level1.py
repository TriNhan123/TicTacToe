from tictactoe import*

class level1Game(TicTacToe):
    def __init__(self, n): 
        TicTacToe.__init__(self, n)
        self.player1 = ""

    def newGame(self, new_player):
        if new_player: 
            self.player1 = input("Enter your name: ").strip()
        self.readHistory(self.player1)
        self.board = [[" "] * self.n for _ in range(self.n)]
        self.rows = [0] * self.n 
        self.cols = [0] * self.n 
        self.diag = 0
        self.anti = 0
        while True: # while game not over
            r, c = [int(x) for x in input("Enter your move: ").split()]
            while self.checkValidMove(r, c) == False: 
                r, c = [int(x) for x in input("Enter your move: ").split()]

            self.playerMove(1, r, c)
            player_game_state = self.checkGameState(1, r, c)

            if player_game_state == gameState.player_1_win: 
                self.recordHistory(True, self.player1)
                self.renderBoard()
                print('You win')
                break 

            if player_game_state == gameState.draw: 
                self.recordHistory(False, self.player1)
                print('Draw')
                break
            
            bot_r, bot_c = self.botMove()
            bot_move_state = self.checkGameState(2, bot_r, bot_c)

            if bot_move_state == gameState.bot_player_2_win: 
                self.recordHistory(False, self.player1)
                self.renderBoard()
                print('Bot win')
                break

            if bot_move_state == gameState.draw: 
                self.recordHistory(False, self.player1)
                print('Draw')
                break
            
            self.renderBoard()


        choice = input("Play again? Y or N: ").strip() 
        if choice == "Y": 
            self.newGame(False) 
        elif choice == "N": 
            print("Bye")