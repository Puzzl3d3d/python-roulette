from urllib import request, parse
import json
import random
import time
import os

# if you wanna bomb the api, add "jared_" before it (e.g. "/blackjack/jared_data") please :)
base_url = "https://flask.puzzl3d.dev"
api = "/blackjack" # yeah ik im using the /blackjack api but i tried changing it to /casino and it kept breaking so stfu
data_endpoint = "/data"
top_endpoint = "/top"

username = None

class leaderboard:
    @staticmethod
    def get_user():
        global username
        if not os.path.exists("session"):
            with open("session", "w") as file:
                username = input("Username: ")
                file.write(username)
        else:
            with open("session", "r") as file:
                username = file.read().split("\n")[0].strip()
        return username
    @staticmethod
    def get_top():
        try:
            with request.urlopen(f"{base_url}{api}{top_endpoint}") as response:
                charset = response.headers.get_content_charset()
                return json.loads(response.read().decode(charset or 'utf-8'))
        except Exception as e:
            print("ERROR |",e)
            return {}
    @staticmethod
    def get_data():
        try:
            with request.urlopen(f"{base_url}{api}{data_endpoint}") as response:
                charset = response.headers.get_content_charset()
                return json.loads(response.read().decode(charset or 'utf-8'))
        except Exception as e:
            return {}
    @staticmethod
    def get_self_data():
        query_params = parse.urlencode({'name': username or leaderboard.get_user()})
        try:
            with request.urlopen(f"{base_url}{api}{data_endpoint}?{query_params}") as response:
                charset = response.headers.get_content_charset()
                return json.loads(response.read().decode(charset or 'utf-8'))
        except Exception as e:
            return {}
    @staticmethod
    def update(value):
        query_params = parse.urlencode({'name': username or leaderboard.get_user(), 'value': value, "roulette": True})
        req = request.Request(f"{base_url}{api}{data_endpoint}?{query_params}", method="POST")
        try:
            with request.urlopen(req) as response:
                charset = response.headers.get_content_charset()
                return response.read().decode(charset or 'utf-8')
        except Exception as e:
            return f"An error occurred: {e}"
    @staticmethod
    def ordinal_suffix(position):
        position = int(position)
        if 10 <= position % 100 <= 20:
            suffix = 'th'
        else:
            suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
            suffix = suffixes.get(position % 10, 'th')
        return f"{position}{suffix}"

cooldown = 60
user = leaderboard.get_user()


cooldown = 60

# Define the roulette slots with ANSI color codes
GREEN = "\033[42m"
RED = "\033[41m"
BLACK = "\033[40m"
RESET = "\033[0m"
slots = [
    f"{GREEN}0 {RESET}",   f"{RED}32{RESET}", f"{BLACK}15{RESET}",   f"{RED}19{RESET}", f"{BLACK}4 {RESET}", 
      f"{RED}21{RESET}", f"{BLACK}2 {RESET}",   f"{RED}25{RESET}", f"{BLACK}17{RESET}",   f"{RED}34{RESET}", 
    f"{BLACK}6 {RESET}",   f"{RED}27{RESET}", f"{BLACK}13{RESET}",   f"{RED}36{RESET}", f"{BLACK}11{RESET}", 
      f"{RED}30{RESET}", f"{BLACK}8 {RESET}",   f"{RED}23{RESET}", f"{BLACK}10{RESET}",   f"{RED}5 {RESET}", 
    f"{BLACK}24{RESET}",   f"{RED}16{RESET}", f"{BLACK}33{RESET}",   f"{RED}1 {RESET}", f"{BLACK}20{RESET}", 
      f"{RED}14{RESET}", f"{BLACK}31{RESET}",   f"{RED}9 {RESET}", f"{BLACK}22{RESET}",   f"{RED}18{RESET}", 
    f"{BLACK}29{RESET}",   f"{RED}7 {RESET}", f"{BLACK}28{RESET}",   f"{RED}12{RESET}", f"{BLACK}35{RESET}", 
      f"{RED}3 {RESET}", f"{BLACK}26{RESET}"
]

# A simple function to clear the terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_wheel(wheel_sequence, marker_index):
    marker_spacing = 3  # Spaces per slot (3 for digits/space and 1 additional space)
    marker_string = ' ' * (marker_index * marker_spacing) + '^'  # The marker aligned with the first digit
    wheel_string = ' '.join(wheel_sequence)

    # Print the wheel and the marker below it
    print(wheel_string)
    print(marker_string)
