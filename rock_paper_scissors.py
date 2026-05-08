"""
Create a Rock Paper Scissors game where the player inputs their choice
and plays  against a computer that randomly selects its move, 
with the game showing who won each round.
Add a score counter that tracks player and computer wins, 
and allow the game to continue until the player types “quit”.
"""
import random

# Initialize score counters
player_wins = 0
computer_wins = 0

# Define the choices
choices = ['rock', 'paper', 'scissors']

# Game loop
while True:
    # Get player's choice
    player_choice = input("Enter your choice (rock, paper, scissors) or 'quit' to exit: ").lower()

    # Check if player wants to quit
    if player_choice == 'quit':
        break

    # Validate player's choice
    if player_choice not in choices:
        print("Invalid choice. Please enter rock, paper, or scissors.")
        continue

    # Generate computer's choice
    computer_choice = random.choice(choices)

    # Determine the winner
    if player_choice == computer_choice:
        print(f"Both players selected {player_choice}. It's a tie!")
    elif (player_choice == "rock" and computer_choice == "scissors") or \
         (player_choice == "paper" and computer_choice == "rock") or \
         (player_choice == "scissors" and computer_choice == "paper"):
        print(f"You chose {player_choice}, computer chose {computer_choice}. You win!")
        player_wins += 1
    else:
        print(f"You chose {player_choice}, computer chose {computer_choice}. Computer wins!")
        computer_wins += 1

# Display final scores
print(f"\nFinal Scores:")
print(f"Player: {player_wins}")
print(f"Computer: {computer_wins}\n")