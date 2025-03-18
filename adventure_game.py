# Simple Text Adventure Game
import time
import random

# Game state
inventory = []
health = 100
current_location = "forest_entrance"

# Game locations and their descriptions
locations = {
    "forest_entrance": {
        "description": "You stand at the entrance of a dark, mysterious forest. Paths lead north and east.",
        "exits": {"north": "clearing", "east": "river"},
    },
    "clearing": {
        "description": "A sunny clearing in the forest. You see a small wooden chest here.",
        "exits": {"south": "forest_entrance", "east": "cave_entrance"},
        "items": ["ancient_key"]
    },
    "river": {
        "description": "A rushing river blocks your path. A rickety bridge crosses to the west.",
        "exits": {"west": "forest_entrance", "north": "cave_entrance"},
    },
    "cave_entrance": {
        "description": "A dark cave looms before you. It looks dangerous but potentially rewarding.",
        "exits": {"west": "clearing", "south": "river", "inside": "treasure_room"},
        "enemy": {"name": "Forest Troll", "damage": 20, "health": 30}
    },
    "treasure_room": {
        "description": "A glittering room filled with treasure! You've reached your goal.",
        "exits": {"outside": "cave_entrance"},
        "items": ["golden_crown", "magic_jewel"],
        "locked": True
    }
}

def display_location():
    """Display current location description and available exits"""
    location = locations[current_location]
    print("\n" + "=" * 50)
    print(location["description"])
    
    # Display available exits
    exits = location["exits"]
    print("\nExits:", ", ".join(exits.keys()))
    
    # Display items if present
    if "items" in location and location["items"]:
        print("\nYou see:", ", ".join(location["items"]))
    
    # Display enemies if present
    if "enemy" in location:
        print(f"\nBeware! A {location['enemy']['name']} is here!")

def get_command():
    """Get user input and process it"""
    command = input("\n> What would you like to do? ").lower().split()
    
    if not command:
        print("Please enter a command.")
        return
    
    action = command[0]
    
    if action == "go" and len(command) > 1:
        move_player(command[1])
    elif action == "look":
        display_location()
    elif action == "take" and len(command) > 1:
        take_item(" ".join(command[1:]))
    elif action == "inventory" or action == "i":
        show_inventory()
    elif action == "use" and len(command) > 1:
        use_item(" ".join(command[1:]))
    elif action == "fight":
        fight_enemy()
    elif action == "help":
        show_help()
    elif action == "quit" or action == "exit":
        return False
    else:
        print("I don't understand that command. Type 'help' for a list of commands.")
    
    return True

def move_player(direction):
    """Move player to a new location"""
    global current_location
    
    location = locations[current_location]
    
    if direction in location["exits"]:
        new_location = location["exits"][direction]
        
        # Check if location is locked
        if locations[new_location].get("locked", False):
            if "ancient_key" in inventory:
                print("You use the ancient key to unlock the door.")
                current_location = new_location
            else:
                print("This area is locked. You need a key.")
        else:
            current_location = new_location
            display_location()
    else:
        print(f"You can't go {direction} from here.")

def take_item(item):
    """Add an item to player's inventory"""
    location = locations[current_location]
    
    if "items" in location and item in location["items"]:
        inventory.append(item)
        location["items"].remove(item)
        print(f"You picked up the {item}.")
    else:
        print(f"There's no {item} here.")

def show_inventory():
    """Display the player's inventory"""
    if inventory:
        print("\nInventory:")
        for item in inventory:
            print(f"- {item}")
    else:
        print("\nYour inventory is empty.")

def use_item(item):
    """Use an item from inventory"""
    if item not in inventory:
        print(f"You don't have a {item}.")
        return
    
    if item == "ancient_key" and current_location == "cave_entrance":
        print("You use the ancient key on the cave door. It unlocks!")
        locations["treasure_room"]["locked"] = False
    else:
        print(f"You can't use the {item} here.")

def fight_enemy():
    """Fight an enemy at the current location"""
    global health
    
    location = locations[current_location]
    
    if "enemy" not in location:
        print("There's nothing to fight here.")
        return
    
    enemy = location["enemy"]
    print(f"You attack the {enemy['name']}!")
    
    # Simple combat system
    enemy_health = enemy["health"]
    while enemy_health > 0 and health > 0:
        # Player attacks
        player_damage = random.randint(10, 20)
        enemy_health -= player_damage
        print(f"You hit the {enemy['name']} for {player_damage} damage!")
        
        # Enemy attacks if still alive
        if enemy_health > 0:
            enemy_damage = random.randint(5, enemy["damage"])
            health -= enemy_damage
            print(f"The {enemy['name']} hits you for {enemy_damage} damage!")
            print(f"Your health: {health}")
        
        time.sleep(1)
    
    if health <= 0:
        print("You have been defeated! Game over.")
        return False
    else:
        print(f"You defeated the {enemy['name']}!")
        del location["enemy"]
    
    return True

def show_help():
    """Display available commands"""
    print("\nAvailable commands:")
    print("  go [direction] - Move in the specified direction")
    print("  look - Examine your surroundings")
    print("  take [item] - Pick up an item")
    print("  inventory (or i) - Show your inventory")
    print("  use [item] - Use an item")
    print("  fight - Fight an enemy")
    print("  help - Show this help menu")
    print("  quit - Exit the game")

def main():
    """Main game loop"""
    print("\n" + "*" * 50)
    print("FOREST ADVENTURE")
    print("*" * 50)
    print("\nWelcome to the mysterious forest! Find the treasure to win.")
    print("Type 'help' for a list of commands.")
    
    display_location()
    
    playing = True
    while playing and health > 0:
        playing = get_command()
    
    if health <= 0:
        print("\nGAME OVER - You were defeated!")
    else:
        print("\nThanks for playing!")

if __name__ == "__main__":
    main()
