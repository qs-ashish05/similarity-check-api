import requests
import pandas as pd
import time
import json
import warnings
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import threading

warnings.filterwarnings("ignore")
df_input = pd.read_csv('input_01.csv')

lats = df_input['lat']
longs = df_input['lon']

# Create a session for connection reuse
session = requests.Session()
lock = threading.Lock()

def api_call(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {
        'User-Agent': 'sample/1.0 (sample9487@gmail.com)'
    }
    try:
        with lock:
            time.sleep(0.8)  # Slightly reduced sleep time
        response = session.get(url, headers=headers, verify=False)
        response.raise_for_status() 
        data = response.json()
        return json.dumps(data)
    
    except Exception as e:
        return json.dumps({"error": str(e)})

address = []

# Process in batches with threading
batch_size = 100
max_workers = 3

for batch_start in range(0, len(lats), batch_size):
    batch_end = min(batch_start + batch_size, len(lats))
    batch_indices = list(range(batch_start, batch_end))
    
    print(f"Processing batch {batch_start//batch_size + 1}: items {batch_start+1}-{batch_end} at {datetime.now()}")
    
    # Use threading for current batch
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(api_call, lats[i], longs[i]): i 
            for i in batch_indices
        }
        
        batch_results = [None] * len(batch_indices)
        for future in future_to_index:
            index = future_to_index[future]
            batch_results[index - batch_start] = future.result()
    
    address.extend(batch_results)
    
    # Save progress every 200 items (keeping your original logic)
    if (batch_end) % 200 == 0 or batch_end == len(lats):
        temp = {
            'longitude': longs[:batch_end],
            'latitute': lats[:batch_end],
            'address': address[:batch_end]
        }
        
        df = pd.DataFrame(temp)
        name = f'output_{batch_end}.csv'
        df.to_csv(name, index=False)
        print(f'file saved - {name}')
        print(datetime.now())

temp = {
    'longitude': longs,
    'latitute': lats,
    'address': address
}

df = pd.DataFrame(temp)
df.to_csv('final_output.csv', index=False)
print("Processing complete!")