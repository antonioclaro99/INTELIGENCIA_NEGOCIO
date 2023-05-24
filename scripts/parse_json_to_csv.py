import os
import json
import pandas as pd

# assign directory
directory = "./data/matches/"

df_matches = pd.read_csv("./data/matches_csv/matches.csv",sep=";",index_col=0)

errors_id = []

# iterate over files in
# that directory
for filename in os.listdir(directory):
    json_file = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(json_file):
        with open(json_file, 'r',encoding='latin-1') as f:
            #print(json_file)
            fixture_json = json.load(f)
            df_fixture = pd.read_csv("./data/matches_csv/matches_template.csv",sep=";")
            #print(fixture_json)
            if fixture_json["errors"]:
                errors_id.append(fixture_json['parameters']['id'])
            else:
                df_fixture["fixture_id"] = fixture_json["response"][0]["fixture"]["id"]
                df_fixture["date"] = fixture_json["response"][0]["fixture"]["date"]
                df_fixture["season"] = fixture_json["response"][0]["league"]["season"]
                df_fixture["league_id"] = fixture_json["response"][0]["league"]["id"]
                df_fixture["league_name"] = fixture_json["response"][0]["league"]["name"]
                df_fixture["league_logo"] = fixture_json["response"][0]["league"]["logo"]
                df_fixture["country_name"] = fixture_json["response"][0]["league"]["country"]
                df_fixture["country_logo"] = fixture_json["response"][0]["league"]["season"]

                df_fixture["home_team_id"] = fixture_json["response"][0]["teams"]["home"]["id"]
                df_fixture["home_team_name"] = fixture_json["response"][0]["teams"]["home"]["name"]
                df_fixture["home_team_img"] = fixture_json["response"][0]["teams"]["home"]["logo"]
                df_fixture["away_team_id"] = fixture_json["response"][0]["teams"]["away"]["id"]
                df_fixture["away_team_name"] = fixture_json["response"][0]["teams"]["away"]["name"]
                df_fixture["away_team_img"] = fixture_json["response"][0]["teams"]["away"]["logo"]
                
                
                
                df_fixture["home_goals"] = fixture_json["response"][0]["goals"]["home"]
                df_fixture["away_goals"] = fixture_json["response"][0]["goals"]["away"]
                
                statistics_matrix = [list(df_fixture)[16:33],list(df_fixture)[33:]]
                            
                for i,statistics in enumerate(statistics_matrix):
                    for j,statistic in enumerate(statistics):
                        try:
                            df_fixture[statistic] = fixture_json["response"][0]["statistics"][i]["statistics"][j]["value"]
                        except:
                            df_fixture[statistic] = None
                            
                df_matches = pd.concat([df_matches,df_fixture],ignore_index=True)
            

df_matches.to_csv("./data/matches_csv/matches3.csv",sep=";")

with open('config.json', 'r') as f:
    config = json.load(f)
    
config["error_ids"] = errors_id

with open('config.json', "w") as f:
    json.dump(config, f)