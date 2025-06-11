import requests
import pandas as pd
import time
import json
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")
df_input = pd.read_csv('input_01.csv')


lats = df_input['lat']
longs = df_input['lon']


def api_call(lat, lon):
    # 
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {
        'User-Agent': 'sample/1.0 (sample9487@gmail.com)'
    }
    try:
        time.sleep(1.3)
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status() 
        data = response.json()
        return json.dumps(data)
    
    except Exception as e:
        return json.dumps({"error": str(e)})

# count = 0
# df_input["Address"] = df_input.apply(lambda row: api_call(row['lat'], row['lon'], count), axis=1)

address = []

for i in range(len(lats)):
    if(i % 200 == 0):
        temp = {
            'longitude': longs[:i],
            'latitute': lats[:i],
            'address': address[:i]
        }

        df = pd.DataFrame(temp)
        name = f'output_{i}.csv'
        df.to_csv(name, index=False)
        print(f'file saved - {name}')
        print(datetime.now())
    
    address.append(api_call(lats[i], longs[i]))
    

temp = {
            'longitude': longs,
            'latitute': lats,
            'address': address
        }

df = pd.DataFrame(temp)
df.to_csv('final_output.csv', index=False)

# # Save to CSV
# df_input.to_csv('main-op.csv', index=False)
# print("File saved!!!!!!!")