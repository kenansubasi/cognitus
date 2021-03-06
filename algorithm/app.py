import os

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

from algorithm.celery_app import train_task
from algorithm.helpers import load_model

# App
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
RESULTS_PATH = os.environ.get("RESULTS_PATH", "/code/results/")

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
Base = automap_base()
Base.prepare(db.engine, reflect=True)
Data = Base.classes.data_data

@app.route("/train/", methods=["GET"])
def train():
    db.session.query()
    data = db.session.query(Data.text, Data.label).all()

    data_count = len(data)
    response = {
        "count": data_count
    }

    if data_count > 0:
        data = list(zip(*data))
        text_list = data[0]
        label_list = data[1]
        train_task.delay(text_list, label_list)
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(response), 400)


@app.route("/prediction/", methods=["POST"])
def prediction():
    request_data = request.get_json()

    text = request_data.get("text")
    if not text:
        response =  {
            "text": [
                "This field is required!"
            ]
        }
        return make_response(jsonify(response), 400)

    model_file = RESULTS_PATH + "model.pickle"
    vectorizer_file = RESULTS_PATH + "vectorizer.pickle"
    if not os.path.exists(model_file) or  not os.path.exists(vectorizer_file):
        response = {
            "non_field_errors": [
                "Model and Vectorizer data not found. Please train first."
            ]
        }
        return make_response(jsonify(response), 400)

    model = load_model(model_file)
    vectorizer = load_model(vectorizer_file)
    result = model.predict(vectorizer.transform([text]))
    response = {
        "result": result.tolist()
    }
    return make_response(jsonify(response), 200)
