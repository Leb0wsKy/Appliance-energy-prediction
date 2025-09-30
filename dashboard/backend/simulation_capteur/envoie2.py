import pandas as pd
import time
import requests
import matplotlib.pyplot as plt
import os
# Simulation de l'envoi des données de consommation d'énergie à l'API
print(os.getcwd()) 

script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_dir, "merged_data.csv"))
merged_df=df
print(merged_df.head())

print(f"Nombre de lignes à envoyer : {merged_df.shape[0]}")

API_URL = "http://localhost:5000/api/measurements"
USER_ID = "68d8592d6cd53946712b109b" # Remplace par l'ID utilisateur réel (ici le admin)

for index, row in merged_df.iterrows():
    payload = {
        "userId": USER_ID,
        "timestamp": row["Timestamp"],
        "globalConsumption": float(row["active"]),
        "measurements": {
            "Refrigeration": float(row["Réfrigération"]),
            "Climatisation": float(row["Climatisation"]),
            "AppareilInformatique": float(row["AppareilInformatique"])
        }
    }

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 201 or response.status_code == 200:
            print(f"[{index+1}/{len(merged_df)}]  OK")
        else:
            print(f"[{index+1}/{len(merged_df)}] Erreur {response.status_code} | {response.text}")
    except Exception as e:
        print(f"[{index+1}/{len(merged_df)}] Exception : {e}")

    time.sleep(2)  
print("Envoi terminé ")
