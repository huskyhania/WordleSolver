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


safe = list("00000")
#Picks random word that the game tries to guess
correct = random.choice(words)
tries = 0
while (1):
	tries += 1
	print(f"this is my {tries} try")
	#Random word that the game thinks is the correct word
	random_guess = random.choice(words)
	# print("give your word")
	# random_guess = input()
	print(correct)
	print(random_guess)

	#green
	green_str = ["0"] * 5
	for i in range(5):
		if correct[i] == random_guess[i]:
			green_str[i] = random_guess[i]
	green = "".join(green_str)
	print("Green str")
	print(green)

	if green == correct:
		print(f"you win {green}")
		break

	#yellow
	yellow_str = ["0"] * 5
	for i in range(5):
		for x in range(5):
			if correct[i] == random_guess[x] and random_guess[x] != green_str[x]:
				yellow_str[x] = random_guess[x]
	yellow = "".join(yellow_str)
	print("Yellow str")
	print(yellow)

	#grey
	grey = ""
	for ch in random_guess:
		if ch not in correct:
       			grey += ch
	print(grey)

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
		print("There is no such word in english language. There are no possible guesses left.")
		break
	print("\nPossible guesses:")
	print(" | ".join(filtered))

	words = filtered