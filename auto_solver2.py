import random
import tkinter as tk

win = '''
                               _       
                              (_)      
  _   _  ___  _   _  __      ___ _ __  
 | | | |/ _ \| | | | \ \ /\ / / | '_ \ 
 | |_| | (_) | |_| |  \ V  V /| | | | |
  \__, |\___/ \__,_|   \_/\_/ |_|_| |_|
   __/ |                               
  |___/                                
'''
root = tk.Tk()

root.title("Tk Example")
root.configure(background="white")
root.minsize(1200, 1200)
root.maxsize(1500, 1500)
root.geometry("300x300+50+50")

try:
    with open("wordle-La.txt", "r") as wordList:
        words = [line.strip() for line in wordList]
except FileNotFoundError:
    print("Error: Word list not found.")
    words = []
except PermissionError:
    print("Error: No permissions to open the Word List.")
    words = []
except Exception as e:
    print(f"Unexpected error: {e}")
    words = []

safe = list("00000")
correct = random.choice(words) if words else "crane"  # fallback word
tries = 0

# Display the correct word in a label (for testing, you can hide later)
label_correct = tk.Label(root, text=correct, fg="white", bg="black", width=20, height=2)
label_correct.pack()

# Label to show the random guesses
label_guess = tk.Label(root, text="", fg="black", bg="red", width=20, height=2)
label_guess.pack()

# Label to show messages (like "You win!")

# label_message = tk.Label(root, text="", fg="green", bg="white", width=1, height=1)
# label_message.pack()

label_list = tk.Label(root, text="", fg="green", bg="white", width=300, height=200)
label_list.pack()

def make_guess(event=None):
    global tries, words, safe

    if len(words) == 0:
        label_message.config(text="No words to guess from!")
        return

    tries += 1
    print(f"Try #{tries}")

    random_guess = random.choice(words)
    print(f"Guess: {random_guess} number {tries}")
    label_guess.config(text=f"Guess #{tries}: {random_guess}")

    # Green logic
    green_str = ["0"] * 5
    for i in range(5):
        if correct[i] == random_guess[i]:
            green_str[i] = random_guess[i]
    green = "".join(green_str)
    print("Green str:", green)

    if green == correct:
        label_list.config(text=f"{win}")
        root.unbind("<Key>")  # stop guessing on further keypresses
        return

    # Yellow logic
    yellow_str = ["0"] * 5
    for i in range(5):
        for x in range(5):
            if correct[i] == random_guess[x] and random_guess[x] != green_str[x]:
                yellow_str[x] = random_guess[x]
    yellow = "".join(yellow_str)
    print("Yellow str:", yellow)

    # Grey logic
    grey = ""
    for ch in random_guess:
        if ch not in correct:
            grey += ch
    print("Grey str:", grey)

    for i, letter in enumerate(green):
        if letter != '0':
            safe[i] = letter

    confirmed_letters = set([c for c in green if c != '0'] + [c for c in yellow if c != '0'])

    true_greys = [c for c in grey if c not in confirmed_letters]

    filtered = words[:]

    for i, letter in enumerate(safe):
        if letter != '0':
            filtered = [word for word in filtered if word[i] == letter]

    for i, letter in enumerate(yellow):
        if letter != '0':
            filtered = [word for word in filtered if letter in word and word[i] != letter]

    def is_valid(word):
        for g in true_greys:
            if g in word:
                if any((word[i] == g and safe[i] == '0') for i in range(5)):
                    return False
        return True

    filtered = [word for word in filtered if is_valid(word)]

    if len(filtered) == 0:
        label_message.config(text="No possible guesses left!")
        root.unbind("<Key>")
        return

    print("\nPossible guesses:")
    print(" | ".join(filtered))

    words = filtered
    result = []
    for i, word in enumerate(filtered,1):
        result.append(word)
    lines = []
    for i in range(0, len(result), 15):
        chunk = result[i:i+15]
        lines.append(" ".join(chunk))

    final_str = "\n".join(lines)

    label_list.config(text=f"Possible guesses:\n{final_str}")

# Bind key press event to call make_guess
root.bind("<Key>", make_guess)

root.mainloop()
