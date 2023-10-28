from flask import Flask
# from project.forms import SignupForm,SigninForm
from project.model import db_session,UserAccount
from flask_login import LoginManager
from flask_mail import Mail
# from . import mail
mail = Mail()
def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'arijit nandy'
	app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
	MAIL_USE_TLS = False,
    MAIL_USERNAME = "a.i.e.c.h.t.g13@gmail.com",
    MAIL_PASSWORD = "izkbimepemrceiiy",
	MAIL_DEFAULT_SENDER = "a.i.e.c.h.t.g13@gmail.com"
	)
	# mail = Mail(app)
	from .route import route
	from .auth import auth
	app.register_blueprint(route, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	mail.init_app(app)
	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)
	@login_manager.user_loader
	def load_user(id):
		return db_session.query(UserAccount).filter_by(id=id).first()
	return app

from project import route

