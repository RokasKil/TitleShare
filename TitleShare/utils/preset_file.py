import os
import hashlib
from ..config import Config

def get_preset_path(name: str) -> str: 
    return os.path.join(os.path.join(Config.SHARE_PRESETS_PATH, f"{name}.json"))

def get_hash(preset: bytes) -> bytes:
    return hashlib.sha256(preset).digest()

def write_preset_file(name: str, preset: bytes):
    with open(get_preset_path(name), "wb") as f: 
        f.write(preset)
        
def read_preset_file(name: str) -> str:
    with open(get_preset_path(name), "r") as f: 
        return f.read()
    
def delete_preset_file(name: str):
    os.remove(get_preset_path(name))