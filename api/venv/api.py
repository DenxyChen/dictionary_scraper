from flask import Flask, json, request
import requests
import random

app = Flask(__name__)


def get_master():
    dictionary_json_url = 'https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json'
    dictionary_json = requests.get(dictionary_json_url)
    dictionary = json.loads(dictionary_json.text)
    return dictionary

@app.route('/dict_api/<string:search_term>')
def return_definition(search_term):
    master = get_master()
    if search_term.upper() in master:
        return {"word": search_term, "definition": master[search_term.upper()]}
    else:
        return {"word": search_term, "definition": "Not found"}

# ----- Meriam-Webster API WIP -----
#     # choice() returns a random key:value pair as a tuple where the key is the word
#     word = random.choice(list(dictionary.items()))[0].lower()
#     api_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?key=d2abfab6-ba61-44cd-9d96-48c99eaa363a"
#     return api_url
#     # api_json = requests.get(api_url)
#     # data = json.loads(api_json.text)
#     # definition = data[0]["def"]
#     # return {'word': word, "def": definition}
#
# print(return_random_word())