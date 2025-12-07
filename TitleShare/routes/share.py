from flask import Blueprint, request, jsonify, render_template, abort, current_app
from werkzeug.utils import secure_filename
import json
from ..config import Config
from ..models import *
from ..database import db
from ..utils.share import generate_share_code
from ..utils.preset_file import write_preset_file, read_preset_file, get_hash
from ..utils.date import get_expiry_date, get_datetime
from ..utils.validation import validate_preset
from ..utils.cat import get_random_cat

share_bp = Blueprint("share", __name__)

@share_bp.route("", methods=["POST"])
def share_preset():
    data = request.get_json()
    preset_json = data["preset"]

    if not validate_preset(preset_json):
        print(f"{request.remote_addr} - Failed preset validation")
        return jsonify({"error": "Invalid preset format"}), 400

    preset_bytes = json.dumps(preset_json).encode("utf-8")
    hash = get_hash(preset_bytes)

    preset_file = PresetFile.query.filter_by(file_hash=hash, size=len(preset_bytes)).first()
    if not preset_file:
        preset_file = PresetFile(
            name=f"{hash.hex()}_{len(preset_bytes)}",
            file_hash=hash, 
            size=len(preset_bytes)
        )
    
    preset = Preset(
        name=preset_json["Name"],
        author=preset_json.get("Author"),
        type=preset_json["LocationModel"]["LocationType"],
        uploader_ip=request.remote_addr,
        code=generate_share_code(),
        upload_date=get_datetime(),
        expiry_date=get_expiry_date(),
        preset_file = preset_file
    )
    db.session.add(preset)
    write_preset_file(preset_file.name, preset_bytes)
    db.session.commit()
    
    print(f"{request.remote_addr} - {preset.code} - Uploaded preset file")
    return jsonify({"code": preset.code}), 201

@share_bp.route("/<code>", methods=["GET"])
def get_share(code):
    print(f"{request.remote_addr} - {code} - Getting")
    preset = Preset.query.filter_by(code=code).first()
    if not preset:
        abort(404)
    if preset.deleted:
        return render_template("expired.html", preset=preset, cat_file_name=get_random_cat(current_app)), 410
    print(f"[{request.remote_addr}][{preset.code}] Getting")
    return render_template("share.html", preset=preset, dalamudUrl=f"{Config.DALAMUD_PROTOCOL}://plugin/TitleEdit/importShared?code={preset.code}")

@share_bp.route("/file/<code>", methods=["GET"])
def get_share_file(code: str):
    print(f"{request.remote_addr} - {code} - Serving preset file")
    preset = Preset.query.filter_by(code=code).first()
    if not preset:
        return jsonify({"error": "Preset not found"}), 404
    if preset.deleted:
        return jsonify({"error": "Preset has expired"}), 410
    preset_file_content = read_preset_file(preset.preset_file.name)
    preset.download_count += 1
    db.session.add(preset)
    db.session.commit()
    return preset_file_content, 200, {
        'Content-Type': 'application/json',
        # TODO: Maybe figure out a better way to escape the name cause this is way too aggresive
        "Content-Disposition": f"attachment; filename={secure_filename(preset.name)}.json"
    }
    
