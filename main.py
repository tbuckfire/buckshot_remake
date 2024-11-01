# main.py

from game import Game
from player import Player

def get_game_mode():
    """Prompt the user to choose the game mode."""
    while True:
        mode = input("Choose game mode: (1) Player vs Player, (2) Player vs Bot: ").strip()
        if mode == "":
            return "1"
        if mode in ["1", "2"]:
            return mode
        print("Invalid choice. Please enter 1 or 2.")

def get_player_names(mode):
    """Collect names based on the chosen mode."""
    player_name = input("Enter the name for Player 1: ").strip()
    if mode == "1":
        opponent_name = input("Enter the name for Player 2: ").strip()
    else:
        opponent_name = "Dealer"
    if player_name == "" and opponent_name == "":
        player_name = "Player 1"
        opponent_name = "Player 2"
    if player_name == "":
        player_name = "Player" 
    return player_name, opponent_name

def get_custom_settings():
    """Ask the user if they want custom settings and collect them if yes."""
    use_custom = input("Do you want to customize game settings? (yes/no): ").strip().lower()
    if use_custom == "yes":
        health = int(input("Enter starting health for both players (default is 5): ").strip())
        ammo = int(input("Enter total ammo amount (default is 8): ").strip())
        bullets = int(input("Enter the number of bullets to be loaded (default is 4): ").strip())
        return health, ammo, bullets 
    else:
        # Return default settings
        return 5, 8, 4

def main():
    print("Welcome to Buckshot Roulette!")
    mode = get_game_mode()
    
    # Get player names
    player_name, opponent_name = get_player_names(mode)
    
    # Collect custom settings if desired
    health, ammo, bullets = get_custom_settings()

    # Initialize and start the game with the chosen settings
    print(f"\nStarting game between {player_name} and {opponent_name}...")
    game = Game(
        health=health,
        total_ammo=ammo,
        bullets=bullets,
        player_name=player_name,
        opponent_name=opponent_name,
        mode=mode,
    )
    
    game.play()

if __name__ == "__main__":
    main()
