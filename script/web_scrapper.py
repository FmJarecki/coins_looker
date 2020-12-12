import requests
from bs4 import BeautifulSoup


def download_phrase_from_marker(name, soup_phrase, phrase_key, useless_phrase_length, end_of_phrase):
    response = requests.get('https://coinmarketcap.com/currencies/' + name)
    soup = BeautifulSoup(response.text, "html.parser")
    for short_name_phrase in soup.find_all(soup_phrase):
        short_name_phrase = str(short_name_phrase)
        symbol_iter = short_name_phrase.find(phrase_key)
        if symbol_iter != -1:
            short_name_phrase = short_name_phrase[symbol_iter + useless_phrase_length:]
            quote_iter = short_name_phrase.find(end_of_phrase)
            return short_name_phrase[:quote_iter]


def scrap_all_coins_from_market():
    coins_names = []
    response = requests.get('https://coinmarketcap.com/1')
    soup = BeautifulSoup(response.text, "html.parser")

    for phrase in soup.find_all('script'):
        phrase = str(phrase)
        if phrase[:10].find('<script id') != -1:
            coins_names_iter = [i + 7 for i in range(len(phrase)) if phrase.startswith('name"', i)]
            for name_iter in coins_names_iter:
                quote_iter = phrase[name_iter:].find('"')
                coins_names.append(phrase[name_iter:name_iter + quote_iter])


    return coins_names