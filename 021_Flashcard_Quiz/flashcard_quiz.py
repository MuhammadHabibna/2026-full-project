import csv
import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_vocab(filename="vocab.csv"):
    flashcards = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None) # Skip header
            for row in reader:
                if len(row) >= 2:
                    flashcards.append((row[0], row[1]))
    except FileNotFoundError:
        print(f"[ERROR] File '{filename}' not found.")
        return []
    return flashcards

def play_quiz():
    clear_screen()
    print("="*50)
    print("       ULTIMATE FLASHCARD QUIZ")
    print("="*50)
    
    cards = load_vocab()
    if not cards:
        print("[INFO] No cards available. Please check vocab.csv.")
        return

    # Shuffle cards
    random.shuffle(cards)
    
    # Settings
    total_questions = min(10, len(cards)) # Max 10 questions per round
    score = 0
    start_time = time.time()

    print(f"[INFO] Loaded {len(cards)} words. Starting round of {total_questions} questions...\n")
    time.sleep(1)

    for i in range(total_questions):
        q, a = cards[i]
        
        print(f"[{i+1}/{total_questions}] What is '{q}' in Indonesian?")
        user_answer = input("   Answer: ").strip()

        if user_answer.lower() == a.lower():
            print("   [V] CORRECT! +10 Points\n")
            score += 10
        else:
            print(f"   [X] WRONG! The correct answer was '{a}'.\n")
        
        time.sleep(0.5)

    # Final Score
    elapsed = time.time() - start_time
    clear_screen()
    print("="*50)
    print("             QUIZ  COMPLETED")
    print("="*50)
    print(f" Final Score : {score} / {total_questions * 10}")
    print(f" Time Taken  : {elapsed:.1f} seconds")
    
    # Grade
    percentage = (score / (total_questions * 10)) * 100
    if percentage == 100:
        print(" Rank: LEGENDARY!")
    elif percentage >= 80:
        print(" Rank: MASTER")
    elif percentage >= 50:
        print(" Rank: APPRENTICE")
    else:
        print(" Rank: NOOB (Keep trying!)")
    print("="*50)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    play_quiz()
