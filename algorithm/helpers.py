import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import precision_score, accuracy_score, recall_score


# feature extraction - creating a tf-idf matrix
def tfidf(data, ma=0.6, mi=0.0001):
    tfidf_vectorize = TfidfVectorizer()
    tfidf_data = tfidf_vectorize.fit_transform(data)
    return tfidf_data, tfidf_vectorize


# SVM classifier
def test_SVM(x_train, x_test, y_train, y_test):
    SVM = SVC(kernel='linear')
    SVMClassifier = SVM.fit(x_train, y_train)
    predictions = SVMClassifier.predict(x_test)
    a = accuracy_score(y_test, predictions)
    p = precision_score(y_test, predictions, average='weighted')
    r = recall_score(y_test, predictions, average='weighted')
    return SVMClassifier, a, p, r


def dump_model(model, file_output):
    pickle.dump(model, open(file_output, 'wb'))


def load_model(file_input):
    return pickle.load(open(file_input, 'rb'))
