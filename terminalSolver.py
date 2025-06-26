try:
	with open("wordle-La.txt", "r") as wordList:
		words = [line.strip() for line in wordList]

	# print("Possible guesses: ")
	# for word in words:
	# 	print(word)

except FileNotFoundError:
	print("Error: Word list not found.")

except PermissionError:
	print("Error: No permissions to open the Word List.")

except Exception as e:
	print(f"Unexpected error: {e}")


safe = list("00000")
while (1):
	print("\nGreen letters (e.g., 0a0c0):")
	green = input().strip().lower()

	print("Yellow letters (e.g., 00b00):")
	yellow = input().strip().lower()

	print("Grey letters (e.g., xyz):")
	grey = input().strip().lower()
	
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

	print("\nPossible guesses:")
	print(" | ".join(filtered))

	words = filtered