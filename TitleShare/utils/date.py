from ..config import Config
import datetime

def get_expiry_date(days: int = Config.SHARE_EXPIRY_DAYS):
    return get_datetime() + datetime.timedelta(days=int(days))

def get_datetime() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)