import random

def play_game():
    choices = ["rock", "paper", "scissors"]
    
    while True:
        # Get player's choice
        player = input("Choose rock, paper, or scissors (or 'quit' to exit): ").lower()
        
        if player == 'quit':
            print("Thanks for playing!")
            break
            
        if player not in choices:
            print("Invalid choice. Please try again.")
            continue
        
        # Get computer's choice
        computer = random.choice(choices)
        print(f"Computer chose: {computer}")
        
        # Determine winner
        if player == computer:
            print("It's a tie!")
        elif (player == "rock" and computer == "scissors") or \
             (player == "paper" and computer == "rock") or \
             (player == "scissors" and computer == "paper"):
            print("You win!")
        else:
            print("Computer wins!")
        print()

if __name__ == "__main__":
    print("Welcome to Rock, Paper, Scissors!")
    play_game()