import level1
import level2
def main(): 
    level = int(input("Choose level:"))
    size = int(input("Choose size:"))
    if level == 1: 
        game = level1.level1Game(size)
        game.newGame(True)
    elif level == 2: 
        game = level2.level2Game(size)
        game.newGame(True)
if __name__=="__main__":
    main()