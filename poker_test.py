import unittest
import POKER as p
from POKER import Game

class pokertester(unittest.TestCase):
    @staticmethod
    def game_creation(amt=100):
        return Game([p.Player("Steven", amt), p.Player("David", amt), p.Player("Frank", amt)])
    
    def test_card_dealing(self):
        g = pokertester.game_creation()
        g.deal_cards()
        self.assertEqual(len(g.in_the_round[0].hand), 2)
        
    def test_player_removal(self):
        g = pokertester.game_creation()
        g.player_list[0].balance = 0
        g.player_removal()
        self.assertEqual(len(g.player_list), 2)
        
    def test_all_in_check(self):
        g = pokertester.game_creation()
        for x in g.player_list:
            x.ALL_IN = True
        AssertionError(g.all_in_check, ZeroDivisionError)
    
    def test_choice_wipe(self):
        g = pokertester.game_creation()
        g.player_list[0].round_choice = "raised"
        g.choice_wipe()
        self.assertEqual(g.player_list[0].round_choice, "")
        
    def test_bet(self):
        g = pokertester.game_creation()
        g.player_list[0].bet(30)
        self.assertEqual(g.player_list[0].balance, 70)
        
        
if __name__ == '__main__':
    unittest.main()

        