from flask import Blueprint, jsonify
from ..models import *
from ..database import db

debug_bp = Blueprint("debug", __name__)

@debug_bp.route("/delete/file/<code>", methods=["GET"])
def debug_delete_file(code: str):
    preset = Preset.query.filter_by(code=code).first()
    if not preset:
        return jsonify({"error": "Preset not found"}), 404
    db.session.delete(preset.preset_file)
    db.session.commit()
    return "ok", 200

@debug_bp.route("/expire/<code>", methods=["GET"])
def debug_expire_share(code: str):
    preset = Preset.query.filter_by(code=code).first()
    if not preset:
        return jsonify({"error": "Preset not found"}), 404
    preset.deleted = True
    db.session.add(preset)
    db.session.commit()
    return "ok", 200


@debug_bp.route("/delete/<code>", methods=["GET"])
def debug_delete_share(code: str):
    preset = Preset.query.filter_by(code=code).first()
    if not preset:
        return jsonify({"error": "Preset not found"}), 404
    db.session.delete(preset)
    db.session.commit()
    return "ok", 200
