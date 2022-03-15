from flask import Flask, json, redirect, url_for, render_template, request
import requests
import random
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_pyfile("config.py")
app.url_map.strict_slashes = False

ENGLISH_API_KEY = "?key=" + app.config.get("ENGLISH_API_KEY")
ENGLISH_MASTER_PATH = '.\data\english_master.json'
ENGLISH_MASTER_URL = 'https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json'

SPANISH_API_KEY = "?key=" + app.config.get("SPANISH_API_KEY")
SPANISH_MASTER_PATH = '.\data\spanish_master.json'
SPANISH_MASTER_URL = 'https://raw.githubusercontent.com/words/an-array-of-spanish-words/master/index.json'


# ---------- HELPER METHODS -----------
def get_master(language):
    """Returns a collection of words from the given language by making a GET request to an online JSON document."""

    def update_local_file(dictionary_json_url, path):
        dictionary_json = requests.get(dictionary_json_url)
        master = json.loads(dictionary_json.text)

        with open(path, "w+") as to_file:
            json.dump(master, to_file)

        return master

    def time_since_last_modified(path):
        last_modified_time = datetime.fromtimestamp(os.stat(path).st_mtime)
        now = datetime.today()

        return (now - last_modified_time).seconds

    language_dict = {"english": {"rel_path": ENGLISH_MASTER_PATH, "url": ENGLISH_MASTER_URL},
                     "spanish": {"rel_path": SPANISH_MASTER_PATH, "url": SPANISH_MASTER_URL}}

    rel_path = language_dict[language]["rel_path"]
    url = language_dict[language]["url"]
    abs_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), rel_path)

    if time_since_last_modified(abs_path) > 120:
        return update_local_file(url, abs_path)

    with open(abs_path, 'r') as from_file:
        return json.load(from_file)


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
    # return redirect(url_for("return_english_word", word=word))
    return parse_data(get_data_from_api("english", word), word)


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

print(get_english_word())
