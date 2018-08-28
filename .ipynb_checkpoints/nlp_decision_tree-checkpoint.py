import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pdb
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix

dataset = pd.read_csv('all_reviews.tsv', delimiter = '\t', quoting = 3)

corpus = []

for i in range(0, len(dataset)):
    try:
        review = re.sub('[^a-zA-Z]', ' ', dataset['Reivew'][i])
        review = review.lower()
        review = review.split()
        ps = PorterStemmer()
        review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
    except:
        review = str(dataset['Reivew'][i])

    corpus.append(review)

cv = CountVectorizer()
X = cv.fit_transform(corpus).toarray()

y = dataset.iloc[:, 1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

true_positive = cm[1][1]
false_positive = cm[1][0]

true_negative = cm[0][0]
false_negative = cm[0][1]

true_positive_rate = true_positive/(true_positive + false_negative)
false_positive_rate = false_positive/(false_positive + true_negative)

accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)

precision = true_positive / (true_positive + false_positive)

recall = true_positive / (true_positive + false_negative)

f1_score = 2 * precision * recall / (precision + recall)