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

all_ids = []

for year in range(from_year,until_year+1):
    
    with open(f"./data/seasons/season_{year}_{league_id}.json", 'r') as f:
        season_json = json.load(f)
        
    ids = [fixture_obj["fixture"]["id"] for fixture_obj in season_json["response"]]
    
    all_ids.extend(ids)
    
    # for i in range(10):
        
    #     base_url = "https://v3.football.api-sports.io/fixtures/?id={id}"

    #     res = requests.get(base_url.format(id=ids[i]), headers=headers)

    #     data = res.json()

    #     #leer entorno de ejecución????
    #     with open(f"./data/matches/{ids[i]}.json", 'w') as f:
    #         json.dump(data, f,ensure_ascii=False)
    
print(all_ids)
