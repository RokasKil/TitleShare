from TitleShare.utils.validation import validate_preset
import json
file_name = r"presets\fca4cdc81e3ba21d4c9e6541e057d0a40337c8f2c831f718c8dae53d0955496a_107741.json"

with open(file_name, "r") as f:
    preset_json = json.load(f)
    print(validate_preset(preset_json))