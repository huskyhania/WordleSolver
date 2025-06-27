from flask import Flask, render_template, request, url_for, redirect
import os
import atexit
app = Flask(__name__)

# with open("wordle-La.txt") as f:
#     word_list = [line.strip() for line in f]

@app.route("/", methods=["GET", "POST"])
def index():
    winner = False
    error_message = ""
    GREEN_STATE_FILE = "green_state.txt"

    def load_green_state():
        if os.path.exists(GREEN_STATE_FILE):
            with open(GREEN_STATE_FILE, "r") as f:
                return f.read().strip()
        return "00000"

    def save_green_state(updated):
        with open(GREEN_STATE_FILE, "w") as f:
            f.write(updated)

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
        saved_green = load_green_state()
        updated_green = ''.join(
            green[i] if green[i] != "0" else saved_green[i]
            for i in range(5)
        )
        save_green_state(updated_green)
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
        #HERE FILTER
        #filtered = [word for word in word_list if all(letter not in word for letter in grey)]
        filtered = []
        for word in word_list:
            exclude = False
            for letter in grey:
                for i, char in enumerate(word):
                    if char == letter and updated_green[i] != letter:
                        exclude = True
                        break
                if exclude:
                    break
            if not exclude:
                filtered.append(word)
        
        for i, letter in enumerate(green):
            if letter != "0":
                filtered = [word for word in filtered if word[i] == letter]
        for i, letter in enumerate(yellow):
            if letter != "0":
                filtered = [word for word in filtered if letter in word and word[i] != letter]
        # result = " | ".join(filtered)
        if len(filtered) == 1:
            winner = True 
            if os.path.exists("temp"):
                os.remove("temp")
            if os.path.exists(GREEN_STATE_FILE):
                os.remove(GREEN_STATE_FILE)
                return render_template("index.html", result=filtered[0], winner=winner, error_message=error_message)
        elif len(filtered) == 0:
            error_message = "No words found with the given criteria. Please check your inputs."
            os.remove("temp")
            if os.path.exists(GREEN_STATE_FILE):
                os.remove(GREEN_STATE_FILE)
            return render_template("index.html", result=result, winner=winner, error_message=error_message)
        result = " | ".join(filtered)
        with open("temp", "w") as f:
            for word in filtered:
                f.write(word + "\n")
    return render_template("index.html", result=result, winner=winner, error_message=error_message)

@app.route("/reset", methods=["POST"])
def reset():
    if os.path.exists("temp"):
        os.remove("temp")
    if os.path.exists("green_state.txt"):
        os.remove("green_state.txt")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)