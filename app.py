from flask import Flask, render_template
from random import shuffle
import requests


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/play")
def play():
    # Make API call to image microservice
    response = requests.get("https://image-microservice-us.herokuapp.com/gifguessr")
    # Get back json object as a response
    image_json = response.json()
    # Json object format is {"image": "image url", "words": ["word1", "word2", "word3"], "name": "UsersFullName",
    # "username": "UsersUsername"}
    image_url = image_json["image"]
    word1 = image_json["words"][0]
    word2 = image_json["words"][1]
    word3 = image_json["words"][2]
    name = image_json["name"]
    username = image_json["username"]
    user_url = "https://unsplash.com/@" + username + "?utm_source=your_app_name&utm_medium=referral"
    credit_url = "https://unsplash.com/?utm_source=your_app_name&utm_medium=referral"
    # Get anagrams for words
    anagram1 = shuffle_word(word1)
    anagram2 = shuffle_word(word2)
    anagram3 = shuffle_word(word3)
    # Call teammate's microservice for word hints
    hint_url = "https://word-hint-service.herokuapp.com/hints/" + word1 + ',' + word2 + ',' + word3
    response = requests.get(hint_url)
    hint_json = response.json()
    hint1, hint_type1 = hint_json["hints"][0], hint_json["hint_types"][0]
    hint2, hint_type2 = hint_json["hints"][1], hint_json["hint_types"][1]
    hint3, hint_type3 = hint_json["hints"][2], hint_json["hint_types"][2]
    return render_template("play.html", image_url=image_url, word1=word1, word2=word2, word3=word3,
                           anagram1=anagram1, anagram2=anagram2, anagram3=anagram3, hint1=hint1, hint2=hint2,
                           hint3=hint3, hint_type1=hint_type1, hint_type2=hint_type2, hint_type3=hint_type3,
                           name=name, username=username, user_url=user_url, credit_url=credit_url)


def shuffle_word(word):
    """Function to create an anagram of a word"""
    original_word = word
    while original_word == word:
        word_list = list(word)
        shuffle(word_list)
        original_word = ''.join(word_list)
    return original_word


if __name__ == "__main__":
    app.run(debug=True)
