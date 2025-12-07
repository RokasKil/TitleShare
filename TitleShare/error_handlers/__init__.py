from flask import Flask

def register_error_handlers(app: Flask):
    from .handler_404 import register_error_handlers
    handler_404.register_error_handlers(app)