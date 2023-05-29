import requests
import json
import time
import os
import glob

with open('config.json', 'r') as f:
    config = json.load(f)

api_keys = config["api_keys"]

from_year = config["season_from"]
until_year = config["season_until"]
league_id = config["league_id"]

next_id_index = config["next_id_index"]

sub_ids = config["fixtures_ids"][next_id_index:]

last_id_saved = next_id_index -1


def obtener_ids_no_obtenidos_y_fallidos(ids_totales, ids_fallidos, ids_obtenidos):
    ids_no_obtenidos = list(ids_totales - ids_obtenidos)
    
    ids_fallidos.extend([id for id in ids_obtenidos if id in ids_fallidos])
    ids_fallidos.extend(ids_no_obtenidos)
    return ids_fallidos


def obtener_ids_desde_carpeta(carpeta):
    archivos_json = glob.glob(os.path.join(carpeta, "*.json"))
    ids = []

    for archivo in archivos_json:
        nombre_archivo = os.path.basename(archivo)
        id = os.path.splitext(nombre_archivo)[0]
        ids.append(int(id))

    return ids

# Ejemplo de uso
carpeta = "./data/matches/"


for api_key in api_keys:
    headers = {
        'x-apisports-key': api_key,
        'x-rapidapi-host': "v3.football.api-sports.io"        
        }
    
    obtenidos = obtener_ids_desde_carpeta(carpeta).copy()
    todos = config["fixtures_ids"].copy()
    fallidos = config["error_ids"].copy()
            
    resultado = [id for id in fallidos]

    resultado_2 = [id for id in todos if id not in obtenidos]

    resultado.extend(resultado_2)
 
    for i,id in enumerate(resultado):
        
        if i > 1000:
            print("quota limit close, breaking for next api")
            break
        
        base_url = "https://v3.football.api-sports.io/fixtures/?id={id}"

        res = requests.get(base_url.format(id=id), headers=headers)

        data = res.json()
        # print(data)
        
        # print("Waiting 7 seconds, api key: ",api_key, " match_id: ",id)
        print("Api key: ",api_key, " match_id: ",id)

        time.sleep(0.3)
        
        if data["errors"]:
            print("Failed ",id, " error: ", data["errors"])
        else:
            #leer entorno de ejecución????
            try:
                with open(f"./data/matches/{id}.json", 'w') as f:
                    json.dump(data, f)
            except Exception as e:
                print("Failed ",id, " error: ", e)
