from flask import Flask
from models import *
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


URL = "server://username:password@localhost:port/name_of_database"


engine = create_engine(URL)

if not database_exists(engine.url):
    create_database(engine.url)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()