from ..config import Config
from ..models import Preset
import random
import string

def generate_share_code(length: int = Config.SHARE_CODE_LENGTH):
    while True:
        code = ''.join(random.choice(string.ascii_letters) for _ in range(int(length)))
        if not Preset.query.filter_by(code=code).first():
            return code