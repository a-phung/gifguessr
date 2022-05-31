from flask import Flask, render_template
from random import shuffle
import requests
import os

IMAGE_FOLDER = os.path.join("static", "images")

app = Flask(__name__)
app.config["IMAGE_FOLDER"] = IMAGE_FOLDER


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/play")
def play():
    try:
        # Make API call to image microservice
        response = requests.get("https://image-microservice-us.herokuapp.com/gifguessr")
        # Get back json object as a response
        image_json = response.json()
        # Json object format is {"image": "image url", "words": ["word1", "word2", "word3"], "name": "UsersFullName",
        # "username": "UsersUsername"}
        jinja_data = parse_json(image_json)
        # Get anagrams for words
        jinja_data = get_anagrams(jinja_data)
        # Call teammate's microservice for word hints
        jinja_data = microservice(jinja_data)
        return render_template("play.html", data=jinja_data)
    except Exception:
        error_image = os.path.join(app.config["IMAGE_FOLDER"], "404error.png")
        return render_template("error.html", error_image=error_image)


def parse_json(image_json):
    """Organize the relevant json data into a dictionary."""
    jinja_data = {"image_url": image_json["image"], "word1": image_json["words"][0],
                  "word2": image_json["words"][1], "word3": image_json["words"][2], "name": image_json["name"],
                  "username": image_json["username"], "user_url": "https://unsplash.com/@" + image_json[
            "username"] + "?utm_source=your_app_name&utm_medium=referral",
                  "credit_url": "https://unsplash.com/?utm_source=your_app_name&utm_medium=referral"}
    return jinja_data


def get_anagrams(jinja_data):
    """Adds anagrams of each of the three words into the jinja dictionary."""
    jinja_data["anagram1"] = shuffle_word(jinja_data["word1"])
    jinja_data["anagram2"] = shuffle_word(jinja_data["word2"])
    jinja_data["anagram3"] = shuffle_word(jinja_data["word3"])
    return jinja_data


def shuffle_word(word):
    """Function to create an anagram of a word"""
    original_word = word
    while original_word == word:
        word_list = list(word)
        shuffle(word_list)
        original_word = ''.join(word_list)
    return original_word


def microservice(jinja_data):
    """Calls teammate's microservice to get a hint for each word."""
    hint_url = "https://word-hint-microservice.herokuapp.com/hints/" + jinja_data["word1"] + ',' + jinja_data["word2"] \
               + ',' + jinja_data["word3"]
    response = requests.get(hint_url)
    hint_json = response.json()
    jinja_data["hint1"], jinja_data["hint_type1"] = hint_json["hints"][0], hint_json["hint_types"][0]
    jinja_data["hint2"], jinja_data["hint_type2"] = hint_json["hints"][1], hint_json["hint_types"][1]
    jinja_data["hint3"], jinja_data["hint_type3"] = hint_json["hints"][2], hint_json["hint_types"][2]
    return jinja_data


if __name__ == "__main__":
    app.run(debug=True)
