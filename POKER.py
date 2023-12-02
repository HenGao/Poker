import random
import poker as p
import names
import copy as cp
      
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
        
    def bet(self, amt):
        self.balance -= amt
        self.in_pot += amt
        if(self.balance < 0):
            self.out = True
        
    def display_cards(self):
        print(self.name + " this is your Hand: ")
        print(self.hand)
        print("\n")
        
class Bot(Player):
    def __init__(self, player_bal):
        super().__init__(names.get_first_name(), random.uniform(1, player_bal))
        

class Game:
    def __init__(self, players):
        self.deck = random.sample(list(p.card.Card), len((list(p.card.Card))))
        self.player_list = players
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
        self.pot = 0
        self.raise_active = False
        
    def deal_cards(self):
        for i in self.player_list:
            i.hand = [self.deck.pop() for x in range(2)]
    
    
    def ask_player(self,player):
        """Asks player what move they want to make"""
        if(player.balance < self.last_bet):
            choice = input("do you want to all in (1) or fold (2)")
            
        else:
            choice = int(input("Do you want to call (1), raise (2), fold (3), or leave game (4) ?"))
            match choice: 
                case 1:
                    player.bet(self.last_bet)
                    self.pot += self.last_bet
                    player.round_choice = "called"
                case 2: 
                    player_raise = float(input("Please input your raise (must be higher than last bet): "))
                    while(player_raise <= self.last_bet):
                        player_raise = float(input("Please input your raise (must be higher than last bet): "))
                    player.bet(player_raise)
                    player.round_choice =  "raised"
                    # self.pot += player_raise
                case 3: 
                    print("Folding \n")
                    player.round_choice =  "folded"
                case 4:
                    self.player_list.remove(player)
                    print(player.name + " has left")
                    
    def player_removal(self):
        for players in self.player_list:
            if players.balance <= 0:
                self.player_list.remove(players)
    
    def win_check(self):
        if(len(self.player_list) == 1):
            return True
        else: 
            return False
        
    
    def distribute_money(self, player):
        for x in self.player_list:
            player.balance += x.in_pot
        for x in self.player_list:
            if x.in_pot - player.in_pot < 0 and x.round_choice != "folded":
                self.player_list.remove(x``)
                
                
    
    def hand_comparison(self):
        return None
    
    def announce_winner(self):
        print("Winner of the game is: " + self.player_list[0].name + "\nPay out is: " + str(self.player_list[0].balance))
        exit()
    
    
    def player_turn(self, player):
        player.display_cards()
        self.ask_player(player)
        if player.round_choice == "folded":
            self.in_the_round.remove(player)
        
        
    def preflop(self):
            
        self.player_removal()
            
        self.in_the_round[0].bet(self.table_limit/4)
        self.in_the_round[1].bet(self.table_limit/2)
        self.in_the_round[0].round_choice = "raised"
        self.in_the_round[1].round_choice = "raised"
        self.last_bet = self.table_limit/2
        self.pot += (.75*self.table_limit)
        self.deal_cards()
        for x in range(2, len(self.in_the_round)):
            self.player_turn(self.in_the_round[x])
    
        
        
        
    def flop(self):
        self.deck.pop()
        self.river = [self.deck.pop() for x in range(3)]
        print("\nFLOP:")
        print(self.river)
        print("\n")
        
        for players in self.in_the_round:
            self.player_turn(players)
        
    def the_turn(self):
        return None
        
    def river(self):
        return None
    
    
    def play(self):
        """Simulates a game of Texas Hold'em poker"""
        
        while(not self.win_check):
            
            self.in_the_round = cp.deepcopy(self.player_list)
            ##preflop##
            self.preflop()
            
            ##flop##
            self.flop()
            
            
            
            ##The Turn##
            self.deck.pop()
            self.river.append(self.deck.pop())
            print("\nTURN: ")
            print(self.river)
            print("\n")
            
            #The River
            
            self.in_the_round = {x:None for x in self.player_list}
            self.table_limit *= 2
        
        
    

g = Player("steven", 50)

s = Player("Frank", 100)
d = Player("David", 60)

gam = Game([g,s,d ])
gam.play()