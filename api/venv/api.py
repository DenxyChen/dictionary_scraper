from flask import Flask, json, Response
import requests
import random
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile("config.py")
app.url_map.strict_slashes = False

ENGLISH_API_KEY = '?key=' + app.config.get("ENGLISH_API_KEY")
ENGLISH_MASTER_PATH = '.\data\english_master.json'
ENGLISH_MASTER_URL = 'https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json'

SPANISH_API_KEY = '?key=' + app.config.get("SPANISH_API_KEY")
SPANISH_MASTER_PATH = '.\data\spanish_master.json'
SPANISH_MASTER_URL = 'https://raw.githubusercontent.com/words/an-array-of-spanish-words/master/index.json'

LANGUAGE_DICT = {"english": {"rel_path": ENGLISH_MASTER_PATH, "url": ENGLISH_MASTER_URL},
                 "spanish": {"rel_path": SPANISH_MASTER_PATH, "url": SPANISH_MASTER_URL}}


# ---------- HELPER METHODS -----------
def get_from_github(language):
    url = LANGUAGE_DICT[language]["url"]
    rel_path = LANGUAGE_DICT[language]["rel_path"]
    abs_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), rel_path)

    dictionary_json = requests.get(url)
    master = json.loads(dictionary_json.text)

    with open(abs_path, 'w+') as to_file:
        json.dump(master, to_file)

    return master


def get_master(language):
    """Returns a collection of words from the given language by making a GET request to an online JSON document."""

    def time_since_last_modified(path):
        last_modified_time = datetime.fromtimestamp(os.stat(path).st_mtime)
        now = datetime.today()
        return (now - last_modified_time).seconds

    rel_path = LANGUAGE_DICT[language]["rel_path"]
    abs_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), rel_path)

    if time_since_last_modified(abs_path) > 120:
        return get_from_github(language)

    with open(abs_path, 'r') as from_file:
        return json.load(from_file)


def get_data_from_api(language, word):
    """Calls the Merriam-Webster endpoint to return a JSON document with info for a given word."""
    if language == "english":
        api_url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/' + word + ENGLISH_API_KEY
    elif language == "spanish":
        api_url = 'https://www.dictionaryapi.com/api/v3/references/spanish/json/' + word + SPANISH_API_KEY
    api_json = requests.get(api_url)
    data = json.loads(api_json.text)
    return data

@app.route('/reviews/<string:word>')
def get_reviews(word):
    reviews_url = 'http://localhost:8000/get_reviews/' + word
    reviews_json = requests.get(reviews_url)
    print(reviews_json)
    all_reviews = json.loads(reviews_json.text)["all_reviews"]
    review_list = []
    for each_review in all_reviews:
        review_list.append(each_review["review"])
    print(review_list)
    review_dict = {"all_reviews": review_list}
    return Response(response=json.dumps(review_dict), status=200, mimetype='application/json')


def parse_data(data, word):
    """Parses the Merriam-Webster data for the definitions and type."""
    definitions = data[0]["shortdef"]
    print(definitions)
    type_of_speech = data[0]["fl"]
    return {"word": word, "definition": definitions, "type": type_of_speech}


# ==================== MICROSERVICE ENDPOINT FOR TEAMMATE ====================
@app.route('/dict_api/<string:search_term>')
def return_definition(search_term):
    """"This program's endpoint which returns the definition of a word if it is found in the master dictionary."""
    master = get_master("english")
    if search_term.upper() in master:
        return {"word": search_term, "definition": master[search_term.upper()]}
    else:
        return {"word": search_term, "definition": "Not found"}


# ==================== MERRIAM-WEBSTER API ROUTES ====================
@app.route('/english')
def send_english_word_data():
    """
    Sends a Response containing a JSON with a randomly selected English word's definition and figure of speech.
    Additionally includes the URL to an external audio recording of the word's pronunciation.
    """
    def select_random_english_word(word_dict):
        """
        Randomly selects a word and calls the Merriam-Webster API to get the required data. API calls for words that
        have the required data return a JSON that contains a Python dictionary at index 0. All other words are removed
        from the master and a recusrive call to this function is made to select a new word.
        """
        # choice() returns a random key:value pair as a tuple where the key is the word
        word = random.choice(list(word_dict.items()))[0].lower()

        # call the Merriam-Webster English Collegiate endpoint
        dict_data = get_data_from_api("english", word)

        # filter out words not found in Merriam-Webster using recursion
        if not isinstance(dict_data[0], dict):
            return select_random_english_word(word_dict)

        return parse_data(dict_data, word)

    master = get_master("english")
    try:
        data = select_random_english_word(master)
    except RecursionError:
        return Response(status=500)
    return Response(response=json.dumps(data), status=200, mimetype='application/json')


@app.route('/spanish')
def send_spanish_word_data():
    def select_random_spanish_word(word_list):
        # choice() returns a random key:value pair as a tuple where the key is the word
        word = random.choice(word_list).lower()

        # call the Merriam-Webster Spanish-English endpoint
        dict_data = get_data_from_api("spanish", word)

        # filter out words not found in Merriam-Webster using recursion
        if not isinstance(dict_data[0], dict):
            return select_random_spanish_word(word_list)

        # create a dynamic URL and redirect
        return parse_data(dict_data, word)

    master = get_master("spanish")
    try:
        data = select_random_spanish_word(master)
    except RecursionError:
        return Response(status=500)
    return Response(response=json.dumps(data), status=200, mimetype='application/json')


# ==================== JINJA2 TEMPLATING AND URL_FOR REDIRECT ====================
# @app.route('/english/<string:word>', methods=['GET', 'POST'])
# def return_english_word(word):
#     data = parse_data(get_data_from_api("english", word), word)

#     reviews_url = 'http://localhost:8000/get_reviews/' + word
#     reviews_json = requests.get(reviews_url)
#     all_reviews = json.loads(reviews_json.text)["all_reviews"]
#     # parse JSON for the definition, type, and path to the sound file
#     return render_template('word.html', data=data, all_reviews=all_reviews)

# @app.route('/spanish/<string:word>')
# def return_spanish_word(word):
#     data = get_data_from_api("spanish", word)
#
#     # parse JSON for the definition, type, and path to the sound file
#     return parse_data(data, word)
