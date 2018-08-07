from flask import Blueprint, render_template

web = Blueprint('web', __name__)
from app.web import shitu, auth, drift, gift, main, wish


@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404