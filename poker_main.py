from POKER import Game
from POKER import Player
from POKER import Bot   

choice = 0
while choice != 2:
    choice = int(input(("Welcome to Poker.py! \n1: Create New Game \n2: Exit Game\n")))
    match choice:
        case 1:
            playerlist = [] 
            print("How many players (maximum 4): ")
            playercount = int(input())
            for x in range(0,playercount):
                playerlist.append(Player(input("Input player name: "), int(input("Player balance: "))))
            if(playercount < 4):
                max_bot_bal = int(input("Input maximum possible bot balance: "))
                for b in range(0, 4 - playercount):
                        playerlist.append(Bot(max_bot_bal))
            game = Game(playerlist)
            print("\n--------------\nSTARTING GAME\n--------------\n")
            game.play()