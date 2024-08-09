import requests

API_KEY = '2dd294f1-4f8b-45f6-8b40-a2bacb7a3e8b'
API_KEY2 = 'a29e4edc2bdf8b7dd49d3d973d7324d262c0d295'
url_crypto = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
url_listing = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'


def get_crypto_data(symbol):
    parameters = {
        'symbol': symbol.upper(),
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    response = requests.get(url_crypto, headers=headers, params=parameters)
    if response.status_code == 200:
        data = response.json()
        return data['data'].get(symbol.upper())
    else:
        return None


def get_crypto_price(base, symbol='USD'):
    parameters = {
        'symbol': base.upper(),
        'convert': symbol.upper()
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    response = requests.get(url_crypto, headers=headers, params=parameters)
    if response.status_code == 200:
        data = response.json()
        prices = data['data']
        return round(prices.get(base.upper(), {}).get('quote', {}).get(symbol.upper(), {}).get('price', 0), 10)
    else:
        return None


def get_top_crypto():
    parameters = {
        'limit': 100
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    response = requests.get(url_listing, headers=headers, params=parameters)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        return []


def custom_enumerate(iterable, start=0):
    return enumerate(iterable, start=start)


def get_crypto_news():
    url_news = 'https://cryptopanic.com/api/v1/posts/'
    params = {
        'auth_token': API_KEY2,
        'filter': 'hot',
        'public': 'true',
    }
    response = requests.get(url_news, params=params)
    data = response.json()
    return data['results']


def crypto_for_converter(form):
    top_crypto = get_top_crypto()
    if top_crypto:
        form.fields['from_crypto'].choices = [(crypto['symbol'], crypto['symbol']) for crypto in top_crypto]
        form.fields['to_crypto'].choices = [(crypto['symbol'], crypto['symbol']) for crypto in top_crypto]
