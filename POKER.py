import random
import poker as p
from poker import card
import names
import copy as cp
import pokerlib as pl
from pokerlib import HandParser
from pokerlib.enums import Rank, Suit
import PySimpleGUI as sg
import math

# Poker.py
# By: Henry Gao
# Submitted: 
# Final project submission for EECE2140 @ Northeastern 2023 
# Mimics a standard game of Texa's Holdem Poker


class Player: 
    """
    Represents a playable player in the poker game.
    """
    def __init__(self, name, balance):
        """
        Constructor that sets up all of the variables for the
        player class
        """
        self.name = name
        self.balance = balance
        self.hand = []
        self.round_choice = ""
        self.ALL_IN = False
        
    def bet(self, amt):
        """
        Bet method that allows a player to place 
        a bet of size 'amt'.
        """
        self.balance -= amt
        
    def display_cards(self):
        """
        Displays the current hand of the player through
        the PySimpleGUI library window.
        """
        print(self.name + " this is your Hand: ")
        card1 = str(self.hand[0].rank) + str(self.hand[0].suit)
        card2 = str(self.hand[1].rank) + str(self.hand[1].suit)
        layout = [
                [sg.Image("Images/" + card1 + ".png"), sg.Image("Images/" + card2 + ".png")],
                [sg.Button('Exit')]
            ]#Tell window what size it needs to be 
        window = sg.Window("hand viewer", layout)
        event, value = window.read()
        while True:
            event, value = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

        window.close() 
    
        print(self.hand)
        print("\n")
        
    def __str__(self):
        result = "Name: {name} \nCurrent Balance: {curr_bal}".format(name = self.name, curr_bal = self.balance)
        return result
        
class Bot(Player):
    """
    Instance of extensibility. Allows the player to create
    playable bots 
    """
    def __init__(self, player_bal):
        """
        Sets the difficulty, name, and balance of the 
        created bot.
        """
        super().__init__(names.get_first_name(), random.randint(8, player_bal))
        

