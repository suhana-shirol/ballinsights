import math
import random
import time
import pandas as pd
import numpy as np
import warnings
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

warnings.simplefilter(action='ignore', category=FutureWarning)
from sklearn.model_selection import train_test_split
from sklearn import svm

stats = pd.read_csv('prediction_data.csv')
stats = stats[-5000:]
X = stats[['WScore', 'WOR', 'WDR', 'LOR', 'LDR', 'WFGP', 'LFGP', 'WBlk', 'LBlk']]
y = stats['W_Home01']
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, test_size=0.3, random_state=100)

# SVM
model = svm.SVC(kernel='poly', degree=2)
model.fit(X_train, y_train)
y_predSVM = model.predict(X_test)
accuracy = accuracy_score(y_test, y_predSVM)*100
print("Accuracy for SVM is:", accuracy)

# Random Forest
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)
y_predRF = clf.predict(X_test)
print("Accuracy for random forest is: ", metrics.accuracy_score(y_test, y_predRF))

# KNN
knn = KNeighborsClassifier(n_neighbors=100)
knn.fit(X_train, y_train)
y_predKNN = knn.predict(X_test)
print("Accuracy for KNN is: ", classification_report(y_test, y_predKNN))