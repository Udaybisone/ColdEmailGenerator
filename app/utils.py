import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_env(key, default=None):
    return os.getenv(key, default)

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
