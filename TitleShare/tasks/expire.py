from sqlalchemy.sql import func

from ..scheduler import scheduler
from ..database import db
from ..models import *
from ..config import Config
from ..utils.preset_file import delete_preset_file
from ..utils.date import get_datetime
@scheduler.task(
    "interval",
    id="test",
    minutes=30,
    next_run_time=get_datetime(),  # Run first time when scheduler starts
)
def expiry_task():
    print("Running expiry task...")
    with scheduler.app.app_context():
        # This won't be accurate when dealing with lots of small files but surely it will be close enough
        total_size = db.session.query(func.sum(PresetFile.size)).scalar() or 0
        print("Current storage usage (bytes):", total_size)
        if Config.SHARE_STORAGE_THRESHOLD != 0 and total_size >= Config.SHARE_STORAGE_THRESHOLD * 1024 * 1024:
            while total_size >= Config.SHARE_STORAGE_THRESHOLD * 1024 * 1024:
                # Delete oldest non-deleted preset
                preset = Preset.query.filter_by(deleted=False).order_by(Preset.expiry_date).first()
                if not preset:
                    break
                total_size -= expire_preset(preset)
        while total_size >= Config.SHARE_EXPIRY_STORAGE_THRESHOLD * 1024 * 1024:
            # Delete oldest preset
            preset = Preset.query.filter(Preset.deleted == False, Preset.preset_file_id.isnot(None), Preset.expiry_date < func.now()).order_by(Preset.expiry_date).first()
            if not preset:
                break
            total_size -= expire_preset(preset)
    print("Running expiry task finished.")

def expire_preset(preset: Preset) -> int:
    print(f"Expiring preset:", preset.code)
    freed_bytes = 0
    delete_file_name = None
    preset.deleted = True
    db.session.add(preset)
    if preset.preset_file:
        preset_file = preset.preset_file
        non_deleted_count = db.session.query(func.count()).group_by(Preset.preset_file_id).filter(Preset.preset_file_id == preset_file.id, Preset.deleted == False, Preset.id != preset.id).scalar() or 0
        print("Non deleted count:", non_deleted_count)
        if non_deleted_count == 0:
            freed_bytes = preset_file.size
            delete_file_name = preset_file.name
            db.session.delete(preset_file)
    db.session.commit()
    if delete_file_name is not None:
        delete_preset_file(preset_file.name)
    return freed_bytes