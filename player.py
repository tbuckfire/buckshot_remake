

class Player:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.inventory = {
            "beer": 0,
            "cigarette": 0,
            "handcuff": 0,
            "handsaw": 0,
            "magnifying_glass": 0
        }
        self.inventory_count = 0
        self.turn_over = True
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health > 0
    
    def add_item(self, item):
        self.inventory[item] += 1
    
    def use_item(self, item):
        if self.inventory.get(item, 0) > 0:
            self.inventory[item] -= 1
            return True
        return False
    
    # class Dealer(Player):
    #     pass