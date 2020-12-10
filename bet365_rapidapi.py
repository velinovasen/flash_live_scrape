import requests


def get_odds(game_id):
    url = "https://betsapi2.p.rapidapi.com/v3/bet365/prematch"

    querystring = {"FI": "96446107"}

    headers = {
        'x-rapidapi-key': "5d7b6983f0msh690ced90fc653bap104ef3jsna9c7878604da",
        'x-rapidapi-host': "betsapi2.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)


def upcoming_games():
    url = "https://betsapi2.p.rapidapi.com/v1/bet365/upcoming"
    querystring = {"sport_id": "1"}
    headers = {
        'x-rapidapi-key': "5d7b6983f0msh690ced90fc653bap104ef3jsna9c7878604da",
        'x-rapidapi-host': "betsapi2.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()

    print(data['results'])
    for fixture in data['results']:
        print(fixture)

upcoming_games()