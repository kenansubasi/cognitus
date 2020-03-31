import os

from celery import Celery
from sklearn import cross_validation

from algorithm.helpers import tfidf, test_SVM, dump_model

# Celery Config
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
RESULT_PATH = os.environ.get("RESULT_PATH", "/code/results/")
celery_app = Celery("algorithm", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery_app.task()
def train_task(text, label):
    training, vectorizer = tfidf(text)
    x_train, x_test, y_train, y_test = cross_validation.train_test_split(training, label, test_size=0.25,
                                                                         random_state=0)
    model, accuracy, precision, recall = test_SVM(x_train, x_test, y_train, y_test)
    if not os.path.exists(RESULT_PATH):
        os.makedirs(RESULT_PATH)
    dump_model(model, RESULT_PATH + "model.pickle")
    dump_model(vectorizer, RESULT_PATH + "vectorizer.pickle")

    return "Success"
