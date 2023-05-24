import requests
import json

with open('config.json', 'r') as f:
    config = json.load(f)

api_key = config["api_keys"][0]

from_year = config["season_from"]
until_year = config["season_until"]
league_id = config["league_id"]

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': api_key
    }

for year in range(from_year,until_year+1):

    base_url = "https://v3.football.api-sports.io/fixtures/?season={season_year_start}&league={league_id}"

    res = requests.get(base_url.format(season_year_start=year,league_id=league_id), headers=headers)

    data = res.json()

    #leer entorno de ejecución????
    with open(f"./data/seasons/season_{year}_{league_id}.json", 'w') as f:
        json.dump(data, f,ensure_ascii=False)
