import requests
import json
import os

DATA_DIR = "data"
N5_URL = "https://raw.githubusercontent.com/elzup/jlpt-word-list/master/json/n5.json"
OUTPUT_FILE = os.path.join(DATA_DIR, "vocab_n5.json")

def fetch_vocabulary():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    print(f"Downloading N5 vocabulary from {N5_URL}...")
    try:
        response = requests.get(N5_URL)
        response.raise_for_status()
        
        data = response.json()
        
        # Verify structure
        print(f"Successfully downloaded {len(data)} words.")
        print("Sample data:")
        print(json.dumps(data[:3], indent=2, ensure_ascii=False))
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Saved to {OUTPUT_FILE}")
        return True
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return False

if __name__ == "__main__":
    fetch_vocabulary()
