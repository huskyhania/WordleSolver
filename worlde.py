from flask import Flask, render_template, request
import os
import atexit

app = Flask(__name__)

# with open("wordle-La.txt") as f:
#     word_list = [line.strip() for line in f]

@app.route("/", methods=["GET", "POST"])
def index():
    winner = False
    if os.path.exists("temp"):
        with open("temp", "r") as f:
            word_list = [line.strip() for line in f]
    else:
        with open("wordle-La.txt") as f:
            word_list = [line.strip() for line in f]
    result = ""
    if request.method == "POST":
        #join green letters
        green_letters = []
        for i in range(1, 6):
            letterg = request.form.get(f"green{i}", "").strip().lower()
            if len(letterg) == 0:
                letterg = "0"
            green_letters.append(letterg)
        green = ''.join(green_letters)
        #print(green)
        #join yellow letters
        yellow_letters = []
        for i in range(1, 6):
            lettery = request.form.get(f"yellow{i}", "").strip().lower()
            if len(lettery) == 0:
                lettery = "0"
            yellow_letters.append(lettery)
        yellow = ''.join(yellow_letters)
        #print(yellow)
        #start checking
        grey = request.form.get("grey", "").strip().lower()
        filtered = [word for word in word_list if all(letter not in word for letter in grey)]
        for i, letter in enumerate(green):
            if letter != "0":
                filtered = [word for word in filtered if word[i] == letter]
        for i, letter in enumerate(yellow):
            if letter != "0":
                filtered = [word for word in filtered if letter in word and word[i] != letter]
        result = " | ".join(filtered)
        with open("temp", "w") as f:
            for word in filtered:
                f.write(word + "\n")
        if len(filtered) <= 1:
            winner = True 
            if os.path.exists("temp"):
                os.remove("temp")

    return render_template("index.html", result=result, winner=winner)

if __name__ == "__main__":
    app.run(debug=True)