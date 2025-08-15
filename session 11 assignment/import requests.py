import requests

BASE_URL = "https://mastermind.darkube.app"
START_GAME_URL = f"{BASE_URL}/game"
GUESS_URL = f"{BASE_URL}/guess"

def start_game():
    response = requests.post(START_GAME_URL)
    if response.status_code == 200:
        return response.json()["game_id"]
    else:
        print(f"Error starting game: {response.status_code}")
        return None

def send_guess(game_id, guess):
    payload = {
        "game_id": game_id,
        "guess": guess
    }
    response = requests.post(GUESS_URL, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error submitting guess: {response.status_code}")
        return None

def validate_guess(guess):
    if len(guess) != 4:
        print("Guess must be exactly 4 digits long.")
        return False
    
    if not guess.isdigit(): #bray halati ke hamey dade ha int nistan va masalan yek harf ham dashte.
        print("Guess must contain only digits (1-6).")
        return False
    
    if any(digit not in '123456' for digit in guess):
        print("Only digits 1-6 are allowed.")
        return False
    
    if len(set(guess)) != 4:
        print("All digits must be unique (no duplicates).")
        return False
    
    return True

def prompt_guess(game_id):
    attempts = 0
    while True:
        guess = input("Enter your 4-digit guess (digits 1-6, all unique): ")
        
        if not validate_guess(guess):
            continue
            
        response = send_guess(game_id, guess)
        if not response:
            continue
            
        attempts += 1
        correct_positions = response.get("black", 0)
        correct_numbers = response.get("white", 0)

        circles = []
        circles.extend(["⚫"] * correct_positions) 
        circles.extend(["⚪"] * correct_numbers)   
        wrong_count = 4 - (correct_positions + correct_numbers)
        circles.extend(["🔴"] * wrong_count)      
        visual_feedback = " ".join(circles)
        
        print(f"Attempt {attempts}: {guess}  |  {visual_feedback}")
        print(f"⚫ Correct positions: {correct_positions}  |  ⚪ Correct numbers: {correct_numbers}  |  🔴 Wrong: {wrong_count}")
        
        if correct_positions == 4:
            print(f"🤝🤝 Congratulations! You solved it in {attempts} attempts🥇🥇🥇!")
            break

def run_game():
    print("""
    🎮🎮HI dear gamer!🎮🎮
    Welcome to Mastermind!
    you must guess the secret 4-digit code.
    Each digit is between 1 and 6(All digits are unique)
     
    You'll get feedback on:
      ⚫ Correct digits in correct position
      ⚪ Correct digits in wrong position
      🔴 Wrong digits""")
    
    game_id = start_game()
    if game_id:
        print("New game started!")
        prompt_guess(game_id)
    else:
        print("Failed to start a new game.")

run_game()
