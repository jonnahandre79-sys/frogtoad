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

def play_sound(pattern="short"):
    """Uses system bell to create 8-bit sound effects"""
    if pattern == "short":
        sys.stdout.write('\a')
    elif pattern == "jingle":
        for _ in range(3):
            sys.stdout.write('\a')
            time.sleep(0.1)
    elif pattern == "rising":
        for i in range(4):
            sys.stdout.write('\a')
            time.sleep(0.15)
    sys.stdout.flush()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ==================== CORE GAME STATE ====================

class GameState:
    def __init__(self):
        self.friendship = 20
        self.inventory = []
        self.chapters_completed = 0
        self.health = 100
        self.energy = 100
        self.day = 1
        self.time_of_day = "Morning"
        self.weather = "Sunny"
        self.location = "Toad's House"
        self.achievements = []

    def update_stats(self):
        self.friendship = max(0, min(100, self.friendship))
        self.energy = max(0, min(100, self.energy))
        self.health = max(0, min(100, self.health))

    def add_achievement(self, name):
        if name not in self.achievements:
            self.achievements.append(name)
            play_sound("rising")

# ==================== ANIMATED CHAPTERS ====================

def draw_header(state):
    clear_screen()
    print(f"{Color.BLUE}{'═'*60}{Color.END}")
    print(f"{Color.BOLD}📍 {state.location} | ❤️ {state.health} | ⚡ {state.energy} | 👥 {state.friendship}{Color.END}")
    print(f"{Color.BLUE}{'═'*60}{Color.END}\n")

def chapter_stargazing(state):
    state.location = "Starlight Ridge"
    draw_header(state)
    type_print(f"{Color.CYAN}The sun sets, and the sky turns a deep indigo...{Color.END}")
    
    # Twinkle Animation
    for _ in range(5):
        stars = "".join(random.choice([" ", " ", ".", "*", "✧", " "]) for _ in range(50))
        sys.stdout.write(f"\r{Color.YELLOW}{stars}{Color.END}")
        sys.stdout.flush()
        time.sleep(0.5)
    print("\n")

    type_print("Frog: 'The stars are so bright, they look like silver coins!'")
    print(f"1. {Color.MAGENTA}Make a wish together (+Friendship){Color.END}")
    print(f"2. {Color.BLUE}Identify constellations (+Energy){Color.END}")
    
    choice = input("\n> ")
    if choice == "1":
        state.friendship += 10
        play_sound("short")
    else:
        state.energy += 15
    
    state.chapters_completed += 1
    return state

def chapter_treasure_hunt(state):
    state.location = "The Hidden Grove"
    draw_header(state)
    type_print("A mysterious map leads you to a patch of ancient ferns...")
    
    # Scanning Animation
    for i in range(11):
        bar = "█" * i + "░" * (10 - i)
        sys.stdout.write(f"\r{Color.YELLOW}Searching: [{bar}] Detecting Treasure...{Color.END}")
        sys.stdout.flush()
        time.sleep(0.3)
    
    play_sound("jingle")
    print(f"\n\n{Color.GREEN}SUCCESS! You found a Golden Dragonfly Brooch!{Color.END}")
    state.inventory.append("Golden Brooch")
    state.friendship += 5
    state.chapters_completed += 1
    return state

def grand_festival_finale(state):
    state.location = "The Great Pond Center"
    draw_header(state)
    play_sound("rising")
    
    type_print(f"{Color.MAGENTA}🎆 THE FESTIVAL OF THE GOLDEN LILY HAS BEGUN! 🎆{Color.END}")
    
    # Firework Animation
    for _ in range(4):
        offset = " " * random.randint(5, 40)
        print(f"{offset}{Color.YELLOW}* . : . *{Color.END}")
        play_sound("short")
        time.sleep(0.5)

    type_print("\nToad: 'Frog, this is the best day I've had in 100 years.'")
    type_print("Frog: 'Me too, Toad. Me too.'")
    
    input(f"\n{Color.BOLD}Press Enter to release the friendship lantern...{Color.END}")
    
    for i in range(6):
        sys.stdout.write(f"\r{' ' * (20-i)} 🏮 {Color.YELLOW}(Rising Higher...){Color.END}")
        sys.stdout.flush()
        time.sleep(0.7)
    
    state.add_achievement("Eternal Best Friends")
    state.chapters_completed += 1
    return state

# ==================== MAIN ENGINE ====================

def main():
    state = GameState()
    
    # Intro
    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}")
    print("  🐸 FROG & TOAD: THE ANIMATED ODYSSEY 🐍")
    print("      (A 1-Hour Interactive Adventure)")
    print(f"{Color.END}")
    play_sound("rising")
    time.sleep(1)

    max_chapters = 40
    
    while state.chapters_completed < max_chapters:
        # Chapter Logic
        if state.chapters_completed == 0:
            # Wake up sequence
            state.location = "Toad's Bedroom"
            draw_header(state)
            type_print("Frog is jumping on the bed! 'Wake up, wake up!'")
            input("\nPress Enter to start the day...")
            state.chapters_completed += 1
        
        elif state.chapters_completed == max_chapters - 1:
            state = grand_festival_finale(state)
        
        else:
            # Random Adventure Selection
            adventure = random.choice([chapter_stargazing, chapter_treasure_hunt])
            state = adventure(state)
            
            # "Walking" animation to pad time and add immersion
            print(f"\n{Color.BLUE}Traveling to the next location...{Color.END}")
            for _ in range(3):
                sys.stdout.write(". ")
                sys.stdout.flush()
                time.sleep(1)
        
        # Check Health/Energy
        if state.energy <= 0:
            type_print(f"\n{Color.RED}Toad is too tired. You must rest for a day.{Color.END}")
            state.energy = 50
            state.day += 1

    # Ending Statistics
    draw_header(state)
    type_print(f"{Color.BOLD}ADVENTURE COMPLETE!{Color.END}")
    print(f"Days Journeyed: {state.day}")
    print(f"Final Friendship: {state.friendship}/100")
    print(f"Achievements: {', '.join(state.achievements)}")
    play_sound("rising")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAdventure paused. See you at the pond!")
