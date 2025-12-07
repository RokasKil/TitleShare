from flask import render_template, Flask
import os
import random
from ..utils.cat import get_random_cat
def register_error_handlers(app: Flask):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html", cat_file_name=get_random_cat(app)), 404