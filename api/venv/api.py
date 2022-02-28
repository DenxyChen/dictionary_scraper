from flask import Flask, json, request
import requests
import random

app = Flask(__name__)

ENGLISH_KEY = "?key=d2abfab6-ba61-44cd-9d96-48c99eaa363a"
SPANISH_KEY = "?key=87d0bcf4-421f-4845-9543-d96eda5ff20a"


# ---------- HELPER METHODS -----------
def get_master(language):
    """Returns a collection of words from the given language by making a GET request to an online JSON document."""
    if language == "English":
        dictionary_json_url = 'https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json'
    elif language == "Spanish":
        dictionary_json_url = 'https://raw.githubusercontent.com/words/an-array-of-spanish-words/master/index.json'
    dictionary_json = requests.get(dictionary_json_url)
    dictionary = json.loads(dictionary_json.text)
    return dictionary


def get_data_from_api(language, word):
    """Calls the Merriam-Webster endpoint to return a JSON document with info for a given word."""
    if language == "English":
        api_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + ENGLISH_KEY
    elif language == "Spanish":
        api_url = "https://www.dictionaryapi.com/api/v3/references/spanish/json/" + word + SPANISH_KEY
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
    master = get_master("English")
    if search_term.upper() in master:
        return {"word": search_term, "definition": master[search_term.upper()]}
    else:
        return {"word": search_term, "definition": "Not found"}


# ---------- MERRIAM-WEBSTER API ----------
@app.route('/English')
def return_english_word():
    # choice() returns a random key:value pair as a tuple where the key is the word
    master = get_master("English")
    word = random.choice(list(master.items()))[0].lower()

    # call the Merriam-Webster English Collegiate endpoint
    data = get_data_from_api("English", word)

    # filter out words not found in Merriam-Webster using recursion
    if not isinstance(data[0], dict):
        return return_english_word()

    # parse JSON for the definition, type, and path to the sound file
    return parse_data(data, word)


@app.route('/Spanish')
def return_spanish_word():
    # choice() returns a random key:value pair as a tuple where the key is the word
    master = get_master("Spanish")
    word = random.choice(master).lower()

    # call the Merriam-Webster Spanish-English endpoint
    data = get_data_from_api("Spanish", word)

    # filter out words not found in Merriam-Webster using recursion
    if not isinstance(data[0], dict):
        return return_spanish_word()

    # parse JSON for the definition, type, and path to the sound file
    return parse_data(data, word)
