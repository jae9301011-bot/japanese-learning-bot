import os
import json
import random

# Dynamic Path Handling
# Try to find data directory relative to this file, or project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR) # web_app/..
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# If not found (e.g. differently structured deployment), try local 'data'
if not os.path.exists(DATA_DIR):
    DATA_DIR = os.path.join(BASE_DIR, "data")

PROGRESS_FILE = os.path.join(DATA_DIR, "user_progress.json")

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_progress(data):
    # Ensure directory exists
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_levels():
    levels = []
    if os.path.exists(DATA_DIR):
        for f in os.listdir(DATA_DIR):
            if f.startswith("vocab_") and f.endswith(".json"):
                levels.append(f.replace("vocab_", "").replace(".json", ""))
    return sorted(levels)

def get_random_word_logic(level, retry_incorrect=False):
    words = load_json(f"vocab_{level}.json")
    if not words:
        return None

    if retry_incorrect:
        progress = load_progress()
        level_progress = progress.get(level, {})
        incorrect_words = [w for w in words if level_progress.get(w["word"]) == "incorrect"]
        
        if not incorrect_words:
             return None
        
        return random.choice(incorrect_words)

    return random.choice(words)

def update_progress_logic(level, word, status):
    progress = load_progress()
    if level not in progress:
        progress[level] = {}
    progress[level][word] = status
    save_progress(progress)

def get_full_vocab_logic(level):
    return load_json(f"vocab_{level}.json")
