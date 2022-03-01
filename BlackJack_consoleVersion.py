# Black Jack, die II.
# 08.08.2021


from enum import Enum
from typing import NamedTuple
import itertools as itt
import random
from time import perf_counter # records in seconds
from pathlib import Path 
import json


class Type(Enum):
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    
class Color(Enum):
    Diamonds = 1
    Clubs = 2
    Hearts = 3
    Spades = 4

class Card(NamedTuple):
    type: Type
    color: Color

class RoundResult(Enum):
    win = 0
    loss = 1


def main():
    print("This is Black Jack. Good Luck!")
    
    balance = 50
    all_bet_RTs, all_hands, all_card_RTs = [], [], []

    while True:
        outcome, balance, bet_RT, card_RTs, final_hand = run_round(balance)
        all_bet_RTs.append(bet_RT)
        all_card_RTs.append(card_RTs)
        all_hands.append(final_hand)
        display_outcome(outcome, balance)
        if not wanna_play_again(balance):
            break
    save_results(all_bet_RTs, all_card_RTs, all_hands)


def run_round(balance):
    card_RTs = []
    hand, ace_val = [], []
    
    print('\n- NEW ROUND -')
    
    deck = init_deck()
    bet, bet_RT = get_player_bet(balance) 
    for i in range(2):
        hand, deck, ace_val, hand_value = draw_card_player(hand, deck, ace_val) 
    
    display_hand(hand, hand_value)
    result = check_player_hand(hand_value)

    while result is None:
        decision, RT = player_wants_another_card()
        card_RTs.append(RT)
        if decision:
            hand, deck, ace_val, hand_value = draw_card_player(hand, deck, ace_val)
        else:
            break

        display_hand(hand, hand_value)
        res = check_player_hand(hand_value)
         
        if res is not None:
            return res, adjust_balance(balance, res, bet), bet_RT, card_RTs, hand
    
    pc_hand = get_pc_hand(deck)
    display_pc_value(pc_hand)
    
    res = check_winner(hand_value, pc_hand)
    
    return res, adjust_balance(balance, res, bet), bet_RT, card_RTs, hand


def init_deck():
    deck = [Card(type, color) for type, color in itt.product(Type, Color)]
    random.shuffle(deck)
    return deck


def draw_card_player(hand, deck, ace_val):
    valid = 0
    hand.append(deck.pop())
    
    # player chooses Ace value
    if hand[-1].type.name in {'Ace'}:
        while valid == 0:
            try:
                val = int(input('Ace! Choose value 1 or 11: '))
                if val in (1,11):
                    ace_val.append(val)
                    valid = 1
                else:
                    print('Only 1 or 11!')
            except ValueError:
                print('Give integer!')
        pass
    
    hand_value = get_value(hand, ace_val)
    
    return hand, deck, ace_val, hand_value


def get_player_bet(balance):
    valid = 0
    print('You have', balance, 'chips.')
    while valid == 0:
        try:
            rt_start = perf_counter() # record rt start 
            bet = int(input("How much do you want to bet this round? "))
            rt_stop = perf_counter() # record rt stop
            bet_rt = rt_stop - rt_start
            
            if bet > balance:
                print("You have not enough chips!")
            elif bet < 0:
                print("That's nonsense!")
            elif bet == 0:
                print("You must bet something!")
            else:
                valid = 1
        except ValueError:
            print("Give integer!")
    return bet, bet_rt


def display_hand(hand, hand_value):
    print("\nYour hand:\n---")
    for card in hand:
        print(card.color.name, ',', card.type.name)
    print("---")
    print("You have ", hand_value, " in your hand.")


def get_value(hand, ace_val = None):
    if ace_val == None:
        ace_val = []
        # do not set ace_val = [] as default value in func, because it creates 
        # a permanent variable which is changed every time func is called !        
    ace_v = ace_val.copy() # use copy, otherwise .append() will change ace_val outside function
    card_val = []
    
    for i,card in enumerate(hand):
        if card.type.name in {'Jack','Queen','King'}:
            card_val.append(10)     
        else:
            # check if 'ace_val' is empty to distinguish between player & pc
            if ace_v != [] and card.type.name in 'Ace':
                card_val.append(ace_v.pop(0))
            else:
                card_val.append(card.type.value)
    hand_val = sum(card_val)   
    return hand_val


def player_wants_another_card():
    valid = 0 
    dec = None
    
    while valid == 0: 
        print("Do you want to draw another card?")

        rt_start = perf_counter() 
        answer = input("'y' (yes) or 'n' (no): ")
        rt_stop = perf_counter() 
  
        if answer == 'y':
            dec = True
            valid = 1
        elif answer == 'n':
            dec = False
            valid = 1
        else: 
            print("Please type 'y' or 'n'.")
    
    rt = rt_stop - rt_start
    return dec, rt      
            

def check_player_hand(hand_value):
    if hand_value == 21:
        return RoundResult.win
    elif hand_value > 21:
        return RoundResult.loss
    else:
        return None
 
  
def get_pc_hand(deck):
    decide = random.randint(1,2)
    hand_pc = [deck.pop() for i in range(2)]
    while True:
        cards_val = get_value(hand_pc)
        if cards_val <= 16:
           hand_pc.append(deck.pop())
        elif cards_val == 17:
            if decide == 1:
                break
            else:
                hand_pc.append(deck.pop())
        else:
            break
    return hand_pc
  

def check_winner(hand_value, pc_hand):
    pc_hand_value = get_value(pc_hand)   
    
    if hand_value <= pc_hand_value <= 21:
        return RoundResult.loss
    else:
        return RoundResult.win


def display_pc_value(pc_hand):
    pc_val = get_value(pc_hand)
    print("PC has ", pc_val, ".", sep='')


def adjust_balance(balance, res, bet):
    if res.name == 'win':
        balance += bet
    else:
        balance -= bet
    return balance
    

def wanna_play_again(balance):
    if balance == 0:
        input("You're broke. Game over!\nPress ENTER to exit.")
        return False
    else:
        while True:
            anwser = input("Do you want to play again? Type 'y' or 'n': ")
            if anwser == 'y':
                return True
            elif anwser == 'n':
                return False
            else:
                print("Please type 'y' or 'n'.")


def display_outcome(outcome, balance):
    if outcome.name == 'win':
        print('\nYou win!')
    else:
        print('\nYou lose!')
    print('New balance:', balance, 'chips')
      
            
def save_results(all_bet_RTs, all_card_RTs, all_hands):
    Path('bj_results.txt').write_text(json.dumps([{'bet_RT': all_bet_RTs, 
                                                   'card_RT': all_card_RTs, 
                                                   'hand': str(all_hands)}]))




if __name__ == "__main__":
    main()