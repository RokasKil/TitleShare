import os
import random
from flask import Flask
def get_random_cat(app: Flask) -> str:
    static_path = app.static_folder
    return "cat/" + random.choice(os.listdir(os.path.join(static_path, "cat")))