from json import dumps

import requests


url_games = "https://api-football-beta.p.rapidapi.com/fixtures"
url_odds = "https://api-football-beta.p.rapidapi.com/odds"

headers = {
    'x-rapidapi-key': "5d7b6983f0msh690ced90fc653bap104ef3jsna9c7878604da",
    'x-rapidapi-host': "api-football-beta.p.rapidapi.com"
    }


def get_odds(game_id):
    querystring = {"date": "2020-12-09", "fixture": game_id}

    response = requests.request("GET", url_odds, headers=headers, params=querystring)

    all_data = response.json()['response']

    all_odds = {}
    all_ids = []
    for league in all_data:
        print(league['fixture'])
        all_ids.append(league['fixture']['id'])

    return all_ids


def get_games():
    querystring = {"date": "2020-12-09"}   # TO ADD AUTO DATE
    response = requests.request("GET", url_games, headers=headers, params=querystring)

    all_data = response.json()['response']

    all_games = {}
    for fixture in all_data:
        all_games[fixture['fixture']['id']] = {
            'timezone': fixture['fixture']['timezone'],
            'date': fixture['fixture']['date'],
            'teams': {
                'home': {'id': fixture['teams']['home']['id'],
                         'name': fixture['teams']['home']['name'],
                         'winner': fixture['teams']['home']['winner']},
                'away': {'id': fixture['teams']['away']['id'],
                         'name': fixture['teams']['away']['name'],
                         'winner': fixture['teams']['away']['winner']},
            },
            'score': {
                'home': fixture['goals']['home'],
                'away': fixture['goals']['away']
            },
            'status': fixture['fixture']['status']['long']
        }

    for key in all_games.keys():
        odds = get_odds(key)
        print(odds)
        print(f'{key} - {all_games[key]}')


get_games()
#print(dumps(all_data, indent=2))