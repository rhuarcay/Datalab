# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 18:09:34 2020

@author: Rodrigo
"""    
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
#Erstmal mit SVC(SVM) ausprobieren und danach es mit dem Bayes vergleichen

def my_function():
    print("here")


df = pd.read_csv(r'C:\Users\Rodrigo\Desktop\TU-Braunschweig\WS20-21\Datalab\Unit_1\Test_Spam_Filter\spam.csv')


X = df["message"]
Y = df["type"]

#Aufsplitung der Data in Train und Test Daten
X_Train, X_Test, Y_Train, Y_Test = train_test_split(X,Y, random_state=0)

#Pipeline um mehrere möglichkeiten zu probieren
pipeline = Pipeline([
    ("cv", CountVectorizer()),
    ("tffidf", TfidfTransformer()),
    ("svm", SVC())    
])

clf = GridSearchCV(pipeline, param_grid = {
    "svm__C": [0.01,0.1,1,10,100],
    "svm__gamma": [0.01,0.1,1,10,100],
   # "tffidf": [True,False],
   "cv__max_df": [0.25,0.5, 0.75, 1.0],
   "cv__min_df": [0.0001,0.001,0.01,0.1]
})

print("Model is been trained")
clf.fit(X_Train, Y_Train)

print(clf.best_params_)
print(clf.score(X_Test,Y_Test))

    
    