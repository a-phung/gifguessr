from flask import Flask, render_template
from random import shuffle  # TODO: Remove and replace with teammate's microservice
import requests


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/play")
def play():
    # TODO: Add image citations
    # Make API call to image microservice
    response = requests.get("https://image-microservice-us.herokuapp.com/gifguessr")
    # Get back json object as a response
    image_json = response.json()
    # Json object format is {"image": "image url", "words": ["word1", "word2", "word3"]}
    image_url = image_json["image"]
    word1 = image_json["words"][0]
    word2 = image_json["words"][1]
    word3 = image_json["words"][2]
    # Get hints for words
    hint1 = shuffle_word(word1)
    hint2 = shuffle_word(word2)
    hint3 = shuffle_word(word3)
    return render_template("play.html", image_url=image_url, word1=word1, word2=word2, word3=word3,
                           hint1=hint1, hint2=hint2, hint3=hint3)


def shuffle_word(word):
    """TODO: Replace with teammate's microservice."""
    word_list = list(word)
    shuffle(word_list)
    return ''.join(word_list)


if __name__ == "__main__":
    app.run(debug=True)
