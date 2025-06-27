from flask import Flask, render_template, request, url_for, redirect
from collections import Counter
import os
import atexit
app = Flask(__name__)

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
            word_list_str = ""
    else:
        with open("wordle-La.txt") as f:
            word_list = [line.strip() for line in f]
            word_list_str = " | ".join(word_list)
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
        yellow_letters = []
        for i in range(1, 6):
            lettery = request.form.get(f"yellow{i}", "").strip().lower()
            if len(lettery) == 0:
                lettery = "0"
            yellow_letters.append(lettery)
        yellow = ''.join(yellow_letters)

        grey = request.form.get("grey", "").strip().lower()
        #FILTERING
        required_counts = Counter([c for c in updated_green if c != '0'])
        required_counts.update([c for c in yellow if c != '0'])
        filtered = []
        for word in word_list:
            #Checks how many times a letter appears in the current word
            word_counter = Counter(word)

            too_many_grey = False
            for g in grey:
                allowed = required_counts.get(g, 0)
                if word_counter[g] > allowed:
                    too_many_grey = True
                    break
            if too_many_grey:
                continue

            if not all(g == '0' or word[i] == g for i, g in enumerate(updated_green)):
                continue

            valid_yellow = True
            for i, y in enumerate(yellow):
                if y != '0':
                    if y not in word or word[i] == y:
                        valid_yellow = False
                        break
            if not valid_yellow:
                continue

            filtered.append(word)

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
        word_list_str = ""
        with open("temp", "w") as f:
            for word in filtered:
                f.write(word + "\n")
    return render_template("index.html", result=result, winner=winner, error_message=error_message, word_list_str=word_list_str)

@app.route("/reset", methods=["POST"])
def reset():
    if os.path.exists("temp"):
        os.remove("temp")
    if os.path.exists("green_state.txt"):
        os.remove("green_state.txt")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)