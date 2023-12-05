import random
import poker as p
from poker import card
import names
import copy as cp
import pokerlib as pl
from pokerlib import HandParser
from pokerlib.enums import Rank, Suit
      
def goto(linenum):
    global line
    line = linenum
                
class Player: 
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = []
        self.out = False
        self.in_pot = 0.0
        self.round_choice = ""
        self.ALL_IN = False
        
    def bet(self, amt):
        self.balance -= amt
        self.in_pot += amt
        if(self.balance < 0):
            self.out = True
        
    def display_cards(self):
        print(self.name + " this is your Hand: ")
        print(self.hand)
        print("\n")
        
    def __str__(self):
        result = "Name: {name} \nCurrent Balance: {curr_bal}".format(name = self.name, curr_bal = self.balance)
        return result
        
class Bot(Player):
    def __init__(self, player_bal):
        super().__init__(names.get_first_name(), random.uniform(1, player_bal))
        

class Game:
    def __init__(self, players):
        self.deck = random.sample(list(p.card.Card), len((list(p.card.Card))))
        self.player_list = players
        self.in_the_round = cp.copy(self.player_list)
        self.poorest_bal = self.player_list[0].balance
        for x in players:
            if x.balance <= self.poorest_bal:
                self.poorest_bal = x.balance
        self.table_limit = 99999999999999999
        while(self.table_limit >= self.poorest_bal):
            print("Input table limit: ")
            self.table_limit = float(input())
        self.last_bet = 0.0
        self.all_in = False
        self.pot = 0.0
        self.raise_active = False
        self.check_distrupted = False
        self.round_num = 1
        self.is_preflop = True
        
    def deal_cards(self):
        for i in self.in_the_round:
            i.hand = [self.deck.pop() for x in range(2)]
    
    def fold_checker(self):
        counter = 0
        if len(self.in_the_round) == 1:
            raise ValueError
        
    
    def ask_player(self, player):
        """Asks player what move they want to make"""
        print("Your balance is: " + str(player.balance))
        print("Money in pot this round: " + str(player.in_pot))
        if(player.ALL_IN == True):
            return None
        elif(player.balance < self.last_bet):
            choice = float(input("do you want to all in (1) or fold (2)"))
            match choice:
                case 1:
                    print(player.name + " is going ALL IN")
                    player.ALL_IN = True
                    player.bet(self.balance)
                    self.all_in_check()
                case 2: 
                    print(player.name + " is folding \n")
                    player.round_choice = "folded"
                    self.in_the_round.remove(player)
            
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
                        print(player.name + " has called\n")
                        player.bet(self.last_bet)
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
                        player.bet(player_raise)
                        print(player.name + " is ALL IN!")
                        self.all_in_check()
                    else:
                        player.bet(player_raise)
                        print(player.name + " has raised\n")
                    player.round_choice =  "raised"
                    self.check_distrupted = True
                    # self.pot += player_raise
                case 3: 
                    print(player.name + " has folded \n")
                    player.round_choice =  "folded"
                    self.pot += player.in_pot
                    player.in_pot = 0.0
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
        for players in self.player_list:
            if players.balance <= 0:
                print(players.name + "has run out of money!")
                self.player_list.remove(players)
    
    def win_check(self):
        if(len(self.player_list) == 1):
            return True
        return False
    
    def all_in_check(self):
        counter = 0
        for x in self.in_the_round:
            if x.ALL_IN == True:
                counter +=1
        if(counter == len(self.in_the_round)):
            difference = 5 - len(self.river)
            for x in range(0, difference):
                self.river.append(self.deck.pop())
            raise ValueError
        
            
        
    
    def distribute_money(self, player):
        for x in self.player_list:
            player.balance += x.in_pot
            player.balance += self.pot
            self.pot = 0.0
            if (x != player and x.in_pot - player.in_pot <= 0 and x.balance == 0 ):
                print(x.name + " has ran out of money!")
                self.player_list.remove(x)
        for x in self.player_list:
            x.in_pot = 0.0
            x.ALL_IN = False
                
    
    def libary_conversion(self, pool):
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
        # self.player_list[0].balance += self.pot
        print("Winner of the game is: " + self.player_list[0].name + "\nPay out is: " + str(self.player_list[0].balance))
        exit()
    
    def check_bet_continue(self):
        raised_counter = 0
        call_counter = 0
        check_counter = 0
        folded_counter = 0
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
        while(self.check_bet_continue() == True and (len(self.in_the_round) > 1)):
            for x in self.in_the_round:
                x.display_cards()
                self.ask_player(x)
                
            self.last_bet = 0
            self.check_distrupted = False
                
    def player_turn(self, player):
        player.display_cards()
        self.ask_player(player)
        
    def choice_wipe(self):
        for x in self.in_the_round:
            x.round_choice = ""
        
          
    def preflop(self):
        print("\n\n\n\n\n\n\n\n")
        self.choice_wipe()
        self.player_removal()
        
        if(self.win_check()):
            self.announce_winner()
            
        self.is_preflop == True
        self.in_the_round[0].bet(self.table_limit/4)
        self.in_the_round[1].bet(self.table_limit/2)
        self.in_the_round[0].round_choice = "raised"
        self.in_the_round[1].round_choice = "raised"
        self.last_bet = self.table_limit/2
        # self.pot += (.75*self.table_limit)
        self.deal_cards()
        for x in range(2, len(self.in_the_round)):
            self.player_turn(self.in_the_round[x])
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
            
        
    def flop(self):
        self.choice_wipe()
        print("\n\n\n\n\n\n\n\n")
        self.deck.pop()
        self.river = [self.deck.pop() for x in range(3)]
        print("\nFLOP:")
        print(self.river)
        print("\n")
        self.bet_ask()
        
    def the_turn(self):
        self.choice_wipe()
        print("\n\n\n\n\n\n\n\n")
        self.river.append(self.deck.pop())
        print("\nTURN: ")
        print(self.river)
        print("\n")
        self.bet_ask()
        
    
    def the_river(self):
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
    
    def play_round(self):
         self.in_the_round = cp.copy(self.player_list)
         self.preflop()
         self.flop()
         self.the_turn()
         self.theriver()
         for x in self.player_list:
            print(str(x) + "\n")
    
    def play(self):
        """Simulates a game of Texas Hold'em poker"""
        
        while(self.win_check):
            self.in_the_round = cp.copy(self.player_list)
            # ##preflop##
            
            try:
                self.preflop()
                
                # ##flop##
                self.flop()
                
                # ##The Turn##
                self.the_turn()
                # # self.deck.pop()
                # # self.river.append(self.deck.pop())
                # # print("\nTURN: ")
                # # print(self.river)
                # # print("\n")
                
                #The River
                self.the_river()
                print("\n\n\n\n\n\n\n")
                for x in self.player_list:
                    print(str(x) + "\n")
                
                self.round_num += 1 
            except ValueError:
                round_winner = self.hand_comparison()
                self.distribute_money(round_winner)
                print(round_winner.name + " has the best hand")
                print("MONEY DISTRIBUTED \n")
                for x in self.player_list:
                    print(str(x) + "\n")
                self.player_removal()
        # self.table_limit *= 2
        
        
    

