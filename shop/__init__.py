from flask import Flask,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES,UploadSet,configure_uploads,patch_request_class
from datetime import timedelta
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_migrate import Migrate
from flask_msearch import Search

import os

basedir=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = 'eeeopopdopeppokakospkoapkaopap'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sparemate_scalingo.db'
db = SQLAlchemy(app)
app.config['UPLOADED_PHOTOS_DEST']=os.path.join(basedir,'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app,photos)
patch_request_class(app) 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u"Please login first"
db = SQLAlchemy(app)
brcypt=Bcrypt(app)



search = Search()
search.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)



app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes
