from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # ✅ Set Secret Key and Database Configuration
    app.config['SECRET_KEY'] = 'bqidfbiwfwiucwuicbwiiwnfw'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/mydb'
    
    db.init_app(app)
    
    # ✅ Import blueprints
    from .views import views
    from .auth import auth
    
    # ✅ Fix typo in 'url_prefix'
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .modules import User, Project, Quranversions, Voices
    
    # ✅ Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.sign_in'  # Make sure 'sign_in' is correctly defined in 'auth.py'
    login_manager.init_app(app)

    # ✅ Flask-Login expects ID from get_id()
    @login_manager.user_loader   
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ✅ Debugging
    app.config['DEBUG'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    return app
