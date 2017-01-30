from sklearn.feature_extraction.text import TfidfVectorizer
import dataset_builder
import cPickle as pickle
from sklearn import metrics
import model_selection
from sklearn import svm
from nltk.stem.wordnet import WordNetLemmatizer
import nltk


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

with open('wordsEn.txt') as f:
    voc = f.read().splitlines()

print "\nProcessing dataset\n"
vectorizer = TfidfVectorizer(tokenizer=tokenize,
                             stop_words='english',
                             lowercase=True,
                             min_df=2,
                             analyzer="word",
                             ngram_range=(1, 3))

try:
    f = open('NTRD')
    titles = pickle.load(f)
except IOError:
    print('Dataset File not present. Creating...')
    dataset_builder.download_reddit_news_data()
    f = open('NTRD')
    titles = pickle.load(f)

train_labels = [0]*len(titles["train"]["0"]) + [1]*len(titles["train"]["1"])
validation_labels = [0]*len(titles["validation"]["0"]) + [1]*len(titles["validation"]["1"])
test_labels = [0]*len(titles["test"]["0"]) + [1]*len(titles["test"]["1"])

train_set = titles["train"]["0"] + titles["train"]["1"]
validation_set = titles["validation"]["0"] + titles["validation"]["1"]
test_set = titles["test"]["0"] + titles["test"]["1"]

print "Train size: " + str(len(train_labels))
print "Validazion size: " + str(len(validation_labels))
print "Test size: " + str(len(test_labels))

train_set = vectorizer.fit_transform(train_set, train_labels)
validation_set = vectorizer.transform(validation_set)
test_set = vectorizer.transform(test_set)

print  "\nTrain matrix shape: " + str(train_set.shape)
print  "Validation matrix shape: " + str(validation_set.shape)
print  "Test matrix shape: " + str(test_set.shape)

with open("vectorizer", 'wb') as f:
    pickle.dump(vectorizer, f)

params = {'kernel': 'rbf', 'C': 2, 'gamma': 1}

re_select_model = False

if re_select_model:
    print "\nTuning hyperparameters..."

    clf, best_params = model_selection.get_best_SVM_model(train_set, train_labels, 5)

    print "Training with hyperparameters: \n " + str(best_params)

else:
    clf = svm.SVC(C=params['C'], kernel=params['kernel'], gamma=params['gamma'], probability=True)


re_fit_model = True

if re_fit_model:
    print "\nFitting Model"
    clf.fit(train_set, train_labels)
    print "Saving model"
    with open("trained_model", 'wb') as f:
        pickle.dump(clf, f)
else:
    try:
        f = open('trained_model')
        clf = pickle.load(f)
    except IOError:
        print('Dataset File not present. Creating...')

predictions = clf.predict(train_set)

print "\nTrain set"

print "\nAccuracy Score: " + str(metrics.accuracy_score(predictions, train_labels))
print "F1 Score: " + str(metrics.f1_score(predictions, train_labels))
print "Recall: " + str(metrics.recall_score(predictions, train_labels))
print "Precision: " + str(metrics.precision_score(predictions, train_labels))

predictions = clf.predict(validation_set)

print "\nValidation set"

print "\nAccuracy Score: " + str(metrics.accuracy_score(predictions, validation_labels))
print "F1 Score: " + str(metrics.f1_score(predictions, validation_labels))
print "Recall: " + str(metrics.recall_score(predictions, validation_labels))
print "Precision: " + str(metrics.precision_score(predictions, validation_labels))

predictions = clf.predict(test_set)

print "\nTest set"

print "\nAccuracy Score: " + str(metrics.accuracy_score(predictions, test_labels))
print "F1 Score: " + str(metrics.f1_score(predictions, test_labels))
print "Recall: " + str(metrics.recall_score(predictions, test_labels))
print "Precision: " + str(metrics.precision_score(predictions, test_labels))
