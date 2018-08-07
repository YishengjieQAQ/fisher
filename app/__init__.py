from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from app.models.base import db


#创建核心示例对象app
login_manager = LoginManager()
mail = Mail()
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'

    mail.init_app(app)
    # login_manager.login_message = '访问该网页需要先进行登录'
    with app.app_context():
        '''通过with语句来让数据库连接核心对象app'''
        db.create_all()
    return app
#注册蓝图
def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)

