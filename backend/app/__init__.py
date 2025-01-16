from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()

def create_app(routes=None):
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://boxboxAdmin:BoxBox4Life2024@10.0.0.246/safechat'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app