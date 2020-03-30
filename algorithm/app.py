from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy

from algorithm.celery_app import debug_task


app = Flask(__name__)

# DB Config
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://cognitus:secret@db:5432/cognitus"
db = SQLAlchemy(app)
Data = db.Table("data_data", db.metadata, autoload=True, autoload_with=db.engine)


@app.route('/train/')
def train():
    debug_task.delay()
    data_count = db.session.query(Data).count()
    response = make_response({"data": {"count": data_count}}, 200)
    return response
