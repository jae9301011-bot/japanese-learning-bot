from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import random
from typing import Dict, List, Optional

app = FastAPI(title="Japanese Learning API")

# Allow CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROGRESS_FILE = os.path.join(DATA_DIR, "user_progress.json")

# Data Models
class ProgressUpdate(BaseModel):
    level: str
    word: str
    status: str  # "correct" or "incorrect"

# Helper Functions
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
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Global Data Cache
vocab_cache = {}

@app.on_event("startup")
async def startup_event():
    # Preload N5 data (expand logic for other levels if needed)
    vocab_cache["n5"] = load_json("vocab_n5.json")
    # Add other levels here if files exist

@app.get("/")
def read_root():
    return {"message": "Japanese Learning API is running!"}

@app.get("/levels")
def get_levels():
    # Scan data directory for vocab_*.json
    levels = []
    if os.path.exists(DATA_DIR):
        for f in os.listdir(DATA_DIR):
            if f.startswith("vocab_") and f.endswith(".json"):
                levels.append(f.replace("vocab_", "").replace(".json", ""))
    return {"levels": sorted(levels)}

@app.get("/word/{level}")
def get_random_word(level: str, retry_incorrect: bool = False):
    # Load data if not in cache
    if level not in vocab_cache:
        vocab_cache[level] = load_json(f"vocab_{level}.json")
    
    words = vocab_cache.get(level, [])
    if not words:
        raise HTTPException(status_code=404, detail=f"No data found for level {level}")

    if retry_incorrect:
        progress = load_progress()
        level_progress = progress.get(level, {})
        incorrect_words = [w for w in words if level_progress.get(w["word"]) == "incorrect"]
        
        if not incorrect_words:
             return {"message": "No incorrect words to retry!", "word": None}
        
        selected = random.choice(incorrect_words)
        return {"word": selected, "mode": "retry"}

    # Normal mode: random word
    selected = random.choice(words)
    return {"word": selected, "mode": "learning"}

@app.get("/progress")
def get_user_progress():
    return load_progress()

@app.post("/progress")
def update_progress(update: ProgressUpdate):
    progress = load_progress()
    
    if update.level not in progress:
        progress[update.level] = {}
        
    progress[update.level][update.word] = update.status
    save_progress(progress)
    return {"status": "success", "updated_word": update.word, "new_status": update.status}

@app.get("/vocab/{level}")
def get_full_vocab(level: str):
    # Returns full list for review table
    vocab_path = os.path.join(DATA_DIR, f"vocab_{level}.json")
    if not os.path.exists(vocab_path):
        return []
    with open(vocab_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/speak")
def speak_word(text: str):
    import subprocess
    try:
        # Use macOS 'say' command (background process)
        subprocess.Popen(["say", "-v", "Kyoko", text])
        return {"status": "playing"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