g = Player("steven", 50)

s = Player("Frank", 100)
d = Player("David", 60)

gam = Game([g,s,d])
gam.play()

# gam.river = [p.Card('J♠'), p.Card('7♠'), p.Card('8♦'), p.Card('4♠'), p.Card('4♦')]
# # gam.player_list[0].hand = [p.Card('5♥'), p.Card('7♣')]
# # gam.player_list[1].hand = [p.Card('J♥'), p.Card('A♥')]
# # gam.player_list[2].hand = [p.Card('7♦'), p.Card('Q♣')]

# # hand1 = HandParser(gam.libary_conversion(gam.player_list[0].hand))
# # hand2 = HandParser(gam.libary_conversion(gam.player_list[1].hand))
# # hand1 += gam.libary_conversion(gam.river)
# # hand2 += gam.libary_conversion(gam.river)
# # print(hand1 < hand2)
# gam.deal_cards()
# print("Board: " + str(gam.river) + "\n")
# for x in gam.in_the_round:
#     x.display_cards()
    
# print(str(gam.hand_comparison()))

# hand1 = HandParser([
#     (Rank.FIVE, Suit.HEART),
#     (Rank.SEVEN, Suit.CLUB)
# ])
# hand2 = HandParser([
#     (Rank.JACK, Suit.HEART),
#     (Rank.ACE, Suit.HEART)
# ])
# hand3 = HandParser([
#     (Rank.SEVEN, Suit.DIAMOND),
#     (Rank.QUEEN, Suit.CLUB)
# ])

# board = [
#     (Rank.JACK, Suit.SPADE),
#     (Rank.SEVEN, Suit.SPADE),
#     (Rank.EIGHT, Suit.DIAMOND),
#     (Rank.FOUR, Suit.SPADE),
#     (Rank.FOUR, Suit.DIAMOND)
# ]

# hand1 += board
# hand2 += board
# hand3 += board

# print(hand1 > hand2)

# Board: [Card('J♠'), Card('7♠'), Card('8♦'), Card('4♠'), Card('4♦')]

# steven this is your Hand: 
# [Card('5♥'), Card('7♣')]


# Frank this is your Hand: 
# [Card('J♥'), Card('A♥')]


# David this is your Hand: 
# [Card('7♦'), Card('Q♣')]


# Name: steven 
# Current Balance: 50