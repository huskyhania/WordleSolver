import random

try:
	with open("wordle-La.txt", "r") as wordList:
		words = [line.strip() for line in wordList]
except FileNotFoundError:
	print("Error: Word list not found.")

except PermissionError:
	print("Error: No permissions to open the Word List.")

except Exception as e:
	print(f"Unexpected error: {e}")

keyboard_layout = {
    'q': 'default', 'w': 'default', 'e': 'default', 'r': 'default', 't': 'default', 'y': 'default', 'u': 'default', 'i': 'default', 'o': 'default', 'p': 'default',
    'a': 'default', 's': 'default', 'd': 'default', 'f': 'default', 'g': 'default', 'h': 'default', 'j': 'default', 'k': 'default', 'l': 'default',
    'z': 'default', 'x': 'default', 'c': 'default', 'v': 'default', 'b': 'default', 'n': 'default', 'm': 'default'
}

def colorize(char, status):
	colors = {
		'green': '\033[1;42m',
		'yellow': '\033[38;5;178m',
		'grey': '\033[1;100m',
		'default': '\033[0m'
	}
	return f"{colors[status]} {char.upper()} \033[0m"

def display_keyboard(layout):
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    print("\nKeyboard:")
    for row in rows:
        print("  ".join(colorize(c, layout[c]) for c in row))
    print()

def update_keyboard_state(guess, correct):
    for i, ch in enumerate(guess):
        if ch == correct[i]:
            keyboard_layout[ch] = 'green'
        elif ch in correct:
            if keyboard_layout[ch] != 'green':
                keyboard_layout[ch] = 'yellow'
        else:
            if keyboard_layout[ch] not in ['green', 'yellow']:
                keyboard_layout[ch] = 'grey'

safe = list("*****")
#Picks random word that the game tries to guess
print("Welcome to Terminal Wordle")
print("You have 6 tries to guess a 5 letter word")
correct = random.choice(words)
tries = 0
grey_set = set()
try: 
	while (1):
		tries += 1
		if tries == 7:
			print("Game over!")
			print(f"The word was {correct.upper()}")
			break
		print(f"\n--- Try {tries} ---")
		display_keyboard(keyboard_layout)
		print("Enter your guess: ")
		guess = input().strip().lower()
		if len(guess) != 5 or guess not in words:
			print("Invalid guess. Must be a valid 5-letter word.")
			tries -= 1
			continue
		
		#green
		green_str = ["*"] * 5
		for i in range(5):
			if correct[i] == guess[i]:
				green_str[i] = guess[i]
				safe[i] = guess[i]
		green = "".join(green_str)

		if green == correct:
			print(f"The word was indeed {green.upper()}")
			print("🎉Congratulations! You win!!!")
			break
		
		print("\nGreen letters (correct letter at correct positions)")
		print(" ".join(f"\033[92m{c}\033[0m" if c != '*' else '*' for c in safe))
		#yellow
		yellow_str = ["*"] * 5
		for i in range(5):
			for x in range(5):
				if correct[i] == guess[x] and guess[x] != green_str[x]:
					yellow_str[x] = guess[x]
		yellow = "".join(yellow_str)
		print("\nYellow letters (correct letters in wrong positons)")
		print(" ".join(f"\033[38;5;178m{c}\033[0m" if c != '*' else '*' for c in yellow))

		#grey
		grey = ""
		for ch in guess:
			if ch not in correct:
					grey += ch
		print("\nNewly excluded letters: ")
		print(grey)

		for i, letter in enumerate(green):
			if letter != '*':
				safe[i] = letter

		confirmed_letters = set([c for c in green if c != '*'] + [c for c in yellow if c != '*'])

		true_greys = [c for c in grey if c not in confirmed_letters]
		grey_set.update(true_greys)
		print("\nAll excluded letters so far:")
		print(' '.join(sorted(grey_set)))
		update_keyboard_state(guess, correct)
	
except (KeyboardInterrupt, EOFError):
    print("\n\nExiting game... Goodbye!\n")