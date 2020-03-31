import os

from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy

from algorithm.celery_app import train_task

# App
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# DB Config
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DBNAME = os.environ.get("POSTGRES_DBNAME")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://{user}:{password}@{host}:{port}/{dbname}".format(
    user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT, dbname=POSTGRES_DBNAME
)
db = SQLAlchemy(app)
Data = db.Table("data_data", db.metadata, autoload=True, autoload_with=db.engine)


@app.route('/train/')
def train():
    data = db.session.query(Data).all()
    text_list = []
    label_list = []

    for item in data:
        text_list.append(item.text)
        label_list.append(item.label)

    data_count = len(text_list)
    data = {
        "count": data_count
    }

    if data_count > 0:
        train_task.delay(text_list, label_list)
        return make_response(data, 200)
    else:
        return make_response(data, 400)