def place_bets(money):
    bets = {}
    while True:
        for bet in bets:
            value = bets[bet]
            print(f"BET {bet.upper()} for ${value:.2f}")
        print(f"You have ${money:.2f} left")
        print("\tb    -> Black  (1x payout)\n\tr    -> Red    (1x payout)\n\t0-36 -> Square (35x payout)")
        bet = input(f"Place your bet or press ENTER to spin: ")
        if bet == "" and len(bets.keys()) > 0:  # Player finished betting
            break
        if bet.lower() in ["r", "b", "g"] or bet in [str(x) for x in range(37)]:
            bet = bet.lower()
            if bets.get(bet):
                amount = input("New amount to bet: $")
            else:
                amount = input("Amount to bet: $")
            try:
                amount = float(amount)
                if bets.get(bet): 
                    money += bets[bet]
                    bets[bet] = None
                if amount <= 0 or amount > money:
                    print("Invalid amount. Try again.")
                    continue
                bets[bet] = amount
                money -= amount
            except ValueError:
                #print("Invalid input. Please enter a numeric value for the amount.")
                clear_screen()
                continue
        else:
            print("Invalid bet. Try again.")
        clear_screen()
    return bets, money
def spin_roulette():
    print("Spinning the roulette wheel...")
    delay = 0.03  # Initial delay between each frame
    marker_index = len(slots) // 2  # Start the marker in the middle

    # Shuffle the wheel randomly before beginning to spin
    starting_offset = random.randint(0, len(slots) - 1)
    slots[:] = slots[starting_offset:] + slots[:starting_offset]
    
    locking_delay = random.randint(17, 30)/100

    # Spin until delay reaches about 0.2 seconds
    while delay < locking_delay:
        clear_screen()
        print_wheel(slots, marker_index)
        time.sleep(delay)
        # Rotate the wheel
        slots.insert(0, slots.pop())
        delay *= 1.06

    # Once delay reaches 0.2, lock the marker
    locking_range = range(10, 20)  # Additional spins after locking marker
    spins_after_lock = random.choice(locking_range)

    for _ in range(spins_after_lock):
        clear_screen()
        print_wheel(slots, marker_index)
        time.sleep(delay)
        # Rotate the wheel and move the marker
        slots.insert(0, slots.pop())
        marker_index = (marker_index + 1) % len(slots)

    # Final result
    clear_screen()
    winning_slot = slots[marker_index]
    print_wheel(slots, marker_index)
    print(f"The ball landed on slot {winning_slot}!")
    return winning_slot


def calculate_money(bets, winning_slot):
    global money
    winning_color = "g" if winning_slot.count(GREEN) > 0 else (
        "b" if winning_slot.count(BLACK) > 0 else "r"
    )

    for bet_choice, bet_amount in bets.items():
        if bet_choice == winning_slot:
            # Winning on an exact number match
            money += bet_amount + (bet_amount * 35)
            print(f"BET {bet_choice.upper()} | Success! ${(bet_amount * 35):.2f} gained!")
            return
        elif bet_choice == winning_color:
            # Winning on a color match
            money += bet_amount + (bet_amount)
            print(f"BET {bet_choice.upper()} | Success! ${(bet_amount):.2f} gained!")
            return
        print(f"BET {bet_choice.upper()} | Loss! ${bet_amount} lost!")
        # Loses are naturally handled since the money is not adjusted for losing bets


def do_round():
    global money
    bets,money = place_bets(money)
    winning_slot = spin_roulette()
    calculate_money(bets, winning_slot)


# Run the roulette wheel simulation
if __name__ == "__main__":
    data = leaderboard.get_self_data()
    money = data.get("current", 100)
    delta = time.time() - data.get("last_updated", 0)
    if money == 0 and delta > cooldown:
        money = 100
        leaderboard.update(money)
    elif money == 0:
        while True:
            clear_screen()
            delta = time.time() - data.get("last_updated", 0)
            if delta > cooldown: break
            else: print(f"You ran out of money! Play again in {round(cooldown-delta)} seconds")
            time.sleep(0.5)
        money = 100
        leaderboard.update(money)

    while True:
        while True:
            do_round()
            leaderboard.update(money)

            if money <= 0:
                break

        print(f"You ran out of money! Play again in {cooldown} seconds")
        start = time.time()
        time.sleep(1)
        while True:
            clear_screen()
            delta = time.time() - start
            if delta > cooldown: break
            else: print(f"{round(cooldown-delta)} seconds left!", end="")
            time.sleep(0.5)
        money = 100
        leaderboard.update(money)
