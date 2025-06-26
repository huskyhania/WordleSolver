

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

while (1):
	print("Green letters")
	green = str(input()) #Green Typecasted to string
	print("Yellow letters")
	yellow = str(input()) #Yellow Typecasted to string
	print("Grey letters")
	grey = str(input()) #Gray Typecasted to string

	answer = "hello"

	print("--Input--")
	print(green)
	print(yellow)
	print(grey)

	#Call solver function
	# ft_solver(green,yellow,grey)



	if input == answer:
		print("Congratulations!")
	else:
		filtered = [word for word in words if all(letter not in word for letter in grey)]
		# filtered = [word for word in words if all(letter not in word[2] for letter in green)]
		for i, letter in enumerate(green):
			if letter != "0":
				filtered = [word for word in filtered if word[i] == letter]
		for i, letter in enumerate(yellow):
			if letter != "0":
				filtered = [word for word in filtered if letter in word and word[i] != letter]
		print("Possible guesses: ")
		print(" | ".join(filtered))
		words = filtered
