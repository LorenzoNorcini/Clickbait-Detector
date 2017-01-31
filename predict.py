import cPickle as pickle
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import sys

def tokenize(text):
    lmtzr = WordNetLemmatizer()
    tokens = nltk.word_tokenize(text)
    l = []
    for t in tokens:
        try:
            t = float(t)
            l.append("<NUM>")
        except ValueError:
            l.append(lmtzr.lemmatize(t))
    return l


def predict(headline):
    try:
        f = open('trained_model')
        clf = pickle.load(f)
        f = open('vectorizer')
        vectorizer = pickle.load(f)
        return clf.predict_proba(vectorizer.transform(headline))[0][1]
    except IOError:
        print("Model not present, run train.py first")


if __name__ == "__main__":
    print "headline is " + str(int(predict([sys.argv[1]])*100)) + "% likely to be clickbait"

