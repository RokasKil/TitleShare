from .database import db

class Preset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    author = db.Column(db.String(256), nullable=True)
    type = db.Column(db.Integer, nullable=False)
    uploader_ip = db.Column(db.String(39), nullable=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    download_count = db.Column(db.Integer, default=0, nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    preset_file_id = db.Column(
        db.Integer,
        db.ForeignKey("preset_file.id", ondelete="SET NULL"),
        nullable=True
    )
    preset_file = db.relationship("PresetFile", backref=db.backref("presets", lazy=True))

class PresetFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    file_hash = db.Column(db.BINARY(32), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.UniqueConstraint("file_hash", "size", name="uq_file_hash_size"),
    )
