from flask import Flask, json, redirect, url_for, render_template, request
import requests
import random

app = Flask(__name__)
app.config.from_pyfile("config.py")
app.url_map.strict_slashes = False

ENGLISH_API_KEY = "?key=" + app.config.get("ENGLISH_API_KEY")
SPANISH_API_KEY = "?key=" + app.config.get("SPANISH_API_KEY")

# ---------- HELPER METHODS -----------
def get_master(language):
    """Returns a collection of words from the given language by making a GET request to an online JSON document."""
    if language == "english":
        dictionary_json_url = 'https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json'
    elif language == "spanish":
        dictionary_json_url = 'https://raw.githubusercontent.com/words/an-array-of-spanish-words/master/index.json'
    dictionary_json = requests.get(dictionary_json_url)
    dictionary = json.loads(dictionary_json.text)
    return dictionary

def get_data_from_api(language, word):
    """Calls the Merriam-Webster endpoint to return a JSON document with info for a given word."""
    if language == "english":
        api_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + ENGLISH_API_KEY
    elif language == "spanish":
        api_url = "https://www.dictionaryapi.com/api/v3/references/spanish/json/" + word + SPANISH_API_KEY
    api_json = requests.get(api_url)
    data = json.loads(api_json.text)
    return data


def parse_data(data, word):
    """Parses the Merriam-Webster data for the definitions and type."""
    definitions = data[0]["shortdef"]
    type = data[0]["fl"]
    return {"word": word, "definition": definitions, "type": type}


# ---------- SCRAPER ENDPOINT FOR TEAMMATE ----------
@app.route('/dict_api/<string:search_term>')
def return_definition(search_term):
    """"This API's endpoint which returns the definition of a word if it is found in the master list."""
    master = get_master("english")
    if search_term.upper() in master:
        return {"word": search_term, "definition": master[search_term.upper()]}
    else:
        return {"word": search_term, "definition": "Not found"}


# ---------- MERRIAM-WEBSTER API ----------
@app.route('/english')
def get_english_word():
    # choice() returns a random key:value pair as a tuple where the key is the word
    master = get_master("english")
    word = random.choice(list(master.items()))[0].lower()

    # call the Merriam-Webster English Collegiate endpoint
    data = get_data_from_api("english", word)

    # filter out words not found in Merriam-Webster using recursion
    if not isinstance(data[0], dict):
        return get_english_word()

    # create a dynamic URL and redirect
    return redirect(url_for("return_english_word", word=word))


@app.route('/english/<string:word>', methods=['GET', 'POST'])
def return_english_word(word):
    data = parse_data(get_data_from_api("english", word), word)
    reviews_url = 'http://localhost:8000/get_reviews/' + word
    reviews_json = requests.get(reviews_url)
    all_reviews = json.loads(reviews_json.text)["all_reviews"]

    # parse JSON for the definition, type, and path to the sound file
    return render_template('word.html', data=data, all_reviews=all_reviews)


@app.route('/spanish')
def get_spanish_word():
    # choice() returns a random key:value pair as a tuple where the key is the word
    master = get_master("spanish")
    word = random.choice(master).lower()

    # call the Merriam-Webster Spanish-English endpoint
    data = get_data_from_api("spanish", word)

    # filter out words not found in Merriam-Webster using recursion
    if not isinstance(data[0], dict):
        return get_spanish_word()

    # create a dynamic URL and redirect
    return parse_data(data, word)

# @app.route('/spanish/<string:word>')
# def return_spanish_word(word):
#     data = get_data_from_api("spanish", word)
#
#     # parse JSON for the definition, type, and path to the sound file
#     return parse_data(data, word)
