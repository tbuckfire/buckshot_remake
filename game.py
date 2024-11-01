# game.py

from player import Player
import random

class Game:
    def __init__(self, health, total_ammo, bullets, player_name, opponent_name, mode):
        self.health = health
        self.total_ammo = total_ammo
        self.remaining_ammo = total_ammo
        self.round = 1
        self.total_bullets = bullets
        self.remaining_bullets = bullets
        self.player_name = player_name
        self.opponent_name = opponent_name
        self.mode = mode
        self.damage_per_shot = 1
        self.magezine = self.load_ammo()
        self.num_possible_items = 5
        
        if mode == 1:
            self.player1 = Player(name=player_name, health=self.health)
            self.player2 = Player(name=opponent_name, health=self.health)
        else:
            self.player1 = Player(name=player_name, health=self.health)
            self.player2 = Player(name=opponent_name, health=self.health)

    def load_ammo(self):
        """Load ammo with a mix of 'live' and 'blank' shells based on ammo count."""
        print(f"Reloading the shotgun, there are {self.total_ammo} slots with {self.total_bullets} bullets.")
        magezine = ["live"] * (self.total_bullets) + ["blank"] * (self.total_ammo - self.total_bullets)
        self.remaining_bullets = self.total_bullets
        self.remaining_ammo = self.total_ammo
        random.shuffle(magezine)
        return magezine

    def player_choice(self):
        """Prompt the player to choose an action."""
        while True:
            choice = input("Shoot yourself or the opponent, or use an item: ").strip().lower()
            if choice in ["self", "opponent", "inventory", "beer", "cigarette", "handcuff", "handsaw", "magnifying_glass", "health", "ammo", "help"]:
                return choice
            print("Invalid choice. Please type a proper command. You can type help for a list of valid commands.")

    def give_items(self):
        if self.round == 1:
            return
        elif self.round == 2:
            num_items = 2
        else:
            num_items = 4
        possible_items = ["beer", "cigarette", "handcuff", "handsaw", "magnifying_glass"]

        # For player 1
        items_to_give = num_items
        if self.player1.inventory_count + items_to_give > 6:
            items_to_give = 6 - self.player1.inventory_count

        items_given = random.sample(possible_items, items_to_give)
        for item in items_given:
            self.player1.add_item(item)

        self.player1.inventory_count += items_to_give
        print(f"Round {self.round}: {self.player1.name} received items {items_given}. Current inventory count: {self.player1.inventory_count}")

        # For player 2
        items_to_give = num_items
        if self.player2.inventory_count + items_to_give > 6:
            items_to_give = 6 - self.player2.inventory_count

        items_given = random.sample(possible_items, items_to_give)
        for item in items_given:
            self.player2.add_item(item)

        self.player2.inventory_count += items_to_give
        print(f"Round {self.round}: {self.player2.name} received items {items_given}. Current inventory count: {self.player2.inventory_count}")

        
    def take_turn(self, player_num):
        """Handle one turn where the player chooses to shoot themselves or the opponent."""
        choice = self.player_choice()
        if self.remaining_bullets == 0 or self.remaining_ammo == 0:
            self.magezine = self.load_ammo()
        if choice == "help":
            self.help()
        elif choice == "beer" or choice == "cigarette" or choice == "handcuff" or choice == "handsaw" or choice == "magnifying_glass":
            self.use_item(choice, player_num)
        elif choice == "inventory":
            self.inventory(player_num)
        elif choice == "health":
            self.health_check()
        elif choice == "ammo":
            self.ammo()
        elif choice == "self":
            self.shoot_self(player_num)
        elif choice == "opponent":
            self.shoot_opponent(player_num)



    def play(self):
        """Run the main game loop."""
        while self.player1.health > 0 and self.player2.health > 0:
            if self.remaining_bullets == 0 or self.remaining_ammo == 0:
                self.magezine = self.load_ammo()
            print(f"\n--- Round {self.round} ---")
            self.give_items()
            self.player1.turn_over = False
            self.player2.turn_over = False
            temp_damage = self.damage_per_shot

            print(f"{self.player1.name}'s turn.")
            while self.player1.turn_over == False:
                self.take_turn(1)
            self.damage_per_shot = temp_damage #set the damage back to proper amount in case of handsaw
            player_won = self.check_game_over() # returns the player who won or 0 if still continuing
            if player_won != 0:
                break

            print(f"{self.player2.name}'s turn.")
            while self.player2.turn_over == False:
                self.take_turn(2)
            self.damage_per_shot = temp_damage #set the damage back to proper amount in case of handsaw
            player_won = self.check_game_over() # returns the player who won or 0 if still continuing
            if player_won != 0:
                break

            self.round += 1
            self.damage_per_shot += 1
            self.health_check()
        
        if player_won == 1:
            print(f"{self.player1.name} has won buckshot roulette!!!")
        elif player_won == 2:
            print(f"{self.player2.name} has won buckshot roulette!!!")
        
    def help(self):
        print("Here are the following commands you can type:")
        print("self: shoot the gun at yourself")
        print("opponent: shoot the gun at the opponent")
        print("inventory: see available items in inventory")
        print("beer: drink a beer can ejecting the current round")
        print("cigarette: smoke a cigarette which restores one shot worth of health")
        print("handcuff: put handcuffs on your opponent skipping their turn")
        print("handsaw: use handsaw to cut shotgun into sawed-off shotgun, next shot double damage")
        print("magnifying_glass: use magnifying glass to reveal next shell")
        print("health: print how much health each player has")
        print("ammo: print how many total bullets and blanks remain")
        print("quit: quit the game")

    def use_item(self, choice, player_num):
        if player_num == 1:
            self.player1.use_item(choice)
        else:
            self.player2.use_item(choice)

        if choice == "beer":
            current_bullet = self.magezine[0]
            self.remaining_ammo -= 1
            if current_bullet == "live":
                self.remaining_bullets -= 1
                self.magezine.pop(0)
                print("A live bullet was removed from the gun!")
            else:
                self.magezine.pop(0)
                print("A blank was removed from the gun!")
        elif choice == "cigarette":
            if player_num == 1:
                self.player1.health += self.damage_per_shot
                print(f"{self.player1.name} smoked a cigarette and increased their health by {self.damage_per_shot}")
            else:
                self.player2.health += self.damage_per_shot
                print(f"{self.player2.name} smoked a cigarette and increased their health by {self.damage_per_shot}")
        elif choice == "handcuff":
            return
        elif choice == "handsaw":
            self.damage_per_shot *= 2
            print("The next shot is double damage!")
        elif choice == "magnifying_glass":
            current_bullet = self.magezine[0]
            if current_bullet == "live":
                print("A live bullet is next in the chamber!")
            else:
                print("A blank is next in the chamber!")
        if self.remaining_bullets == 0 or self.remaining_ammo == 0:
            self.magezine = self.load_ammo()
    
    def ammo(self):
        print(f"The gun has {self.remaining_ammo} remaining shots with {self.remaining_bullets} remaining live rounds.")

    def health_check(self):
        print(f"{self.player1.name} Health: {self.player1.health} | {self.player2.name} Health: {self.player2.health}")
        
    def inventory(self, player_num):
        if player_num == 1:
            print(f"{self.player1.name} has the following inventory: {self.player1.inventory}")
        elif player_num == 2:
            print(f"{self.player2.name} has the following inventory: {self.player2.inventory}")

    def shoot_self(self, player_num):
        self.remaining_bullets -= 1
        self.remaining_ammo -= 1
        if player_num == 1:
            self.player1.turn_over = True
            current_bullet = self.magezine.pop(0)
            if current_bullet == "live":
                print(f"{self.player1.name} shot themselves with a live round!")
                self.player1.take_damage(self.damage_per_shot)
            elif current_bullet == "live":
                print(f"{self.player1.name} shot themselves with a blank!")
        elif player_num == 2:
            self.player2.turn_over = True
            current_bullet = self.magezine.pop(0)
            if current_bullet == "live":
                print(f"{self.player2.name} shot themselves with a live round!")
                self.player1.take_damage(self.damage_per_shot)
            elif current_bullet == "live":
                print(f"{self.player2.name} shot themselves with a blank!")
        if self.remaining_bullets == 0 or self.remaining_ammo == 0:
            self.magezine = self.load_ammo()
    
    def shoot_opponent(self, player_num):
        self.remaining_bullets -= 1
        self.remaining_ammo -= 1
        if player_num == 1:
            self.player1.turn_over = True
            current_bullet = self.magezine.pop(0)
            if current_bullet == "live":
                print(f"{self.player1.name} shot {self.player2.name} with a live round!")
                self.player2.take_damage(self.damage_per_shot)
            elif current_bullet == "blank":
                print(f"{self.player1.name} shot {self.player2.name} with a blank!")
        elif player_num == 2:
            self.player2.turn_over = True
            current_bullet = self.magezine.pop(0)
            if current_bullet == "live":
                print(f"{self.player2.name} shot {self.player1.name} with a live round!")
                self.player1.take_damage(self.damage_per_shot)
            elif current_bullet == "blank":
                print(f"{self.player2.name} shot {self.player1.name} with a blank!")
        if self.remaining_bullets == 0 or self.remaining_ammo == 0:
            self.magezine = self.load_ammo()

    def check_game_over(self):
        if self.player1.health <= 0:
            return 2
        elif self.player2.health <= 0:
            return 1
        else:
            return 0
    
    