class Game:
    """
    Game object that runs all of the programs
    needed to mimic a full game of poker.
    """
    def __init__(self, players):
        """
        Instantiates the deck, finds the smallest balance, prompts the user
        to input a table limit, and creates the various important tracking
        variables necessary to keep the program functioning.
        """
        self.deck = random.sample(list(p.card.Card), len((list(p.card.Card))))
        self.player_list = players
        self.in_the_round = cp.copy(self.player_list)
        self.poorest_bal = self.player_list[0].balance
        for x in players:
            if x.balance <= self.poorest_bal:
                self.poorest_bal = x.balance
        self.table_limit = 99999999999999999
        for x in self.player_list:
            print(str(x) + "\n")
        self.table_limit = 8
        self.last_bet = 0
        self.all_in = False
        self.pot = 0
        self.raise_active = False
        self.check_distrupted = False
        self.round_num = 1
        self.is_preflop = True
        self.river = []
        
    def deal_cards(self):
        """
        Deals cards to each of the players who are 
        still in the current poker round.
        """
        for i in self.player_list:
            i.hand = [self.deck.pop() for x in range(2)]
    
    def fold_checker(self):
        """
        Checks the case where every player
        folds but one.
        """
        counter = 0
        if len(self.in_the_round) == 1:
            raise ZeroDivisionError
        
    def ask_bot(self, bot):
        """
        If a bot player is present, this method will 
        decided the bots move based on a pre-designed
        algorithm.
        """
        self.all_in_check()
        self.fold_checker()
        if(self.last_bet != 0 and bot.balance >= self.last_bet):
            #if the last bet was higher than 3/4 of the bot's remaining balance, the bot folds
            if(self.last_bet >= bot.balance*.75):
                if bot.ALL_IN == True:
                    return None
                self.check_distrupted = True
                bot.ALL_IN = True
                self.last_bet = bot.balance
                self.pot += bot.balance
                bot.bet(bot.balance)
                print(bot.name + " is ALL IN!")
                bot.round_choice = "raised"
                self.all_in_check()
            else:
                x = random.randint(1,2)
                match x:
                    case 1: 
                        self.check_distrupted = True
                        print(bot.name + " has called with " + str(self.last_bet))
                        self.pot += self.last_bet
                        bot.bet(self.last_bet)
                        bot.round_choice = "called"
                    case 2: 
                        self.check_distrupted = True
                        random_raise = random.randint(1, bot.balance)
                        self.last_bet = random_raise
                        self.pot += random_raise
                        bot.bet(random_raise)
                        bot.round_choice = "raised"
                        print(bot.name + " has raised " + str(random_raise) +"!\n")
                        
                        
        elif(self.last_bet == 0 and bot.balance > 0): #when bot has to go first during the round 
            x = random.randint(1,4)
            if(x == 4 and self.check_distrupted == False): #bot can check
                bot.round_choice = "checked"
                return None
            else:
                match x: 
                    case 1: 
                        self.check_distrupted = True
                        bot.bet(self.last_bet)
                        self.pot += self.last_bet
                        bot.round_choice = "called"
                    case 2: 
                        self.check_distrupted = True
                        random_raise = random.randint(1, bot.balance)
                        self.last_bet = random_raise
                        self.pot += random_raise
                        bot.bet(random_raise)
                        bot.round_choice = "raised"
                        print(bot.name + " has raised " + str(random_raise) +"!\n")
                    case 3: 
                        print(bot.name + " has folded \n")
                        bot.round_choice =  "folded"

                        self.in_the_round.remove(bot)
                        self.all_in_check()
                        self.fold_checker
            
        else: #bot has no more money and has to all in 
            if(bot.ALL_IN == True):
                return None
            self.check_distrupted = True
            bot.ALL_IN = True
            self.last_bet = bot.balance
            self.pot += bot.balance
            bot.bet(bot.balance)
            print(bot.name + " is ALL IN!")
            bot.round_choice = "raised"
            self.all_in_check()
            self.fold_checker()
        # bot.bet(random.uniform(0,30))
        # bot.round_choice = "raised"
        # print(bot.name + "has raised")
        
    
    def ask_player(self, player):
        """
        Prompts the selected player with move options
        depending on the current state of their balance
        and what moves have already been played during the
        round. 
        """
        self.all_in_check()
        self.fold_checker()
        print("Your balance is: " + str(player.balance))
        if(player.ALL_IN == True):
            print("Skipping\n")
            return None
        elif(player.balance < self.last_bet):
            choice = float(input("do you want to all in (1) or fold (2)"))
            match choice:
                case 1:
                    print(player.name + " is going ALL IN")
                    player.ALL_IN = True
                    self.last_bet = player.balance
                    self.pot += player.balance
                    player.bet(player.balance)
                    self.all_in_check()
                case 2: 
                    print(player.name + " is folding \n")
                    player.round_choice = "folded"
                    self.in_the_round.remove(player)
                    self.all_in_check()
                    self.fold_checker
            
        else:
            if(self.check_distrupted == False and self.is_preflop == False):
                choice = int(input("Do you want to check (1), raise (2), fold (3), or leave game (4) ?"))
            else: 
                choice = int(input("Do you want to call (1), raise (2), fold (3), or leave game (4) ?"))
                self.check_distrupted = True
            match choice: 
                case 1:
                    if(self.check_distrupted == False):
                        print(player.name + " has checked\n")
                        player.round_choice = "checked"
                    else:
                        print(player.name + " has called with " + str(self.last_bet) + "\n")
                        player.bet(self.last_bet)
                        self.pot += self.last_bet
                        # self.pot += self.last_bet
                        player.round_choice = "called"
                        self.all_in_check()

                case 2: 
                    player_raise = float(input("Please input your raise: "))
                    valid_raise = True
                    if((player_raise < self.last_bet) or (player.balance < player_raise)):
                        valid_raise = False
                    while(not valid_raise):
                        player_raise = float(input("Please input your raise (must be higher than last bet and can't be higher than your balance): "))
                        if(player_raise > self.last_bet and player.balance > player_raise):
                            valid_raise = True
                    if(player_raise == player.balance):
                        player.ALL_IN = True
                        self.last_bet = player_raise
                        player.bet(player_raise)
                        self.pot += player_raise
                        print(player.name + " is ALL IN!")
                        self.all_in_check()
                    else:
                        self.last_bet = player_raise
                        player.bet(player_raise)
                        self.pot += player_raise
                        print(player.name + " has raised with " + str(player_raise) + "\n")
                        
                    player.round_choice =  "raised"
                    self.check_distrupted = True
                    # self.pot += player_raise
                case 3: 
                    print(player.name + " has folded \n")
                    player.round_choice =  "folded"
                    self.in_the_round.remove(player)
                    self.all_in_check()
                    self.fold_checker

                case 4:
                    print(player.name + " has left")
                    self.player_list.remove(player)
                    self.in_the_round.remove(player)
                    self.all_in_check()
                    if(self.win_check):
                        self.announce_winner
                    
    def player_removal(self):
        """
        Checks the list of players for anybody
        who has a balance less than or equal to 
        zero. If a player is found, that player is 
        removed from the game and any money they 
        had in the pot becomes community property. 
        """
        for players in self.player_list:
            if players.balance <= 0:
                print(players.name + " has ran out of money!")
                self.player_list.remove(players)
                self.in_the_round.remove(players)
    
    def win_check(self):
        """
        Checks to see if only 1 player remains.
        If more than 1 player is still playing, 
        returns False. 
        """
        if(len(self.player_list) == 1):
            return True
        return False
    
    def all_in_check(self):
        """
        Checks the case where if everyone has declared
        an ALL IN. If case is checked, a value error is made
        and the program will jump to the final river state. 
        """
        counter = 0
        for x in self.in_the_round:
            if x.ALL_IN == True:
                counter +=1
        if(counter == len(self.in_the_round)):
            difference = 5 - len(self.river)
            for x in range(0, difference):
                self.river.append(self.deck.pop())
            raise ZeroDivisionError
        
            
        
    
    def distribute_money(self, player):
        """
        Distributes the money in the pot to the 
        winner of the round. 
        """
        player.balance += self.pot
        self.pot = 0
        for x in self.player_list:
            # x.in_pot = 0
            x.All_IN = False
        # for x in self.in_the_round:
        #     if(player.balance > x.in_pot):
        #         player.balance += x.in_pot
        #     else:
        #         player.balance += player.in_pot
            
        #     if (x != player and x.in_pot - player.in_pot <= 0):
        #         print(x.name + " has ran out of money!")
        #         self.in_the_round.remove(x)
        #         self.player_list.remove(x)
        #     if x.in_pot > 0 and x != player:
        #         x.balance += x.in_pot
        # player.balance += self.pot
        # self.pot = 0    
        # for x in self.player_list:
        #     x.in_pot = 0
        #     x.ALL_IN = False
                
    
    def libary_conversion(self, pool):
        """
        Method that converts values from the 'poker' library
        to the 'pokerlib' library.
        """
        ranks = {
        "A" : Rank.ACE,
        "2" : Rank.TWO,
        "3" : Rank.THREE,
        "4" : Rank.FOUR,
        "5" : Rank.FIVE,
        "6" : Rank.SIX,
        "7" : Rank.SEVEN,
        "8" : Rank.EIGHT,
        "9" : Rank.NINE,
        "T" : Rank.TEN,
        "J" : Rank.JACK,
        "Q" : Rank.QUEEN,
        "K" : Rank.KING
        }
        
        suits = {
        "♣" : Suit.CLUB,
        "♦" : Suit.DIAMOND,
        "♥" : Suit.HEART,
        "♠" : Suit.SPADE
        }
        
        converted_hand = []
        for cards in pool:
            converted_hand.append((ranks[str(cards.rank)], suits[str(cards.suit)]))

        return converted_hand
            
                
    
    def hand_comparison(self):
        """
        Compares the hand + river combination of every
        player whose still in the round. The highest
        value hand is declared the river. (Utilizes 
        'pokerlib' for hand comparison).
        """
        winning_player = self.in_the_round[0]
        for x in range(0, len(self.in_the_round)):
            currPlayer = HandParser(self.libary_conversion(winning_player.hand))
            # print(currPlayer)
            currPlayer += self.libary_conversion(self.river)
            nextPlayer = HandParser(self.libary_conversion(self.in_the_round[x].hand))
            # print(nextPlayer)
            nextPlayer += self.libary_conversion(self.river)
            # print(currPlayer > nextPlayer)
            if(currPlayer < nextPlayer):
                winning_player = self.in_the_round[x]
            
        return winning_player
            
            
            
    def announce_winner(self):
        """
        Announces the last remaining player as the winner and 
        distributes any remaining pot money to the player.
        """
        print("Winner of the game is: " + self.player_list[0].name + "\nPay out is: " + str(self.player_list[0].balance))
        exit()
    
    def check_bet_continue(self):
        """
        Checks if the betting round can continue based on 
        the actions of each player. If only 1 player 
        is still raising, the method will return False. 
        If people are still betting, the method will return
        True.
        """
        raised_counter = 0
        call_counter = 0
        check_counter = 0
        # folded_counter = 0
        for players in self.in_the_round:
            match players.round_choice:
                case "raised":
                    raised_counter+=1
                case "checked": 
                    check_counter+=1
                case "called":
                    call_counter+=1
        if(raised_counter == 1):
            return False
        if((call_counter + check_counter) == len(self.in_the_round)):
            return False
        return True
    
    
    def bet_ask(self):
        """
        Simulates the betting round by asking each of the players/bots
        still in the round for their moves. Also prints the total pot
        amount for that round.
        """
        print("-------------------\n" + "TOTAL POT THIS ROUND IS: " + str(self.pot) + "\n-------------------")
        while(self.check_bet_continue() == True and (len(self.in_the_round) > 1)):
            for x in self.in_the_round:
                if(type(x) == type(Bot(100))):
                    self.ask_bot(x)
                else:
                    # x.display_cards()
                    print(x.name + "'s Turn")
                    self.display_river(x)
                    self.ask_player(x)
                # self.window.close() 
                
        self.last_bet = 0
        self.check_distrupted = False
                
    def player_turn(self, player):
        """
        Special case method used for the 
        pre-flop round. Used to prevent showing 
        an empty river. 
        """
        if(type(player) == type(Bot(100))):
            self.ask_bot(player)
        else:
            player.display_cards()
            self.ask_player(player)
        # self.window.close() 
        
    def choice_wipe(self):
        """
        Wipes the move choice of everyoen in the round.
        """
        for x in self.in_the_round:
            x.round_choice = ""
        
        
    def preflop(self):
        """
        Simulates the pre-flop of the current round (Initial betting before the 
        river is drawn).
        """
        print("\n\n\n\n\n\n\n\n")
        self.choice_wipe()
        self.player_removal()
        
        if(self.win_check()):
            self.announce_winner()
            
        self.is_preflop == True #fixes the fact that you can't check during the preflop
        small_blind = self.in_the_round[0]
        big_blind = self.in_the_round[1]
        if(small_blind.balance > 2):
            small_blind.bet(2)
            self.last_bet = 2
        else:
            small_blind.ALL_IN = True
            self.last_bet = small_blind.balance
            small_blind.bet(small_blind.balance)
            print(small_blind.name + " is ALL IN!")
            small_blind.round_choice = "raised"
            self.all_in_check()
            
        self.pot += self.last_bet
        
        if(big_blind.balance > 4):
            big_blind.bet(4)
            self.last_bet = 4
        else:
            big_blind.ALL_IN = True
            self.last_bet = big_blind.balance
            big_blind.bet(big_blind.balance)
            print(big_blind.name + " is ALL IN!")
            big_blind.round_choice = "raised"
            self.all_in_check()
            
        self.pot += self.last_bet
        
        # self.pot += (.75*self.table_limit)
        self.deal_cards()
        
        for x in self.player_list:
            if(x != self.in_the_round[0] and x != self.in_the_round[1]):
                self.player_turn(x)
        self.last_bet = 0
        self.check_distrupted = False
        self.is_preflop = False
        
    # def all_in_case(self):
    #     counter = 0
    #     for x in self.in_the_round:
    #         if x.balance == 0:
    #             counter +=1
                
    #     if counter == len(self.in_the_round):
    #         self.the_river()
    
    def display_river(self, player = 0):
        """
        Displays the current river using PySimpleGUI. If a player is passed, 
        the player's hand is displayed along side the river.
        """
        imagelist = []
        #     layout = [
        #     [sg.Image("Images/" + card1 + ".png"), sg.Image("Images/" + card2 + ".png")],
        #     [sg.Button('Exit')]
        # ]#Tell window what size it needs to be 
        if player == 0: 
            for x in self.river:
                imagelist.append(sg.Image("Images/" + str(x.rank) + str(x.suit) + ".png"))
            layout = [
                [sg.Text("Current River: ")],
                imagelist,
                [sg.Button('Exit')]
            ]
        else:
            card1 = str(player.hand[0].rank) + str(player.hand[0].suit)
            card2 = str(player.hand[1].rank) + str(player.hand[1].suit)
            for x in self.river:
                imagelist.append(sg.Image("Images/" + str(x.rank) + str(x.suit) + ".png"))
            layout = [
                [sg.Text("Current River: ")],
                imagelist,
                [sg.Text(player.name + "'s Hand: ")],
                [sg.Image("Images/" + card1 + ".png"), sg.Image("Images/" + card2 + ".png")],
                [sg.Button('Exit')]
            ]
        
        window = sg.Window("river viewer", layout)
        event, value = window.read()
        while True:
            event, value = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

        window.close() 
        
        
    def flop(self):
        """
        Simulates the flop of the current round (first 3 cards).
        """
        self.choice_wipe()
        print("\n\n\n\n\n\n\n\n")
        self.deck.pop()
        self.river = [self.deck.pop() for x in range(3)]
        print("\nFLOP:")
        # self.display_river()
        print(self.river)
        print("\n")
        self.bet_ask()
        
    def the_turn(self):
        """
        Simulates the turn of the current round (first 4 cards). 
        """
        self.choice_wipe()
        print("\n\n\n\n\n\n\n\n")
        self.river.append(self.deck.pop())
        print("\nTURN: ")
        # self.display_river()
        print(self.river)
        print("\n")
        self.bet_ask()
        self.last_bet = 0
        
    
    def the_river(self):
        """
        Simulates the river of the curreent round (final river state/5 cards). 
        """
        self.choice_wipe()
        print("\n\n\n\n\n\n\n\n")
        self.river.append(self.deck.pop())
        print("\n River: ")
        print(self.river)
        print("\n")
        self.bet_ask()
        # print(str(self.hand_comparison()))
        round_winner = self.hand_comparison()
        self.distribute_money(round_winner)
        print(round_winner.name + " has the best hand")
        print("MONEY DISTRIBUTED \n")
    
    def play(self):
        """Simulates a game of Texas Hold'em poker"""
        
        while(self.win_check):
            self.player_removal()
            self.deck = random.sample(list(p.card.Card), len((list(p.card.Card))))
            for x in self.player_list:
                x.hand = []
            self.in_the_round = cp.copy(self.player_list)
            
            for x in self.player_list:
                    print(str(x) + "\n")
            try:
                #pre-flop
                self.preflop()
                
                #flop
                self.flop()
                
                #The Turn
                self.the_turn()

                #The River
                self.the_river()
                print("\n\n\n\n\n\n\n")
                
                self.round_num += 1 
            except ZeroDivisionError:
                round_winner = self.hand_comparison()
                self.distribute_money(round_winner)
                print(round_winner.name + " has the best hand")
                print("MONEY DISTRIBUTED \n")
                # for x in self.player_list:
                #     print(str(x) + "\n")
                self.player_removal()
                for x in self.player_list: 
                    x.ALL_IN = False
        for x in self.player_list:
            print(str(x) + "\n")
        # self.table_limit *= 2
        
        
# choice = 0
# while choice != 2:
#     choice = int(input(("Welcome to Poker.py! \n1: Create New Game \n2: Exit Game\n")))
#     match choice:
#         case 1:
#             playerlist = [] 
#             print("How many players (maximum 4): ")
#             playercount = int(input())
#             for x in range(0,playercount):
#                 playerlist.append(Player(input("Input player name: "), int(input("Player balance: "))))
#             if(playercount < 4):
#                 max_bot_bal = int(input("Input maximum possible bot balance: "))
#                 for b in range(0, 4 - playercount):
#                         playerlist.append(Bot(max_bot_bal))
#             game = Game(playerlist)
#             print("\n--------------\nSTARTING GAME\n--------------\n")
#             game.play()
    
# g = Bot(50, "highrisk")
# s = Player("Frank", 100)
# d = Player("David", 60)

# gam = Game([s,d])
# gam.play()