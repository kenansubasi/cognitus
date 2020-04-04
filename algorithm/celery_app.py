import os

from celery import Celery
from sklearn import cross_validation

from algorithm.helpers import tfidf, test_SVM, dump_model
from conf.constants import RESULTS_PATH, CELERY_BROKER_URL, CELERY_RESULT_BACKEND


# Celery Config
celery_app = Celery("algorithm", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery_app.task()
def train_task(text, label):
    training, vectorizer = tfidf(text)
    x_train, x_test, y_train, y_test = cross_validation.train_test_split(training, label, test_size=0.25,
                                                                         random_state=0)
    model, accuracy, precision, recall = test_SVM(x_train, x_test, y_train, y_test)
    if not os.path.exists(RESULTS_PATH):
        os.makedirs(RESULTS_PATH)
    dump_model(model, RESULTS_PATH + "model.pickle")
    dump_model(vectorizer, RESULTS_PATH + "vectorizer.pickle")

    return "Success"
