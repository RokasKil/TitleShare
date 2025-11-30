import dotenv
import os
dotenv.load_dotenv()

# Used by logic
class Config:
    DEBUG = os.getenv("DEBUG", "false") in ["1", "true", "True", "TRUE"]
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///titleShare.db")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 2)) # in MB

    DALAMUD_PROTOCOL = os.getenv("DALAMUD_PROTOCOL", "dalamud")

    SHARE_PRESETS_PATH = os.getenv("SHARE_PRESETS_PATH", "presets")
    SHARE_CODE_LENGTH = int(os.getenv("SHARE_CODE_LENGTH", 6))
    SHARE_EXPIRY_DAYS = int(os.getenv("SHARE_EXPIRY_DAYS", 30))
    # how much storage (in MB) to use before deleting expired presets
    SHARE_EXPIRY_STORAGE_THRESHOLD = int(os.getenv("SHARE_EXPIRY_STORAGE_THRESHOLD", 512)) # in MB
    # how much storage (in MB) beofre deleting non-expired presets
    SHARE_STORAGE_THRESHOLD = int(os.getenv("SHARE_STORAGE_THRESHOLD", 1024)) # in MB

# Passed to Flask app
class AppConfig:
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = Config.MAX_CONTENT_LENGTH * 1024 * 1024  # in MB
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'check_same_thread': False,
            'timeout': 20.0,
        },
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 50,
        'echo': False,  # Set to True for debugging
    }