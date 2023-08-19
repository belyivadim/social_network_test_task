import os
import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

# config app
app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")
app.config["JWT_LIFETIME_IN_SECONDS"] = os.getenv("JWT_LIFETIME_IN_SECONDS")
app.config["JWT_ALGORITHM"] = os.getenv("JWT_ALGORITHM")

db = SQLAlchemy(app)
ma = Marshmallow(app)
