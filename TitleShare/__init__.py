from flask import Flask
import os
from .database import db, setup_sqlite_pragma
from .models import *
from .config import AppConfig, Config
from .scheduler import scheduler

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(AppConfig)

    db.init_app(app)
    scheduler.init_app(app)
    

    with app.app_context():
        setup_sqlite_pragma(db)
        # TODO: Proper migrations
        db.create_all()
        print("Database initialized.")
        if not os.path.islink(Config.SHARE_PRESETS_PATH):
            print("Creating", os.path.abspath(Config.SHARE_PRESETS_PATH))
            os.makedirs(Config.SHARE_PRESETS_PATH, exist_ok=True)

    # Register blueprints
    from .routes.share import share_bp
    app.register_blueprint(share_bp, url_prefix="/share")
    if Config.DEBUG:
        print("Debug mode enabled: registering debug routes")
        from .routes.debug import debug_bp
        app.register_blueprint(debug_bp, url_prefix="/share/debug")
    # register error handlers
    from .error_handlers import register_error_handlers
    register_error_handlers(app)
    #start scheduler
    from .tasks import expire
    scheduler.start()
    return app
