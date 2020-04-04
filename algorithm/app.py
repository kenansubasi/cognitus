import os
import datetime

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

from algorithm.celery_app import train_task
from algorithm.helpers import load_model

from conf.constants import RESULTS_PATH, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DBNAME


# App
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# DB Config
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://{user}:{password}@{host}:{port}/{dbname}".format(
    user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT, dbname=POSTGRES_DBNAME
)
db = SQLAlchemy(app)
Base = automap_base()
Base.prepare(db.engine, reflect=True)
Data = Base.classes.data_data
Train = Base.classes.data_train


@app.route("/train/", methods=["GET"])
def train():
    last_train = db.session.query(Train.task_id).order_by(Train.id.desc()).first()
    if last_train != None:
        last_train_state = train_task.AsyncResult(last_train.task_id).state
        if last_train_state == "PENDING":
            response = {
                "non_field_errors": [
                    "Please wait for the last train to end!"
                ]
            }
            return make_response(jsonify(response), 400)

    data = db.session.query(Data.text, Data.label).all()
    data_count = len(data)
    if data_count > 0:
        data = list(zip(*data))
        text_list = data[0]
        label_list = data[1]

        task = train_task.delay(text_list, label_list)
        today = datetime.datetime.now()
        train = Train(task_id=task.task_id, created_at=today, updated_at=today)
        db.session.add(train)
        db.session.commit()

        response = {
            "count": data_count,
            "task_id": task.task_id
        }
        return make_response(jsonify(response), 200)
    else:
        response = {
            "non_field_errors": [
                "Data not found!"
            ]
        }
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
