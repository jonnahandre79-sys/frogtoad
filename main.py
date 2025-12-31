import time
import random
import sys
import os

# ==================== VISUAL & AUDIO ENGINE ====================

class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

class Icons:
    FROG = "🐸"
    TOAD = "🐍"
    COIN = "🪙"
    HEART = "❤️"
    ENERGY = "⚡"
    BAG = "🎒"

def play_sound(pattern="short"):
    # simple console beep patterns (may be limited by terminal)
    if pattern == "short":
        sys.stdout.write('\a')
    elif pattern == "jingle":
        for _ in range(3):
            sys.stdout.write('\a')
            time.sleep(0.1)
    elif pattern == "rising":
        for i in range(4):
            sys.stdout.write('\a')
            time.sleep(0.12 + i*0.03)
    sys.stdout.flush()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ==================== ANIMAL "PICTURE" RENDERING ====================

def draw_frog_portrait():
    print(f"""
    {Color.GREEN}      _    _      
     (o)--(o)     
    /.______.\    
    \________/    
   ./        \.   
  (            )  
   \  __  __  /   {Color.END}
    """)

def draw_toad_portrait():
    print(f"""
    {Color.YELLOW}     .-'''-.      
    /   _   \     
   |  (o o)  |    
    \   _   /     
    /       \     
   /  \___/  \    
  /           \   {Color.END}
    """)

# ==================== GAME STATE ====================

class GameState:
    def __init__(self):
        self.friendship = 20
        self.inventory = ["Old Map"]
        self.chapters_completed = 0
        self.health = 100
        self.energy = 100
        self.money = 10
        self.day = 1
        self.location = "Toad's House"
        self.achievements = []

    def show_inventory(self):
        clear_screen()
        print(f"{Color.MAGENTA}{Icons.BAG} YOUR ADVENTURE BAG {Icons.BAG}{Color.END}")
        print("═" * 30)
        if not self.inventory:
            print("Your bag is empty and light.")
        for item in self.inventory:
            print(f"• {item}")
        print("═" * 30)
        print(f"Pond Coins: {Icons.COIN} {self.money}")
        input("\nPress Enter to close bag...")

    def add_achievement(self, name):
        if name not in self.achievements:
            self.achievements.append(name)
            play_sound("jingle")

# ==================== INTERACTIVE MODULES ====================

def pond_shop(state):
    state.location = "The General Store"
    draw_header(state)
    print(f"{Color.CYAN}Turtle Shopkeeper:{Color.END} 'Welcome! Only the finest pond goods here.'\n")
    
    items = {"Fly-Juice": 5, "Warm Blanket": 15, "Shiny Marble": 10}
    for i, (item, price) in enumerate(items.items(), 1):
        print(f"{i}. {item} - {price} Coins")
    print("4. Leave Shop")
    
    choice = input("\nChoose an option (1-4): ").strip()
    if choice in ("1", "2", "3"):
        try:
            idx = int(choice) - 1
            item_list = list(items.items())
            item_name, price = item_list[idx]
        except (ValueError, IndexError):
            print("\nInvalid selection.")
            input("\nPress Enter to continue...")
            return state

        if state.money >= price:
            state.money -= price
            state.inventory.append(item_name)
            play_sound("short")
            print(f"\nYou bought {item_name} for {price} Coins.")
        else:
            print("\nNot enough Coins.")
        input("\nPress Enter to continue...")
    # any other input (including 4) leaves the shop
    return state

def chapter_stargazing(state):
    state.location = "Starlight Ridge"
    draw_header(state)
    type_print(f"{Color.CYAN}The sky turns a deep indigo...{Color.END}")
    
    for _ in range(6):
        stars = "".join(random.choice([" ", " ", ".", "*", "✧", " "]) for _ in range(60))
        sys.stdout.write(f"\r{Color.YELLOW}{stars}{Color.END}")
        sys.stdout.flush()
        time.sleep(0.25)
    print()

    draw_frog_portrait()
    type_print("Frog: 'The stars look like little lanterns tonight!'")
    print(f"1. Make a wish (+Friendship)\n2. Just watch (+Energy)")

    choice = input("> ").strip()
    if choice == "1":
        state.friendship = min(100, state.friendship + 10)
        print("\nYou feel closer.")
    else:
        state.energy = min(100, state.energy + 20)
        print("\nYou feel rested.")
    state.chapters_completed += 1
    input("\nPress Enter to continue...")
    return state

def grand_festival_finale(state):
    state.location = "The Great Pond Festival"
    draw_header(state)
    play_sound("rising")
    type_print(f"{Color.MAGENTA}🎆 THE FESTIVAL OF THE GOLDEN LILY 🎆{Color.END}")
    
    # Firework Show
    for _ in range(6):
        print(" " * random.randint(10, 50) + Color.YELLOW + "✨ EXPLOSION! ✨" + Color.END)
        play_sound("short")
        time.sleep(0.4)

    draw_toad_portrait()
    type_print("Toad: 'I'm so happy we spent this hour together, Frog.'")
    state.add_achievement("Eternal Bond")
    state.chapters_completed += 1
    input("\nPress Enter to continue...")
    return state

def draw_header(state):
    clear_screen()
    print(f"{Color.BLUE}{'═'*60}{Color.END}")
    print(f"📍 {state.location} | {Icons.HEART} {state.health} | {Icons.ENERGY} {state.energy} | {Icons.COIN} {state.money}")
    print(f"👥 Friendship: {state.friendship}/100 | Chapter: {state.chapters_completed}/40")
    print(f"{Color.BLUE}{'═'*60}{Color.END}\n")

# ==================== MAIN ENGINE ====================

def main():
    state = GameState()
    
    # Intro Sequence
    clear_screen()
    draw_frog_portrait()
    type_print(f"{Color.GREEN}{Color.BOLD}FROG & TOAD: THE 1-HOUR JOURNEY{Color.END}")
    play_sound("rising")
    time.sleep(1.2)

    try:
        while state.chapters_completed < 40:
            draw_header(state)
            print("Options: (1) Adventure  (2) Open Bag  (3) Shop  (4) Quit")
            choice = input("\nChoose your action: ").strip()

            if choice == "2":
                state.show_inventory()
                continue
            elif choice == "3":
                state = pond_shop(state)
                continue
            elif choice == "4":
                print("\nGoodbye.")
                break

            # Adventure Logic
            if state.chapters_completed >= 39:
                state = grand_festival_finale(state)
                continue

            # Traveling Animation
            print(f"\n{Color.GREEN}Walking through the tall grass...{Color.END}")
            for _ in range(6):
                sys.stdout.write("👣 ")
                sys.stdout.flush()
                time.sleep(0.6)
            print("\n")

            # Random event selection
            event = random.choice([chapter_stargazing, pond_shop])
            state = event(state)

    except KeyboardInterrupt:
        print("\n\nInterrupted. Exiting...")

    # FINAL ENDING / SUMMARY
    clear_screen()
    type_print("The sun sets on a perfect adventure.")
    print(f"Final Friendship: {state.friendship}")
    print(f"Achievements earned: {', '.join(state.achievements) if state.achievements else 'None'}")
    play_sound("rising")

if __name__ == "__main__":
    main()