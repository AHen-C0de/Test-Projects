# Rock, Paper, Scissors Game #

# Angela Hentschel, 07.03.2021

import random


def main():
    while True:
        run_game()
        if not play_again():
            input("Bye Bye! Press ENTER to exit.")
            break
    
    
def run_game():
    print("Dear Player. Choose eigther rock, paper or scissor. The computer "
          "will do as well. It's a best-out-of-3. Good luck!")    
   
    player_win_counter = 0
    pc_win_counter = 0
   
    while pc_win_counter < 2 and player_win_counter < 2:
       pc_guess = get_pc_guess()
       player_guess = get_player_guess()
           
       win_cond = get_win_cond(pc_guess, player_guess)
       winner = get_winner(win_cond, pc_guess)
       
       print_line()
       show_choice(pc_guess, player_guess)
       print_line()
       show_win_cond(win_cond)
       print_line()
       
       if winner == "draw":
           None
       elif winner == "pc":
           print("PC won this round!")
           pc_win_counter += 1
       else:
           print("You won this round!")
           player_win_counter += 1
        
       show_point_status(pc_win_counter, player_win_counter)
       print()
   
    show_winner_of_game(pc_win_counter, player_win_counter)     

     
def print_line():
   print("--------------------")
    
    
def get_pc_guess():
    x = random.randint(1, 3)
    if x == 1:
        x = "rock"
    elif x == 2:
        x = "paper"
    else:
        x = "scissor"
    return(x)
      

def get_player_guess():
    valid_input = 0
    while valid_input == 0:
        x = input("Give your guess! Type 'rock', 'paper' or 'scissor': ")
        if x == "rock" or x == "paper" or x == "scissor":
            valid_input = 1
        else:
            print("That was neigther of the three. Try again!")
    return(x)
 
    
def get_win_cond(pc_guess, player_guess):
    # Define win conditions
    r_v_s = ("rock", "scissor")
    s_v_p = ("scissor", "paper")
    p_v_r = ("paper", "rock")
    
    if pc_guess == player_guess:
        x = "draw"
    elif (pc_guess in r_v_s) and (player_guess in r_v_s):
            x = r_v_s
    elif (pc_guess in s_v_p) and (player_guess in s_v_p):
        x = s_v_p
    else:
        x = p_v_r 

    return(x)
    

def get_winner(win_cond, pc_guess):
    if win_cond == "draw":
        return("draw")
    elif win_cond[0] == pc_guess:
        return("pc")
    else:
        return("player")
    

def show_choice(pc_guess, player_guess):   
    print(f"PC: {pc_guess}")
    print(f"You: {player_guess}")
    
    
def show_win_cond(win_cond):
    if win_cond == "draw":
        print("Draw!")
    else:
        print(f"{win_cond[0]} defeats {win_cond[1]}")

            
def show_point_status(pc_win_counter, player_win_counter):
    print(f"POINTS:  PC|{pc_win_counter}| - YOU|{player_win_counter}|")
     
        
def show_winner_of_game(pc_win_counter, player_win_counter):             
    if pc_win_counter > player_win_counter:
        print("------------------------------------------")
        print("--- Match is over! PC wins this match! ---")
        print("------------------------------------------")
    else:
        print("------------------------------------------")
        print("--- Match is over! You win this match! ---")
        print("------------------------------------------")


def play_again():
    while True:
        anwser = input("Do you want to play again? Type 'y' or 'n': ")
        if anwser == 'y':
            return True
        elif anwser == 'n':
            return False
        else:
            print("Please type 'y' or 'n'.")


   
if __name__ == "__main__":
    main() 

    


