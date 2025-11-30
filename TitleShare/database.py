from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
db = SQLAlchemy()

def setup_sqlite_pragma(db_instance):
    @event.listens_for(db_instance.engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA busy_timeout=20000")
        cursor.close()
