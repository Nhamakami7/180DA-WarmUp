import random

def get_user_input():
    user_move = input('Play either "rock", "paper", or "scissors"\n')
    while user_move not in ["rock", "paper", "scissors"]:
        print('invalid move')
        user_move = input('Play either "rock", "paper", or "scissors"\n')
    return user_move

def get_ai_input():
    moves = ["rock", "paper", "scissors"]
    ai_move = random.choice(moves)
    return ai_move

def get_winner(user_input, ai_input, second_user=None):
    if user_input == ai_input:
        return "TIE"
    elif ((user_input == "rock" and ai_input == "scissors") or 
          (user_input == "paper" and ai_input == "rock") or 
          (user_input == "scissors" and ai_input == "paper")):
        return "PLAYER1 WIN"
    elif second_user is not None:
        return "PLAYER2 WIN"
    else:
        return "AI WIN"

if __name__ == "__main__":
    while True:
        user_input = get_user_input()
        ai_input = get_ai_input()
        
        print(f"User played {user_input} and AI played {ai_input}")
        print(get_winner(user_input, ai_input))

        play_again = input('Play again? "Y" or "N"\n')
        if play_again == 'Y':
            continue
        else:
            break

        
